#!/usr/bin/env python3
#
#=============================================
#| harvest.py | Joshua Westgard | 2015-06-30 |
#=============================================
# Usage --> python3 harvest.py sourcedir/
#

import sys, os
from lxml import etree as etree
from bs4 import BeautifulSoup

rootpath = sys.argv[1]

def listFiles(rootdir):
    result = []
    print('Searching {0} ...'.format(rootdir))
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            p = os.path.join(root,f)
            result.append(os.path.abspath(p))
    print('Found {0} files in the specified directory tree.'.format(len(result)))
    return result

def readFile(sourcefile):
    with open(sourcefile, "rb") as f:
        soup = BeautifulSoup(f)
        lines = parseSourceHTML(soup)
        return lines
        
def writeFile(data, origpath):
    stub = origpath.replace(rootpath,'')
    outpath = 'output/{0}.xml'.format(stub.replace('/','_'))
    with open(outpath, 'w') as f:
        f.write(data)
            
def parseSourceHTML(source):
    data = {}
    data['site'] = "http://ganjoor.net/"
    poem = source.find("div", class_="poem")
    if poem:
        data['id'] = poem['id']
        anchor = poem.h2.a
        data['url'] = anchor['href']
        data['title'] = anchor.string
        lines = poem.find_all("div", class_="b")
        data['text'] = []
        for n, line in enumerate(lines):
            num = n + 1
            a = line.find("div", class_="m1").p.string
            b = line.find("div", class_="m2").p.string
            data['text'].append((num, a, b))
        return data

def teixml(data):
    # create root element and tree object
    root = etree.Element('tei')
    tei = etree.ElementTree(root)
    # create source element and sub-elements
    source = etree.SubElement(root, 'source')
    for elem in ['site','url','id']:
        etree.SubElement(source, elem).text = data[elem]
    text = etree.SubElement(root, 'text')
    title = etree.SubElement(text, 'title').text = data['title'].replace("\n","")
    body = etree.SubElement(text, 'body')
    for n, a, b in data['text']:
        line = etree.SubElement(body, 'line')
        line.set('id', "n {0}".format(n))
        etree.SubElement(line, 'a').text = a
        etree.SubElement(line, 'b').text = b
    return etree.tostring(tei, pretty_print=True, xml_declaration=True, 
        encoding='utf-8').decode()

def main():
    files_to_convert = listFiles(sys.argv[1])
    for f in files_to_convert:
        data = readFile(f)
        if data:
            result = teixml(data)
            print('Writing TEI file for {0}'.format(f))
            writeFile(result, f)
        else:
            print('No poem found in {0}.\n'.format(f))  

main()
    
