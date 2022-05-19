from Bio import Entrez, Medline
import pickle
import os
import argparse as ap

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

        authors = Medline.read(handle)['AU']  # Gets the records with read and selects the authors

        with open(f'output/{pmid}.authors.pickle', 'wb') as f:
            pickle.dump(authors, f)
            print(f"{pmid} authors pickled successfully.")


if __name__ == "__main__":
    # Instanciating argparser
    argparser = ap.ArgumentParser(
        description="Script that downloads (default) 10 articles referenced by the given PubMed ID "
                    "concurrently and extracts their authors.")
    argparser.add_argument("-n num", "--number_peons",
                           action="store_true",
                           dest="peons",
                           help="Number of peons per client.")
    argparser.add_argument("pubmed_id",
                           action="store",
                           type=str,
                           nargs=1,
                           help="Pubmed ID of the article to harvest for references to download.")
    args = argparser.parse_args()
    print("Args:", args)
    print("Getting child references: ", args.pubmed_id)

    pmgetter = PMgetter("m.professional188@gmail.com", '5fac5151cab100c58c572d349e388975b408')
    # example pmid = '19304878'

    refs = pmgetter.elinker(args.pubmed_id, 10)
    print(refs)
    for i in refs:
        pmgetter.get_autors(i)

# assignment2.py -n <number_of_peons_per_client>
# [-c | -s] --port <portnumber>
# --host <serverhost>
# -a <number_of_articles_to_download> STARTING_PUBMED_ID