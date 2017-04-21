pid-extractor
=============

Script to read text file and extract a particular string (in this case PIDs for Digital Collections objects) from it.

1. The script asks the user to specify an input file, and reads it into memory as a list of strings (each line a separate item in the list).
1. It then iterates through the list, searching for matches to '(umd:' followed by any number of digits, followed by a semicolon.
1. If it finds a match, it appends the substring between the inner parentheses in the original search (= 'umd:0000') as an item in the list 'results'.
1. After iterating through the original input, it stores the results list as a text file, with one PID on each line.
