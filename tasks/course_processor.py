

from xml.etree import ElementTree as etree
import urllib

springURL = "http://courses.rice.edu/admweb/!SWKSECX.main?term=201320&title=&course=&crn=&coll=&dept=&subj="
fallURL = "http://courses.rice.edu/admweb/!SWKSECX.main?term=201310&title=&course=&crn=&coll=&dept=&subj="

opener = urllib.FancyURLopener({})
xmlFile = opener.open(springURL)
tree = etree.parse(xmlFile)

courses = tree.findall('//course')
KVPairs = []

for c in courses:
	# Get a key-value set of tag to text for each course
	data = (dict(zip([x.tag for x in c.getchildren()],
					 [x.text for x in c.getchildren()])))
	KVPairs.append(data)





opener = urllib.FancyURLopener({})
xmlFile = opener.open(fallURL)
tree = etree.parse(xmlFile)

courses = tree.findall('//course')

for c in courses:
	# Get a key-value set of tag to text for each course
	data = (dict(zip([x.tag for x in c.getchildren()],
					 [x.text for x in c.getchildren()])))