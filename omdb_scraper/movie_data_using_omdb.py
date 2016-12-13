import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

movie_data = open('movie_data_new.csv','wb')
skipped = open('skipped_urls_imdb_data.txt','wb')
df = pd.read_csv('book_names.csv', names=['Book Name'])
book_names = df['Book Name'].values
skipped_urls = []

def getnum(s):
    return ''.join(s.split(','))

def get_content(book_name, ID, link1, link2, f, a_href):
    try:
        movie_page = requests.get(link1, timeout=30)
        soup = BeautifulSoup(movie_page.content, "lxml")

        budget = ''
        gross = ''
        opening = ''

        li = soup.find_all('div',id='tn15content')
        if(len(li)!=0):
            for row in li:
                #print row
                re_obj = re.search("Budget<\/h5>[\s]*\$(.*?)\s", str(row))
                if(re_obj!=None):
                    budget = getnum(re_obj.group(1))
                re_obj = re.search("Gross<\/h5>[\s]*\$(.*?)\s", str(row))
                if(re_obj!=None):
                    gross = getnum(re_obj.group(1))
                re_obj = re.search("Opening Weekend<\/h5>[\s]*\$(.*?)\s", str(row))
                if(re_obj!=None):
                    opening = getnum(re_obj.group(1))
            
        movie_page = requests.get(link2, timeout=30)
        soup = BeautifulSoup(movie_page.content, "lxml")
        
        releasedate = ''
        
        li = soup.find_all('a',href=a_href)
        if(len(li)!=0):
            for row in li:
                #print row
                re_obj = re.search(">(.*)(USA)", str(row))
                if(re_obj!=None):
                    releasedate = getnum(re_obj.group(1))
                    releasedate = releasedate[:-1].strip()

        #print(book_name+'\t'+ID+'\t'+link1+'\t'+budget+'\t'+gross+'\t'+opening+'\t'+releasedate)
        print(budget+'\t'+gross+'\t'+opening+'\t'+releasedate)
        f.write(book_name+'\t'+ID+'\t'+link1+'\t'+budget+'\t'+gross+'\t'+opening+'\t'+releasedate+'\n')
            
    except Exception as exception:
        skipped_urls.append(ID)
        print(exception)

iter=0

for b in book_names:
    try:
        query = "http://www.omdbapi.com/?t="+b+"&y=&plot=full&r=json"
        res = requests.get(query)
        text = res.json()
        url1 = "http://www.imdb.com/title/" + text['imdbID'] + "/"
        url2 = "http://www.imdb.com/title/" + text['imdbID'] + "/business"
        a_href = "/title/" + text['imdbID'] + "/releaseinfo?ref_=tt_ov_inf"
        iter += 1
        print iter
#         print url1
#         print url2
#         print a_href
        get_content(b, text['imdbID'], url2, url1, movie_data, a_href)
    except Exception as exception:
        skipped.write(b+'\n')
        
    
movie_data.close()

for i in skipped_urls:
    skipped.write(i+'\n')

skipped.close()