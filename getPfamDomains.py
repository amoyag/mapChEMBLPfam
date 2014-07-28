"""
Function: getTargets

gets UniProt accession for human proteins from the Chembl
target dictionary. Edited after getUniProtTargets
momo.sander@googlemail.com
"""
import queryDevice

def getTargets(release, user, pword, host, port):
    #release_number = int(release.split('_')[1])
    release_number = int(release)
    if release_number >= 15:
        rawtargets = queryDevice.queryDevice("""SELECT DISTINCT accession 
        FROM component_sequences
        WHERE ORGANISM = 'Homo sapiens'""", 'ChEMBL_%s' %release, user, pword, host, port)
    targets= []
    for target in rawtargets:
        targets.append(target[0])
    return targets 




"""
Function:  getDomains(targets) 

takes a list of ChEMBL targets and determines their domain content as reported in Pfam.
Results are stored in a hash domainDict[target][domain]= no_occurences(optional)
  --------------------

"""


def getDomains(targets,release):
  import urllib
  from xml.dom.minidom import parse  
  import xml.dom
  import pickle
  pfamDict ={}
  

  ## Loop through all targets and get pfam domains.
  errors = []
  for target in targets:
    #print "getting Pfam domains for %s" % target
    pfamDict[target] = {}
    pfamDict[target]["domains"] = []
    pfamDict[target]["start"] = []
    pfamDict[target]["end"] = []
    opener = urllib.FancyURLopener({})                                     
    f = opener.open("http://pfam.sanger.ac.uk/protein/%s?output=xml" % target) 
    dom = parse(f)
    if not dom.getElementsByTagName('sequence'):
      #print "encountered Error for %s" %target
      errors.append(target)
      del pfamDict[target]
      continue

    
    for pfam in dom.childNodes:
      if pfam.nodeName == 'pfam':
        for entry in pfam.childNodes:
          if entry.nodeName == 'entry':
            for matches in entry.childNodes:
              if matches.nodeName == 'matches':
                for match in matches.childNodes:
                  if match.nodeName == 'match':
                    if match.getAttribute('type') == 'Pfam-A':
                      pfamDict[target]['domains'].append(match.getAttribute('id'))
                      for location in match.childNodes:
                        if location.nodeName == 'location':
                          start = location.getAttribute('start')
                          end = location.getAttribute('end')
                          pfamDict[target]['start'].append(int(start))
                          pfamDict[target]['end'].append(int(end))
    dom.unlink()
    
    # Add domain count.
    pfamDict[target]['count'] = len(pfamDict[target]['domains'])
    
    # Calculate and add the uniq count of domains. 
    uniqDomains = {}
    for domain in pfamDict[target]['domains']:
      uniqDomains[domain] = 0   
    pfamDict[target]['countUnique'] = len(uniqDomains)
    
  ## Pickle the PfamDict
  output = open('data/protCodPfamDict_%s.pkl' %release, 'w')
  pickle.dump(pfamDict, output)

  print "encountered Error for", errors
  return pfamDict   
   


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 5:  # the program name and the two arguments

        sys.exit("Must specify release, user, pword, host, port")

        
    release = sys.argv[1]
    user = sys.argv[2]
    pword = sys.argv[3]
    host = sys.argv[4]
    port = int(sys.argv[5])

    targets = getTargets(release, user, pword, host, port)


getDomains(targets, release)





