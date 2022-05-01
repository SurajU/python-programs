PACKAGES REQUIRED: selenium, pandas, check-chromedriver, shutil

The function "shareWorkingHospitals.py" automates the collection of specialist information from "https://www.agbcode.nl/Webzoeker/Zoeken". It does this by first imitating clicking behavior (done through a chrome webdriver) and then reading and converting all information on a website page into distinct tables (done through pandas.read_html). 

In a first stage, this script gets basic info on all specialists working in hospitals in my data. This is outputted to the "allSpecialists.xlsx" file. It then cycles through each name in the "allSpecialists.xlsx" file and gets detailed information on where they work, what they do, whether they're salaried or self-employed, etc. The output of this process in stored in "whereProvidersWork2.xlsx". (The file "whereProvidersWork2.xlsx" in this repository contains the output I used for my own research).

This is done for both hospitals and independent treatment centers (ZBCs).

Small modifications to the script may be required given that it was used in 2019.

