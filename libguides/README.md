# libguides
Files for web scraping and problem identification exercises for the UMD Libraries Coding Workshop.

## Starter Files

1. urls.txt: the urls of each of UMD's libguides
2. guides.html: an HTML list for convenient access to the live pages
3. 280 files in guides/: HTML downloaded from each of the UMD pages

The command for re-downloading the files in guides/ would be:
```
wget --input urls.txt --directory-prefix guides
```
Notes: You would need to create the 'guides' directory first; you can use a -E flag to append '.html' to the downloaded filename.

## Project Goals
The following requirements are based on the infomration that has been circulated about the required changes. It may or may not be possible to facilitate all of these tasks through scripting:
- To facilitate link correction, identify all 'non-AAA' database links, and (optionally) locate the AAA equivalent for any non-AAA links that are found;
- Remove all references, links, and screenshots that refer to Research Port, Citation Linker, and the old WorldCat interface (update links to the last of these with links to the WorldCat discovery interface);
- Check that physical addresses follow the new format: http://maps.umd.edu/addressing;
- Check for inconsistencies in database names ( this would involve assembling a list of canonical database names and comparing link text to those names);
- All of the preceding changes should, ideally, be assembled into a report indicating the url/page (and line?) for each required change, since it will not be possible to write changes directly back to the libguides website.
