# Media Cleanser

A very simple python script to strip clutters readability web page for people with a handicap situation.

This script is to be used on a downloaded [mozilla's firefox readable HTML page](https://github.com/mozilla/readability). The changes are made infile.

A text-to-speech can be used without earing debiltating cluters.

This script depends on :

+ [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup)
+ [lxml](https://lxml.de/)

This is, and will be, a work in progress. This script was originally created to clean **Montreal Gazette's readable webpages** of debilitating clutter.

**What's next (future features):**

- an URL could be provided, and the script would generate an uncluttered readable html page and launch it in your default browser ;
- an output file location could be specified ;
- Install pipx and install this script from the root directory like so ``` pipx install . ```.

