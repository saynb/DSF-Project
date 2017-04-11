from bs4 import BeautifulSoup
import requests
import io


book_better = io.open('book_was_better_names.txt','w',encoding='utf8')
movie_better = io.open('movie_was_better_names.txt','w',encoding='utf8')

def clean_text(text):
    return ' '.join(text.split())

def get_content(link, f):
    movie_page = requests.get(link)
    soup = BeautifulSoup(movie_page.content, "lxml")

    for row in soup.find_all('a',class_='bookTitle'):
        f.write(row.find('span').text+'\n')

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