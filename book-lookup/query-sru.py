import re
from urllib.request import urlopen


def load_file(type):
    filename = input("\nEnter the name of the %s file: " % (type))
    if type == 'isbn':
        f = open(filename, 'r').readlines()
    else:
        f = open(filename, 'r').read()
    print(f)
    return(f)


def fetch_page(url):
    data = str(urlopen(url).read())
    return data


def build_query(data):
    isbn = data.replace('-','').replace(' ','').replace('\n','')
    url = "http://z3950.loc.gov:"
    query = "7090/voyager?version=1.1&operation=searchRetrieve&query="
    params = "&maximumRecords=1&recordSchema=marcxml"
    search = url + query + isbn + params
    print(search)
    return search


def query_sru(isbn):
    q = build_query(isbn)
    record = fetch_page(q)
    result = extract_field(record)
    print(result)


def extract_field(data):
    r = re.compile('<datafield tag="050".+?<subfield code="a">(.*?)</subfield>')
    m = r.search(data)
    if m:
        return m.group(1)
    else:
        print('Error: Not found')
    

def greeting():
    print("\n\nWelcome to Query-SRU!")
    print("\n\nThis program batch searches the LOC's Search/Retrieval via URL ")
    print("service, returning the requested fields to a CSV file.")
    

def main():
    greeting()
    isbnlist = load_file("isbn")
    for i in isbnlist:
        print("Searching for " + i)
        query_sru(i)
    



main()


