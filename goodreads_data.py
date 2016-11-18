import matplotlib as mlp
import scipy
import numpy as np
import sympy
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from sklearn.preprocessing import scale
from scipy.stats.stats import spearmanr 
from sklearn.linear_model import LinearRegression
from sklearn import cross_validation
from sklearn import metrics
import scipy.sparse as sps
import math
from bs4 import BeautifulSoup
import requests
import re
import fileinput
import os,sys
# import sys




def clean_text(text):
    """ Removes white-spaces before, after, and between characters

    :param text: the string to remove clean
    :return: a "cleaned" string with no more than one white space between
    characters
    """
    return ' '.join(text.split())

df_book = pd.DataFrame(data={'Book Name' : [],'Author' : [], 'Awards List' : [], 'Genres' : [], 'Characters' : []})

# reload(sys)
# sys.setdefaultencoding('utf-8')

#TODO :
# 1. Clean awards to trim ..more , ..less
# 2. Delimit by commas 
# 3. Make a pandas dataframe and put into it the data for the book

    
# with open('book_was_better.txt','r') as book_better:
#     for url_first in book_better:
i = 0
fin = fileinput.input(files=('book_was_better.txt', 'movie_was_better.txt'),mode='r')
for url_first in fin:

# if 1:
#         url_first  = book_better.readline()
    try:
#        if (i>940):
            book_page = requests.get(url_first)

            # Strain the items from the book page
            soup = BeautifulSoup(book_page.content,"lxml")
            print i
            #Book Name

            book_name = soup.find_all('h1',attrs={"class":'bookTitle'})
            book_name = book_name[0].text
            book_name = clean_text(book_name)
            print book_name

            #Author
            author = soup.find_all('a',attrs={"class":'authorName'})[0].text

            #Awards
            awards_string = ""
            for row in soup.find_all('div',attrs={"class":'infoBoxRowItem',"itemprop":'awards'}):
                    awards_string = row.text

            #Genres
            genre_list = []
            for row in soup.find_all('a',attrs={"class":'actionLinkLite bookPageGenreLink'}):
                    genre_list.append(row.text)

            #Characters
            character_list = []
            for row in soup.find_all('a', {'href': re.compile(r'/characters')}):
                character_list.append(row.text)

            #Other editions
            other_editions = soup.find_all('a', {'href': re.compile(r'/work/editions/')})[1].text
            m = re.search('.*\((.*)\)', other_editions)
            if m:
                other_editions = int(m.group(1))

            #Getting number of votes for [5 4 3 2 1] star ratings        
            script_text = []
            for row in soup.find_all('script',attrs={'type':'text/javascript+protovis'}):
                script_text.append(str(row))
            if len(script_text) >0:
                m = re.search('.*renderRatingGraph\(\[(.*)\]\).*', script_text[0])
            if m:
                rating_values_str = m.group(1)
            rating_values_list = [ int(x) for x in rating_values_str.split(",") ]

            #Average star rating
            star = soup.find_all('span',attrs={"class":'average', "itemprop":"ratingValue"})[0].text
            print star

            #Pages
            pages = soup.find_all('span',attrs={"itemprop":"numberOfPages"})[0].text
            print pages
            
            #publish_date
            publish_date = soup.find_all('nobr',attrs={"class":'greyText'})
            if len(publish_date) > 0:
                publish_date = publish_date[0].text
                m = re.search('\(.*d\s(.*)\)', publish_date)
                if m:
                    publish_date = m.group(1)
            else: publish_date = ""
            print publish_date
            
            #num_reviews
            num_reviews = soup.find_all('span',attrs={"class":'value-title'})[0].text
            m = re.search('(.*?)\s', num_reviews)
            if m:
                num_reviews = int(m.group(1).replace(',', ''))
                
            print ("\nnum_reviews = ",num_reviews)


            df = pd.DataFrame({'Book Name':book_name, 'Author':author, 'Awards List':awards_string, 
                               'Genres':[genre_list], 'Characters':[character_list], 'Other editions':other_editions,
                              'Star votes':[rating_values_list], 'Stars':star, 'Num_reviews':num_reviews,
                              'publish_date':publish_date, 'Pages':pages})
            df_book = df_book.append(df,ignore_index=True)


            if (i%20 == 0):
                df_book.index += (i-19)
                df_book.to_csv('goodreads_data_new.csv', mode='a', header=(True if i<21 else False), encoding="utf-8")
                df_book = pd.DataFrame()
            i +=1
            
        
                
    except Exception as exception:
        
#                 df.to_csv('skipped.csv', mode='a', header=False, ignore_index=True, encoding="utf-8")
            f = open('skipped_files', 'a')
            f.write(url_first + " "+type(exception).__name__+"\n")
            f.close()
            print type(exception).__name__
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            i +=1
            


fin.close()
df_book

