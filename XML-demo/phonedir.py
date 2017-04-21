from lxml import etree						# import the etree module from the lxml package

with open('input.txt', 'r') as inputfile:			# read the input data from a file
	data = [item.rstrip("\n").split("\t") 
		for item in inputfile.readlines()]		# parse input data into a list

root = etree.Element('phonedirectory')				# define the root element for our xml tree
myphonedir = etree.ElementTree(root)				# create the xml tree with the predefined root element

for item in data:						# iterate through the dataset
    entry = etree.SubElement(root, 'entry')			# for each line of data, create a child of root called entry
    number = etree.SubElement(entry, 'number')			# for each entry, create a child of entry called number
    name = etree.SubElement(entry, 'name')			# for each entry, create a child of entry called name
    name.text = item[0]						# populate name with 0th (i.e. first) value from line of data
    number.text = item[1]					# populate number with 1st (i.e. second) value from line of data

with open('output.xml', 'wb') as outputfile:			# open a file in write mode
	myphonedir.write(outputfile, pretty_print=True)		# write the xml tree to the file in "pretty print" format
