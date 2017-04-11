from bs4 import BeautifulSoup
import requests
import io


book_names = io.open('book_names.txt','w',encoding='utf8')

def clean_text(text):
    return ' '.join(text.split())

def get_content(link, f):
    movie_page = requests.get(link)
    soup = BeautifulSoup(movie_page.content, "lxml")

    for row in soup.find_all('a',class_='bookTitle'):
        f.write(row.find('span').text+'\n')

link = "https://www.goodreads.com/list/show/429.The_BOOK_was_BETTER_than_the_MOVIE?page="

for i in range(1,15):
    link1 = link+str(i)
    get_content(link1,book_names)

link = "https://www.goodreads.com/list/show/104.The_MOVIE_was_BETTER_than_the_BOOK?page="

for i in range(1,10):
    link1 = link+str(i)
    get_content(link1,book_names)

book_names.close()
