import multiprocessing as mp
from Bio import Entrez

def querylister(query):
    Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
    handle = Entrez.esearch(db="pubmed", term=f"{query}[title]", retmax="10" )
    record = Entrez.read(handle)
    return record["IdList"]

def efetcher(id):
    Entrez.email = "A.N.Other@example.com"  # Always tell NCBI who you are
    handle = Entrez.efetch(db="pubmed", id=id, retmode="xml")  # rettype="gb", retmode="text"
    return handle.read()

if __name__ == "__main__":
    querylist = querylister('COVID')
    # xmlout = efetcher(querylist)
    # print(xmlout)
    cpus = mp.cpu_count()
    with mp.Pool(cpus) as pool:
        results = pool.map(efetcher, querylist)
    print(results)