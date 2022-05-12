from Bio import Entrez
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
import time
import os
import argparse as ap


class BioDownloader:

    def __init__(self, email, api):
        self.email = email
        self.api_key = api
        if os.path.exists('output'):
            pass
        else:
            os.makedirs('output')

    def elinker(self, id):
        Entrez.email = self.email  # Tells pubmed who I am
        results = Entrez.read(Entrez.elink(dbfrom="pubmed",
                                           db="pmc",
                                           LinkName="pubmed_pmc_refs",
                                           id=id,
                                           api_key=self.api_key))
        references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]
        return references

    def efetcher(self, id):
        time.sleep(1)
        Entrez.email = self.email
        handle = Entrez.efetch(db="pmc",
                               id=id,
                               rettype="XML",
                               retmode="text",
                               api_key=self.api_key)
        with open(f'output/{id}.xml', 'wb') as file:
            file.write(handle.read())

    def multi_predict(self, predict, x):
        pool = Pool(cpu_count())
        pool.map(predict, x)
        pool.close()


if __name__ == "__main__":
    argparser = ap.ArgumentParser(
        description="Script that downloads (default) 10 articles referenced by the given PubMed ID concurrently.")
    argparser.add_argument("-n", action="store",
                           dest="n", required=False, type=int,
                           help="Number of references to download concurrently.")
    argparser.add_argument("pubmed_id", action="store", type=str, nargs=1,
                           help="Pubmed ID of the article to harvest for references to download.")
    args = argparser.parse_args()
    print("Getting: ", args.pubmed_id)

    biodownloader = BioDownloader("m.professional188@gmail.com", '5fac5151cab100c58c572d349e388975b408')
    references = biodownloader.elinker(args.pubmed_id)[0:10]  # grabs 10 first references
    biodownloader.multi_predict(biodownloader.efetcher, references)
    print('The requested files have been downloaded to "output"')