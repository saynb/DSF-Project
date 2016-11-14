from bs4 import BeautifulSoup
import requests


book_better = open('book_was_better.txt','wb')
movie_better = open('movie_was_better.txt','wb')

def clean_text(text):
    return ' '.join(text.split())

def get_content(link, f):
    movie_page = requests.get(link)
    soup = BeautifulSoup(movie_page.content, "lxml")

    for row in soup.find_all('a',class_='bookTitle'):
        f.write('https://www.goodreads.com'+row.get('href')+'\n')

link = "https://www.goodreads.com/list/show/429.The_BOOK_was_BETTER_than_the_MOVIE?page="

for i in xrange(1,15):
    link1 = link+str(i)
    get_content(link1,book_better)

link = "https://www.goodreads.com/list/show/104.The_MOVIE_was_BETTER_than_the_BOOK?page="

for i in xrange(1,10):
    link1 = link+str(i)
    get_content(link1,movie_better)

book_better.close()
movie_better.close()
