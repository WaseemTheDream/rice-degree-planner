

from lxml import etree
import urllib

springURL = "http://courses.rice.edu/admweb/!SWKSECX.main?term=201320&title=&course=&crn=&coll=&dept=&subj="
fallURL = "http://courses.rice.edu/admweb/!SWKSECX.main?term=201310&title=&course=&crn=&coll=&dept=&subj="

opener = urllib.FancyURLopener({})
xmlFile = opener.open(springURL)

tree = etree.parse(xmlFile)






opener = urllib.FancyURLopener({})
xmlFile = opener.open(fallURL)
