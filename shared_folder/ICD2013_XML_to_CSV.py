'''
Created on Jul 17, 2012

@author: Josh Lipschultz
'''

from lxml import etree
import os
import time
import csv

def ICD2013_XML_to_CSV():
    start_time = time.clock()
    # Tags
    data = [['Billable?', 'Code', 'Description', 'inclusionTerm', 'sevenChrNote', 'sevenChrDef',
             'includes', 'excludes1', 'excludes2', 'codeFirst', 'useAdditionalCode',
             'codeAlso', 'notes']] # Notice double bracket
    
    print os.getcwd()
    xmltree = etree.parse('ICD10CM_FY2013_Full_XML_Tabular.xml')
    
    print data
    diag_list = xmltree.xpath('//diag/name')
    for ele in diag_list:
        linedata = ['' for i in range(13)]
        siblings = ele.getparent().getchildren()
    
        linedata[0] = 0 if ('diag' in [x.tag for x in siblings]) else 1     #is billable?
        linedata[1] = ele.text
        linedata[2] = ele.getnext().text
        
        for optionalTag in siblings:
            if optionalTag.tag == 'diag' or optionalTag.tag not in data[0]:
                continue
            linedata[ data[0].index(optionalTag.tag) ] = " || ".join([x.text for x in optionalTag.iterchildren()])
        
        data.append(linedata)
    #        print data[-1]  # (increases runtime by a factor of 8)
    
    # save to CSV:
    csvWriter = csv.writer(open('icd10-cm-2013.csv', 'wb'), delimiter=',')
    csvWriter.writerows(data)
    print "Elapsed Time: " + str(time.clock() - start_time) + "s"
    
    
if __name__ == '__main__':
    ICD2013_XML_to_CSV()