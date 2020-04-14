# erz-case-collector

Scrapes COVID-19 cases from:
https://www.erzgebirgskreis.de/index.php?id=1126

Sorts cases by area ('Ort'), stores area names, new cases and updated cases in a dictionary of dictionaries.

Saves the dictionary using pickle. Pickle is awesome!

Required imports:
re
time
pickle
bs4 / BeautifulSoup
urllib.request / urlopen

A work in progress. If you have any feedback or suggestions, let me know. :)

-mike cullen
