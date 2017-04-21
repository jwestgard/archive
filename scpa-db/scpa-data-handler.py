#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, csv, sys, re

def parse_csv(source, fieldnames):
    input_data = csv.DictReader(open(source, 'r'))
    input_data.fieldnames
    output_data = [line for line in input_data]
    print("\nRead {0} rows of data from {1}.\n".format(len(output_data), source))
    return output_data

def load_json_dataset(filename):
    f = open(filename, 'r')
    result = json.load(f)
    f.close()
    return result

def save_json_dataset(filename, data):
    f = open(filename, 'w')
    f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    f.close()

def write_list_to_file(filename, result):
    f = open(filename, 'w')
    f.write('\n'.join(result))
    f.close()
    
def value_range(field, data):
    hits = len([row[field] for row in data if row[field] != ""])
    misses = len([row[field] for row in data if row[field] == ""])
    unique_values = set([row[field] for row in data])
    return hits, misses, len(unique_values)
    
def profile_dataset(data, fields):
    result = {}
    border = "+" + "-" * 91 + "+"
    cols = ["Field Name", "Number Populated", "Number Blank", "Unique Count"]
    header = "| {0} |".format(" | ".join([col.upper().center(20) for col in cols]))
    for field in fields:
        result[field] = value_range(field, data)
       # print("| {0} | {1} | {2} | {3} |".format(field, hits, misses, len(unique_values)))
    print(border)
    print(header)
    print(border)
    for key in result.keys():
        column_values = " | ".join([str(result[key][x]).ljust(20) for x in range(3)])
        print("| {0} | {1} |".format(key.rjust(20), column_values))
    print(border)

sourcefile = sys.argv[1]
scores_fieldnames = ['id', 'composer', 'title', 'imprint', 'additional_info', 'collation',
              'collection', 'difficulty', 'duration', 'ensemble',
              'fair_use', 'instrumentation', 'location', 'pages', 'solo_difficulty',
              'special']

mydata = parse_csv(sourcefile, scores_fieldnames)
profile_dataset(mydata, scores_fieldnames)
save_json_dataset('output.json', mydata)

master_instrumentation = []
for x in mydata:
    if x['instrumentation']:
        master_instrumentation.extend(re.split(", | or | and ", x['instrumentation']))

for i in sorted(master_instrumentation):
    print(i)
                
                