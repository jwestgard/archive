# import the regular expressions module
import re

# Ask the user to specify the text file to search
sourceFile = input("\nWelcome to the PID extractor!\n\nEnter the name of the data file: ")
# Open the specified text file in read mode, reading it line-by-line into a list
f = open(sourceFile, 'r').readlines()
# Create an empty list to hold the results
result = []

# Loop through the lines of the original input
for line in f:
    # search for matches in each line
    pid = re.search('\((umd:\d+?);', line)
    # if a match is found
    if pid:
        # append the matched substring to the results list
    	result.append(pid.group(1))
    # Otherwise, if no match go to the next line
    else:
    	pass

# After finishing looping through the data,
# print the results list to the screen
print(result)
# Then open a text file in write mode to store the results
f = open("result.txt", mode='w')
# Write the results to the text file, joining the items in the list
# as separate lines (= separated by the \n newline character in Unix)
f.write("\n".join(result))
# Finally, close the output file.
f.close()
