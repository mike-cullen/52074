#!/usr/bin/env python3.8

import re
import time
import pickle
from bs4 import BeautifulSoup
from urllib.request import urlopen

def remove_regex_pattern_from_list(pattern, list): 
    list = [re.sub(pattern, '', i) for i in list] 
    return list

dictionary_exists = False

# try to grab the saved state dictionary, else fail message:
try:
    with open("mySavedDict.txt", "rb") as myFile:
       pulled_dic = pickle.load(myFile)
       dictionary_exists = True 
except IOError:
    print("No saved dict file retrievable, please create one first!")
    dictionary_exists = False

# if dictionary_exists:
    # print(pulled_dic['Schneeberg'])

page = urlopen("https://www.erzgebirgskreis.de/index.php?id=1126")
str_page = page.read()
soup = BeautifulSoup(str_page, "lxml")

mytable = soup.findAll("table", {"class": "ce-table"})

# adds stored village information from the <table> element
# as elements to this collection list:
collection = []
for x in mytable:
    collection.append(str(x))

# make new string, convert the collection list to a string, then
# clean up the string
str1 = ""
str1 = str1.join(collection)
str1 = str1.replace('\n', ' ').replace('\r', '').replace(' ', '')
str1 = re.sub(r'<.+?>', '', str1)
str1 = str1.replace('.', '')
str1 = str1.replace('/Erzgebirge', '').replace('/Erzgeb', '')
str1 = str1.replace('-Buchholz', 'buchholz').replace('-BadSchlema', 'badschlema')
str1 = str1[str1.find('Vortag') + len('Vortag'): ]
str1 = str1.replace('Wiesenbad2-', 'wiesenbad2-')

# after string is 'cleaned up' convert back to list:
#splits on capital letters, be careful! :
list1 = re.sub( r"([A-Z])", r" \1", str1).split()
# print(list1)
digit_regex = '[0-9]'
letter_regex = '[a-zA-Z|äöüÄÖÜß]'

# removes all digits, plus and minus symbols, from list1:
# list2 will contain only the village names:
pat = '[0-9]|\+|-'
list2 = remove_regex_pattern_from_list(pat, list1)

# removes all letters including german letters, from list1:
# list3 will only contain the values for corona cases:
pat2 = '[a-zA-Z|äöüÄÖÜß]'
list3 = remove_regex_pattern_from_list(pat2, list1)

# merges two lists into a dictionary
dic = dict(zip(list2, list3))
# print(dic)

# sets variable to current date:
# todaysdate = time.strftime("%d-%m-%Y-%H%M%S")
todaysdate = time.strftime("%d-%m-%Y-%H"+":00")

if dictionary_exists:
    print(pulled_dic['Schneeberg'])
    # print(type(pulled_dic))

# builds dictionary for the first time:
if not dictionary_exists:
    for key, value in dic.items():
        if value[-1] == '-':
            dic[key] = { todaysdate: { 'new': '-', 'total': value[ : -1] } }
        if re.match(digit_regex, value[-1]) is not None:
            dic[key] = { todaysdate: { 'new': value[ value.find('+')+1 : ], 'total': value[ : value.find('+') :  ]  }  }
    print("New dictionary created!")

# adds daily values to existing dict (das heisst - pulled_dic)
if dictionary_exists:
    for key, value in dic.items():
        if value[-1] == '-':
            pulled_dic[key][todaysdate] = { 'new': '-', 'total': value[ : -1] }
        if re.match(digit_regex, value[-1]) is not None:
            pulled_dic[key][todaysdate] = { 'new': value[ value.find('+')+1 : ], 'total': value[ : value.find('+') :  ]  }


if dictionary_exists:
    print(pulled_dic['Schneeberg'])
    # print(type(pulled_dic))

print('dictionary_exists =', dictionary_exists)

# current working save file, leave here until the dictionary is
# fully functional:
timestr = time.strftime("%d-%m-%Y-%H%M%S")
with open(timestr + "-corona-tabelle.txt", "w") as file:
    file.write(str(list1))

# save the current dictionary, to a file:
if dictionary_exists:
    with open("mySavedDict.txt", "wb") as myFile:
        pickle.dump(pulled_dic, myFile)

# or save dictionary for the first time:
if not dictionary_exists:
    with open("mySavedDict.txt", "wb") as myFile:
        pickle.dump(dic, myFile)

