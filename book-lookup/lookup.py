from urllib.request import urlopen
import re


def fetchWebpage(url):
    data = str(urlopen(url).read())
    return data

 
def extractTitle(data):
    r = re.compile('<title>(.*?)</title>')
    m = r.search(data)
    if m:
        return m.group(1)
    else:
        print('Error: Not found')

        
def buildQuery(data):
    isbn = data.replace('-','').replace(' ','')
    url = "http://z3950.loc.gov:"
    query = "7090/voyager?version=1.1&operation=searchRetrieve&query="
    params = "&maximumRecords=1&recordSchema=marcxml"
    search = url + query + str(isbn) + params
    return search


def extractField(data):
    r = re.compile('<datafield tag="050".+?<subfield code="a">(.*?)</subfield>')
    m = r.search(data)
    if m:
        return m.group(1)
    else:
        print('Error: Not found')
    

print("\n\nWelcome to the Book Lookup script!")
print("\nWould you like to lookup a book, or search a URL?")
choice = input("Press B for book, U for URL: ")

while choice not in ["B","U"]:
    choice = input("\nYou must enter either B or U! Try again: ")

if choice == "B":
    isbn = input("Enter the ISBN: ")
    q = buildQuery(isbn)
    record = fetchWebpage(q)
    result = extractField(record)
    print(result)
    
elif choice == "U":
    target = input("\nEnter the URL from which you would like to extract the title: ")
    webpage = fetchWebpage(target)
    result = extractTitle(webpage)
    print(result)
