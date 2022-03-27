# -*- coding: utf-8 -*-
"""
Parse a "forum page" of wine forum lapassionduvin.com
Created on June 06, 2020

@author: E. Cabrol
"""
import re
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import random
from LPV_parse_subject_final import parse_subject

# not generic ... yet

database = './DB_LPV'
region='bordeaux'
forum_page = 'https://www.lapassionduvin.com/'+region
local_forum_dir = database+"/"+region
subjects_file = local_forum_dir+"/liste_sujets.txt"

list_existing_ids=[]

# Create an empty file if it does not exist, else parse it
if not os.path.exists(subjects_file):
    with open(subjects_file, 'w') as f: 
        pass
else:
    with open(subjects_file, 'r') as f:
        for line in f.readlines():
            regexp = re.search(r'(\d+)\s([A-Za-z0-9-]+)',line)
            if regexp:
                list_existing_ids.append(int(regexp.group(1)))

    
# RETRIEVE DISTANT INFO

#  user_agent required to avoid HTTPError: Forbidden
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent} 
request = urllib.request.Request(forum_page,None,headers) #The assembled request
response = urllib.request.urlopen(request)
content = response.read()

soup = BeautifulSoup(content,"lxml")

# myPages = soup.find_all("ul",class_="pagination")
# myLine = soup.find("ul",class_="pagination")

pagination = soup.find("ul",class_="pagination")
lastStartNumber=0
for link in pagination.find_all("a", class_="hasTooltip"):
    address = link.get('href') 
    regexp = re.search(r"\d+$",address)
    result = regexp.group()
    if int(result)>lastStartNumber:
        lastStartNumber=int(result)
upperLimit = lastStartNumber+1 # to cope with Python range behavior

# EXTRACT SUBJECTS OF ALL PAGES

# Get relative paths to subjects
# example : "/vins-deurope/35474-zorah-wines-armenie"

# list_ids_found = []
# list_subjects_found = []
list_found = {}

for i in range (0,upperLimit,30):
    if i != 0:
        time.sleep(random.uniform(5,8))
        print('Parsing page',i)
        next_page = forum_page+'?start='+str(i)
        request = urllib.request.Request(next_page,None,headers) 
        response = urllib.request.urlopen(request)
        content = response.read()
        soup = BeautifulSoup(content,"lxml")
    
    myPaths = soup.find_all(lambda tag: tag.name == 'tr' and tag.get('class') == ['category'])
    
    for item in myPaths:
        regexp = re.search(r"/(\d+)-([A-Za-z0-9-]+)",item.a.get('href'))
        if regexp:
            list_found[int(regexp.group(1))] = regexp.group(2)
        else:
            continue

# PARSE ALL SUBJECTS FOUND
    
for id_subject in list_found.keys():
    
    if id_subject not in list_existing_ids:
        with open(subjects_file,'a') as f:
            f.write(f"{id_subject} {list_found[id_subject]}\n")

    parse_subject(forum_page+'/'+str(id_subject)+'-'+list_found[id_subject])

