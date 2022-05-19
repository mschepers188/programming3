from Bio import Entrez

# Entrez.email = "m.professional188@gmail.com"     # Always tell NCBI who you are
# handle = Entrez.esearch(db="journals", term="computational")
# record = Entrez.read(handle)
# record["Count"]

class Autorgetter:

    def __init__(self, email, api):
        self.email = email
        self.api_key = api

        # if os.path.exists('output'):
        #     pass
        # else:
        #     os.makedirs('output')

    def elinker(self, id):
        Entrez.email = self.email  # Tells pubmed who I am
        results = Entrez.read(Entrez.elink(dbfrom="pubmed",
                                           db="pmc",
                                           LinkName="pubmed_pmc_refs",
                                           id=id,
                                           api_key=self.api_key))

record[0]["Id"]
record[0]["Title"]
'Computational biology and chemistry'
record[0]["Publisher"]


        references = [f'{link["Id"]}' for link in results[0]["autor"][0]["Link"]]
        return references

autorgetter = Autorgetter("m.professional188@gmail.com", '5fac5151cab100c58c572d349e388975b408')
print(autorgetter.elinker('19304878')[0:10])
