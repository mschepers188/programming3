from Bio import Entrez
from Bio import Medline

class PMgetter:
    def __init__(self, email, api):
        self.email = email
        self.api_key = api

    def get_autors(self, pmid):
        # pmid = '19304878'
        Entrez.email = "m.professional188@gmail.com"     # Always tell NCBI who you are
        handle = Entrez.efetch(db="pubmed",id=pmid,rettype="medline",retmode="text")
        records = Medline.parse(handle)

        for record in records:
            print(record["AU"])

if __name__ == "__main__":
    pmgetter = PMgetter("m.professional188@gmail.com", '5fac5151cab100c58c572d349e388975b408')
    print(pmgetter.get_autors('19304878'))