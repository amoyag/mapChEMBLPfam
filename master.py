"""
Function:  master 

Goes through all necessary steps.
    --------------------
    Author:
    Felix Kruger
    fkrueger@ebi.ac.uk
"""  

def master(release, user, pword, host, port): 
    

    ## Get all human protein coding genes from ensembl and a count of all uniqe domains.
    import os
    import pfamDomains  #creates pfamDict and pfam_domains
    import mapPfamDomains   #Carry out the mapping and save results
    import pdbChembl    #Retrieves all binding site residues for interactions in ChEMBL.
    import uniprotChembl    ### Get all protein targets from ChEBML. ## Get Uniprot binding site annotation for each target.
    import analysis     #Carries out the analysis of the data generated in the previous steps.
    import yaml     #YAML is a data serialization format designed for human readability and interaction with scripting languages.
    # Read config file.
    paramFile = open('mpf.yaml')
    params = yaml.safe_load(paramFile)
    user = params['user']
    pword = params['pword']
    host = params['host']
    port = params['port']
    th = params['threshold']


    
    # Get Uniprot identifiers for all human proteins.
    os.system("R CMD BATCH --vanilla queryBioMaRt.R")
    # Map Pfam domains and positions to all Uniprot identifiers.
    #pfamDomains.pfamDomains(release, user, pword, host, port)
    # Map small molecule binding to Pfam domains.
    mapPfamDomains.mapPDs(th, release, user, pword, host, port)
    # Get all ChEMBL interactions in PDB and binding site residues.
    #pdbDict = pdbChembl.query(release, user, pword, host, port)
    # Get all ChEMBL interactions in Uniprot and binding site annotation.
    #uniprotDict = uniprotChembl.query(release, user, pword, host, port)
    # Analyze the data.
    #analysis.analysis(th, release, user, pword, host, port)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 5:  # the program name and the two arguments

        sys.exit("Must specify release, user, pword, host, port")

        
    release = sys.argv[1]
    user = sys.argv[2]
    pword = sys.argv[3]
    host = sys.argv[4]
    port = int(sys.argv[5])

    master(release, user, pword, host, port) 
