PACKAGES REQUIRED: selenium, chrome-driver, os, time, shutil, datetime, numpy

This python script simulates clicking behavior to reserve the 18:15 slot on Mondays, Tuesdays, Thursdays and Fridays at Tilburg University's sports center. All of this is done through locating the XPath of areas on the website that are to be clicked. 

This script needs to be used with Windows Task Scheduler. This requires writing a .bat file that runs the script and then running the .bat file with Windows Task Scheduler. The program books a spot in the next week on the day the program was run. E.g: if the program was run on Monday 2 May, it would book a spot on Monday 9 May at 18:15. 

**UPDATE: The sports center's website has undergone a massive change. This script needs to be modified in order for it to work again (new XPaths need to be specified).