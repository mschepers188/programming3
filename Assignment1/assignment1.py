from Bio import Entrez
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import time

class BioDownloader:
    
    def elinker(id):
        Entrez.email = "m.professional188@gmail.com"  # Tells pubmed who I am
        results = Entrez.read(Entrez.elink(dbfrom="pubmed", db="pmc", LinkName="pubmed_pmc_refs", id=id, api_key='5fac5151cab100c58c572d349e388975b408'))
        references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]
        return references


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
        # pool.join()


if __name__ == "__main__":
    biodownloader = BioDownloader
    references = biodownloader.elinker('30577416')[0:10]  # grabs 10 first references
    print(references)
    BioDownloader.multi_predict(biodownloader.efetcher, references)