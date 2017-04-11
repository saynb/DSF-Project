from bs4 import BeautifulSoup
import requests
import io
import codecs

f = codecs.open('books_becoming_movies_2016.txt','wb',encoding='utf-8')

def clean_text(text):
    return ' '.join(text.split())

def get_content(link, f):
    movie_page = requests.get(link)
    soup = BeautifulSoup(movie_page.content, "lxml")

    for row in soup.find_all('a',class_='bookTitle'):
    	tt = row.find('span').text
        f.write('https://www.goodreads.com'+row.get('href')+'\t'+tt+'\n')

link = "https://www.goodreads.com/list/show/86204.Books_Becoming_Movies_in_2016?page="

for i in xrange(1,3):
    link1 = link+str(i)
    get_content(link1,f)

f.close()
