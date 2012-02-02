"""
  Function:  mapPDsa
  --------------------
  Carry out the mapping and save results.
  
  momo.sander@googlemail.com
"""                              
def mapPDs(release, user, pword): 

  ## Set the threshold.
  import numpy as np
  threshold = -np.log10(50*10**(-6))
  
  ## Get a list of all ChEMBL targets.
  import getUniProtTargets
  chemblTargets = getUniProtTargets.getUniprotTargets(release)

  ## Load the pfamDict.
  inFile = open('data/protCodPfamDict_%s.pkl' %release, 'r')
  pfamDict = pickle.load(inFile)
  inFile.close()    

  ## Get ligands for targets with single domains.
  import singleDomains 
  single = singleDomains.singleDomains(pfamDict, chemblTargets, threshold, release, loadOld)

  ## Construct the propDict for targets with one domain and manually 
  ## insert/delete ligands. From this, we also derive the list of winners, ie. 
  ## domains binding ligands with at least micromolar affinity. 
  import feedPropDict
  import parse
  blacklist = parse.col2list('data/removeLigands.txt',1, False)  
  propDict = {}
  propDict = feedPropDict.dictionary(single, propDict, blacklist 'single')
  propDict = feedPropDict.addLigs(propDict,'manual') 
  
  ## Extract a list of validated domains.
  valid = propDict.keys() 

  ## Identify targets with one binding site containing domain and at least one
  ## other domain.
  import multiDomain
  multi = multiDomain.multiDomain(pfamDict, chemblTargets, valid, threshold, release)

  ## Deal with targets that have more than one binding site containing 
  ## domain. Interface with Sam's text mining process.
  import findConflicts
  conflicts = findConflicts.findConflicts(pfamDict, valid, chemblTargets)

  ## Insert data for conflicts and multi domain proteins
  import feedPropDict
  propDict = feedPropDict.dictionary(multi, propDict, 'multi')
  propDict = feedPropDict.dictionary(confDict, propDict, 'conflict')

  ## Export the mapping to a mySQL table.
  import exportDict
  export.exportMapsMySQL(propDict, release)
  export.exportConflsMySQL(conflicts, release)
  
