from unittest import result
from Bio import Entrez
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

class BioDownloader:
    
    def elinker(id):
        Entrez.email = "m.professional188@gmail.com"  # Tells pubmed who I am
        handle = Entrez.elink(dbfrom="pubmed", id=id, linkname="pubmed_pubmed")  # creates handle for search
        record = Entrez.read(handle)  # reads handle
        handle.close()  # closes handle
        linked = [link["Id"] for link in record[0]["LinkSetDb"][0]["Link"]]  # generates list with references
        return linked  # returns list with references

    def efetcher(id):
        Entrez.email = "m.professional188@gmail.com"
        handle = Entrez.efetch(db="pubmed", id=id, rettype="gb", retmode="xml", )
        record = Entrez.read(handle)
        return record


    def multi_predict(predict, X):
        pool = Pool(cpu_count())
        results = pool.map(predict, X)
        pool.close()
        pool.join()
        return results

if __name__ == "__main__":
    biodownloader = BioDownloader
    references = biodownloader.elinker('30577416')[0:10]  # grabs 10 first references
    result = BioDownloader.multi_predict(biodownloader.efetcher, references)
    
    # print(biodownloader.efetcher(references))
    # cpus = mp.cpu_count()
    # with mp.Pool(cpus) as pool:
    #     results = pool.map(efetcher, querylist)