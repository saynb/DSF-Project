from bs4 import BeautifulSoup
import requests


book_links = open('book_links.txt','w')

def clean_text(text):
    return ' '.join(text.split())

def get_content(link, f):
    movie_page = requests.get(link)
    soup = BeautifulSoup(movie_page.content, "lxml")

    for row in soup.find_all('a',class_='bookTitle'):
        f.write('https://www.goodreads.com'+row.get('href')+'\n')

link = "https://www.goodreads.com/list/show/429.The_BOOK_was_BETTER_than_the_MOVIE?page="

for i in range(1,15):
    link1 = link+str(i)
    get_content(link1,book_links)

link = "https://www.goodreads.com/list/show/104.The_MOVIE_was_BETTER_than_the_BOOK?page="

for i in range(1,10):
    link1 = link+str(i)
    get_content(link1,book_links)

book_links.close()
