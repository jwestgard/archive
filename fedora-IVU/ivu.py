from time import sleep
from urllib.request import urlopen

# Read PIDs from specified file.
pidfile = input('Enter the name of the PID file: ')
f = open(pidfile, 'r').readlines()

# Empty list for storing URLs.
result = []

# Attach each PID to the base URL.
baseurl = "http://fedora.lib.umd.edu/index/add/"
for pid in f:
    q = baseurl + pid
    result.append(q.rstrip('\n'))

# Save the list of URLs in a text file.   
f = open('urls.txt', 'w')
f.write("\n".join(result))
f.close()

# Give feedback on progress to the user.
print('\n\nFinished creating the list of URLs.')
input('Hit return to display them.')
for url in result:
    print(url)

# Ask the user whether they wish to proceed from here.
response = input('\nWould you like to send these requests to the server? (Y or N)')
while response not in ['Y','N']:
    response = input('Please enter Y or N: ')

# Use urllib.request to issue requests to server,
# pausing for 1 second between each request.
if response == "Y":
    print('\nExecuting HTTP request for each URL...')
    for url in result:
        print('\nRequesting ' + url)
        response = str(urlopen(url).read())
        # Print the server's response to the screen.
        print('Response = ' + response)
        # Pause to ensure that the server can keep up.
        sleep(1)
elif response == 'N':
    quit
    