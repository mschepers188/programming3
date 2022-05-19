from Bio import Entrez, Medline
import pandas as pd
import pickle
import os

class PMgetter:
    def __init__(self, email, api):
        self.email = email
        self.api_key = api

        if os.path.exists('output'):
            pass
        else:
            os.makedirs('output')

    def elinker(self, id, refnum):
        Entrez.email = self.email  # Tells pubmed who I am
        results = Entrez.read(Entrez.elink(dbfrom="pubmed",
                                           db="pmc",
                                           LinkName="pubmed_pmc_refs",
                                           id=id,
                                           api_key=self.api_key))
        references = [f'{link["Id"]}' for link in results[0]["LinkSetDb"][0]["Link"]]
        return references[0:refnum]

    def get_autors(self, pmid):
        # pmid = '19304878'
        Entrez.email = "m.professional188@gmail.com"     # Always tell NCBI who you are
        handle = Entrez.efetch(db="pubmed",id=pmid,rettype="medline",retmode="text")
        records = Medline.read(handle)

        autors = tuple(records['AU'])
        
        print(autors)
        
        # with open('tuplePickle.pkl','wb') as f: 
        #     pickle.dump(autors, f)
            # print("The tuple is pickled successfully.")


if __name__ == "__main__":
    pmgetter = PMgetter("m.professional188@gmail.com", '5fac5151cab100c58c572d349e388975b408')
    refs = pmgetter.elinker('19304878', 10)
    print(refs)
    # pmgetter.get_autors('19304878')