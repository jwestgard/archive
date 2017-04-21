A generic preprocessor for Hippo DB projects.

The goal of this project is to provide a single preprocessing script that applies transformations to an input CSV based solely on rules embodied in a YAML configuration file.

The YAML file is a two-layer nested dictionary where the top-level keys are the names of the output columns and the values are additional sets of key-value pairs representing the following elements of each transformation "rule":

1. source: the input column (required)
2. operation: the type of transformation to apply to the input data (optional, defaults to "copy"); options include: 
    * copy: copy source to output
    * replace: substitute 'replacement' text for 'match' text
    * concatenate: create a new string via string formatting
    * split: create a list from a string based on a delimiter
3. match: the portion of the source data to match (optional)
4. replace: the text or pattern to substitute for the match
5. strip: extraneous characters to remove from either end of the final string, or in cases of a split operation, from each element of the final list.

The input is read from stdin, and output written to stdout. Config files should be placed in the "config" directory.  
