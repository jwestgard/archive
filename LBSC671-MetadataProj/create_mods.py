import json
from lxml import etree as etree

# Load the data from a JSON file
def load_json_dataset(filename):
    f = open(filename, 'r')
    result = json.load(f)
    f.close()
    return result

border = "\n" + "*" * 50
print border
print "\nWelcome to the MODS XML converter."
myFile = raw_input("\nPlease enter name of the datafile to load: ")
myData = load_json_dataset(myFile)
print "Data loaded successfully..."

# Create the XML root
xml = '''<modsCollection xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.loc.gov/mods/v3"
    xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-3.xsd"></modsCollection>'''
root = etree.fromstring(xml)

# Iterate through the data, creating each child element
for x in myData['response']['docs']:
    mods = etree.SubElement(root, 'mods')
    mods.attrib["version"] = "3.3"
    
    titleInfo = etree.SubElement(mods, 'titleInfo')
    title = etree.SubElement(titleInfo, 'title')
    
    # Check whether the key exists
    if 'pid' in x.keys():
        # populate the field with the pid value
        title.text = x['pid']
    
    subject = etree.SubElement(mods, 'subject')
    topic = etree.SubElement(subject, 'topic')
    
    # Check whether the key exists
    if 'dmTitle' in x.keys():
        # populate the field with the first value
        topic.text = x['dmTitle'][0]
        
    hierGeog = etree.SubElement(subject, 'hierarchicalGeographic')
    country = etree.SubElement(hierGeog, 'country')
    
    # Check whether the key exists
    if 'dmSubjectGeogCounty' in x.keys():
        # populate the field with the first value
        country.text = x['dmSubjectGeogCounty'][0]
    state = etree.SubElement(hierGeog, 'state')
    
    # Check whether the key exists
    if 'dmSubjectGeogRegion' in x.keys():
        # populate the field with the first value
        state.text = x['dmSubjectGeogRegion'][0]
    city = etree.SubElement(hierGeog, 'city')
    
    # Check whether the key exists
    if 'dmSubjectGeogSettlement' in x.keys():
        # populate the field with the first value
        city.text = x['dmSubjectGeogSettlement'][0]
    
    location = etree.SubElement(mods, 'location')
    url = etree.SubElement(location, 'url')
    
    # Check whether the key exists
    if 'handlehttp' in x.keys():
        # populate the field with the first value
        url.text = x['handlehttp'][0]

print "Completed XML tree generation."
print "Saving result.xml file...",

result = etree.ElementTree(root)
result.write('result.xml', pretty_print=True, xml_declaration=True)

print "File saved."

print "\nThanks for using the MODS XML converter!"
print border
