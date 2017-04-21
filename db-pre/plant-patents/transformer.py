#!/usr/bin/env python3

import csv
from datetime import datetime as dt
from operator import itemgetter as ig
import os
from pdfrw import PdfReader
import sys

PATH_TO_PDFS = "allfiles/"
PURL_BASE = 'http://patft.uspto.gov/netacgi/nph-Parser?patentnumber='
IURL_BASE = 'http://www.lib.umd.edu/plantpatents/binaries'

results = []


# extract file metadata for the file itself
def get_file_metadata(filepath):
    if os.path.exists(filepath):
        mtime = dt.fromtimestamp(os.stat(filepath).st_mtime)
        pdf = PdfReader(filepath)
        pages = len(pdf.pages)
    else:
        mtime = ''
        pages = ''
    return (mtime, pages)


# check for existing scans
print("Checking directory '{0}' for scans...".format(PATH_TO_PDFS), end='')
all_files = []
for (root, dirs, files) in os.walk(PATH_TO_PDFS):
    for f in files:
        all_files.append(os.path.join(root,f))
print("found {0} PDFs!".format(len(all_files)))

# read metadata file for existing items
print("Reading metadata from {0}...".format(sys.argv[1]), end='')
with open(sys.argv[1], 'r') as f1:
    newdata = [line for line in csv.DictReader(f1)]
    print("{0} lines read.".format(len(newdata)))

# read new metadata file
print("Reading metadata from {0}...".format(sys.argv[2]), end='')
with open(sys.argv[2], 'r') as f2:
    olddata = {line['patent_number']: line for line in csv.DictReader(f2)}
    print("{0} lines read.".format(len(olddata)))

# loop and process each entry
for row in newdata:
    print("Processing data...")
    
    # construct file path and get file metadata
    number = row['patent_number']
    folder = number[2:5] + '00'
    filename = number.lower() + '.pdf'
    filepath = '/'.join([PATH_TO_PDFS, folder, filename])
    filemeta = get_file_metadata(filepath)
    
    # remove zero-padding from patent number for use in URL
    if number.startswith('PP0'):
        purl_number = "PP" + number[3:]
    else:
        purl_number = number
    
    # map data and transform or construct additional values
    new_item = {
        'id': '',
        'title': row['title'],
        'date': row['date'],
        'year': row['date'][:4],
        'patent_number': row['patent_number'],
        'large_category': row['large_category'],
        'inventor': ';'.join([row['applicant1'], row['applicant2']]),
        'city': ';'.join([row['app1_city'], row['app2_city']]),
        'state': ';'.join([row['app1_st'], row['app2_st']]),
        'country': ';'.join([row['app1_co'], row['app2_co']]),
        'uspc': row['ccl'],
        'application_number': row['app_no'].replace(',', ''),
        'application_date': row['filed'],
        'application_year': row['filed'][:4],
        'image_url': '/'.join([IURL_BASE, folder, filename]),
        'patent_url': '{0}{1}'.format(PURL_BASE, purl_number),
        'display_title': '{0} -- {1}'.format(row['patent_number'],
                                             row['title']),
        'scan_date': str(filemeta[0]),
        'pages': str(filemeta[1]),
        'assignee': row['assignee'],
        'assignee_city': row['acity'],
        'assignee_state': row['astate'],
        'assignee_country': row['aco'],
        'notes': ''
    }
    
    # remove extraneous separator characters
    for k,v in new_item.items():
        if type(v) is str:
            new_item[k] = v.strip(';')
        
    # verify against existing spreadsheet
    if number in olddata:
        # bring over old IDs and notes
        new_item['id'] = olddata[number]['id']
        new_item['notes'] = olddata[number]['notes']
        for key, oldvalue in olddata[number].items():
            newvalue = new_item[key]
            if oldvalue == newvalue:
                pass
            else:
                print("{0}: '{1}' vs. '{2}'".format(key, newvalue, oldvalue))

    results.append(new_item)

# sort and write out results
sorted_results = sorted(results, key=ig('patent_number'))

# give ids to all items, preserving existing ids
max_id = max([int(r['id']) for r in sorted_results if r['id'] is not ''])
next_id = max_id + 1
for item in sorted_results:
    if item['id'] == '':
        item['id'] = next_id
        next_id += 1
    else:
        continue

fieldnames = [  'id','patent_number','date','year','title',
                'display_title','large_category','inventor',
                'city','state','country','uspc','image_url',
                'patent_url','scan_date','pages','application_number',
                'application_date','application_year','assignee',
                'assignee_city','assignee_state','assignee_country',
                'notes']

with open(sys.argv[3], 'w') as outfile:
    dw = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='ignore')
    dw.writeheader()
    for row in sorted_results:
        dw.writerow(row)
        
    

'''
# field mapping: 

id                  calculate
title               [copy]
patent_number       [copy]
large_category      [copy]

inventor            applicant1  applicant2
city                app1_city   app2_city
state               app1_st     app2_st
country             app1_co     app2_co

date                date (formerly application_date)
notes               N/A

uspc                ccl
application_number  app_no
application_date    filed
application_year    [calculate]
image_url           [construct]
patent_url          [construct]
pages               [grab]
scan_date           [grab]
display_title       [construct]

assignee            assignee            [discard]
assignee_city       acity               [discard]
assignee_state      astate              [discard]
assignee_country    aco                 [discard]
'''
