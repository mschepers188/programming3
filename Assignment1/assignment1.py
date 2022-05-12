from Bio import Entrez
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import time

class BioDownloader:
    
    def elinker(id):
        Entrez.email = "m.professional188@gmail.com"  # Tells pubmed who I am
        handle = Entrez.elink(dbfrom="pubmed", id=id, linkname="pubmed_pubmed", api_key='5fac5151cab100c58c572d349e388975b408')  # creates handle for search
        record = Entrez.read(handle)  # reads handle
        handle.close()  # closes handle
        linked = [link["Id"] for link in record[0]["LinkSetDb"][0]["Link"]]  # generates list with references
        return linked  # returns list with references


    def efetcher(id):
        time.sleep(1)
        print('sleeping...')
        Entrez.email = "m.professional188@gmail.com"
        handle = Entrez.efetch(db="pmc", id=id, rettype="XML", retmode="text", api_key='5fac5151cab100c58c572d349e388975b408')
        with open(f'output/{id}.xml', 'wb') as file:
            file.write(handle.read())
        print('file created')

    def multi_predict(predict, X):
        pool = Pool(cpu_count())
        pool.map(predict, X)
        pool.close()
        pool.join()

if __name__ == "__main__":
    biodownloader = BioDownloader
    references = biodownloader.elinker('30577416')[0:10]  # grabs 10 first references
    BioDownloader.multi_predict(biodownloader.efetcher, references)