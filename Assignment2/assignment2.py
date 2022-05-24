
import multiprocessing as mp
from multiprocessing.managers import BaseManager, SyncManager
import os, sys, time, queue
from Bio import Entrez, Medline
import pickle
import os
import argparse as ap

POISONPILL = "MEMENTOMORI"
ERROR = "DOH"
AUTHKEY = b'whatistheairspeedvelocityofanulandenswallow?'

class PMgetter:
    def __init__(self, email, api):
        self.email = email
        self.api_key = api

        if os.path.exists('output'):
            pass
        else:
            os.makedirs('output')

    def elinker(self, pmid, numchildren=10):
        Entrez.email = self.email  # Tells pubmed who I am
        results = Entrez.read(Entrez.elink(dbfrom="pubmed",
                                           db="pmc",
                                           LinkName="pubmed_pmc_refs",
                                           id=pmid,
                                           api_key=self.api_key))
        references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]
        return references[0:numchildren]

    def get_autors(self, pmid):
        Entrez.email = self.email     # Always tell NCBI who you are
        handle = Entrez.efetch(db="pubmed",
                               id=pmid,
                               rettype="medline",
                               retmode="text",
                               api_key=self.api_key)

        authors = tuple(Medline.read(handle)['AU'])  # Gets the records with read and selects the authors

        with open(f'output/{pmid}.authors.pickle', 'wb') as f:
            pickle.dump(authors, f)
            print(f"{pmid} authors pickled successfully.")

        # Added for XML output
        handle2 = Entrez.efetch(db="pubmed", id=pmid, rettype="XML", retmode="text", api_key=self.api_key)
        with open(f'output/{pmid}.xml', 'wb') as file:
            file.write(handle2.read())


def make_server_manager(port, authkey, ip):
    """ Create a manager for the server, listening on the given port.
        Return a manager object with get_job_q and get_result_q methods.
    """
    job_q = queue.Queue()
    result_q = queue.Queue()

    # This is based on the examples in the official docs of multiprocessing.
    # get_{job|result}_q return synchronized proxies for the actual Queue
    # objects.
    class QueueManager(BaseManager):
        pass

    QueueManager.register('get_job_q', callable=lambda: job_q)
    QueueManager.register('get_result_q', callable=lambda: result_q)

    manager = QueueManager(address=(ip, port), authkey=authkey)
    manager.start()
    print('Server started at port %s' % port)
    return manager

def runserver(fn, data, ip, port):
    # Start a shared manager server and access its queues
    manager = make_server_manager(port, AUTHKEY, ip)
    shared_job_q = manager.get_job_q()
    shared_result_q = manager.get_result_q()
    
    if not data:
        print("Gimme something to do here!")
        return
    
    print("Sending data!")
    for d in data:
        shared_job_q.put({'fn' : fn, 'arg' : d})
    
    time.sleep(2)  
    
    results = []
    while True:
        try:
            result = shared_result_q.get_nowait()
            results.append(result)
            print("Got result!", result)
            if len(results) == len(data):
                print("Got all results!")
                break
        except queue.Empty:
            time.sleep(1)
            continue
    # Tell the client process no more data will be forthcoming
    print("Time to kill some peons!")
    shared_job_q.put(POISONPILL)
    # Sleep a bit before shutting down the server - to give clients time to
    # realize the job queue is empty and exit in an orderly way.
    time.sleep(5)
    print("Aaaaaand we're done for the server!")
    manager.shutdown()
    print(results)

def make_client_manager(ip, port, authkey):
    """ 
    Create a manager for a client. This manager connects to a server on the
    given address and exposes the get_job_q and get_result_q methods for
    accessing the shared queues from the server.
    Return a manager object.
    """
    class ServerQueueManager(BaseManager):
        pass

    ServerQueueManager.register('get_job_q')
    ServerQueueManager.register('get_result_q')

    manager = ServerQueueManager(address=(ip, port), authkey=authkey)
    manager.connect()

    print('Client connected to %s:%s' % (ip, port))
    return manager



def runclient(num_processes, ip, portnum):
    manager = make_client_manager(ip, portnum, AUTHKEY)
    job_q = manager.get_job_q()
    result_q = manager.get_result_q()
    run_workers(job_q, result_q, num_processes)
    
def run_workers(job_q, result_q, num_processes):
    processes = []
    for p in range(num_processes):
        temP = mp.Process(target=peon, args=(job_q, result_q))
        processes.append(temP)
        temP.start()
    print("Started %s workers!" % len(processes))
    for temP in processes:
        temP.join()

def peon(job_q, result_q):
    my_name = mp.current_process().name
    while True:
        try:
            job = job_q.get_nowait()
            if job == POISONPILL:
                job_q.put(POISONPILL)
                print("Aaaaaaargh", my_name)
                return
            else:
                try:
                    result = job['fn'](job['arg'])
                    print("Peon %s Workwork on %s!" % (my_name, job['arg']))
                    result_q.put({'job': job, 'result' : result})
                except NameError:
                    print("Can't find yer fun Bob!")
                    result_q.put({'job': job, 'result' : ERROR})

        except queue.Empty:
            print("sleepytime for", my_name)
            time.sleep(1)



if __name__ == "__main__":
    # Instanciating argparser
    argparser = ap.ArgumentParser(
        description="Script that downloads (default) 10 articles referenced by the given PubMed ID "
                    "concurrently and extracts their authors.")
    argparser.add_argument("-n", "--number_peons", action="store", type=int, dest="peons", help="Number of peons per client.")
    argparser.add_argument("--port", action="store", type=int, dest="port", help="portnumber")
    argparser.add_argument("--host", action="store", dest="host", help="serverhost")
    argparser.add_argument("-a", action="store", type=int, dest="n_articles", default=10, help="number_of_articles_to_download")
    argparser.add_argument("pubmed_id", action="store", type=str, nargs=1, help="Pubmed ID of the article to harvest for references to download.")
    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-c", action="store_true", dest="clients", help="Number_of_clients.")
    group.add_argument("-s", action="store_true", dest="servers", help="Number_of_servers")
    args = argparser.parse_args()
    print("Args:", args)
    print("Getting child references: ", args.pubmed_id)

    pmgetter = PMgetter("m.professional188@gmail.com", '5fac5151cab100c58c572d349e388975b408')
    # example pmid = '19304878'
 
    refs = pmgetter.elinker(pmid=args.pubmed_id, numchildren=args.n_articles)

    ip = args.host
    portnum = args.port

    if args.clients:
        client = mp.Process(target=runclient, args=(4, ip, portnum))
        client.start()
        client.join()

    if args.servers:
        servers = mp.Process(target=runserver, args=(pmgetter.get_autors, refs, ip, portnum))
        servers.start()
        servers.join()
    
    time.sleep(1)

# python assignment2.py -n 5 -s --port 1024 --host nuc417 -a 10 19304878
# python assignment2.py -n 5 -c --port 1024 --host nuc417 -a 10 19304878
