import os
import re
import glob
from zipfile import ZipFile

documents = glob.glob('D:/Docs/*.docx')


#%%

total_pages = 0

for file_name in documents:

    print(file_name)
    try:
        zip = ZipFile(file_name, 'r') 
    except:
        print("... is not a zip file")
    else:
        data=zip.read('docProps/app.xml').decode('utf-8')
        nb_pages = int((re.search(r"<Pages>(\d+)</Pages>",data)).group(1))
        print("... has "+str(nb_pages)+" pages")
        total_pages += nb_pages
            
    print()


print("Total number of pages = "+str(total_pages))
