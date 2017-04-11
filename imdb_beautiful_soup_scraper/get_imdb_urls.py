from bs4 import BeautifulSoup
import requests
import io
import time

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

book_better = io.open('book_was_better_names.txt','r')
movie_better = io.open('movie_was_better_names.txt','r')

imdb_urls = open('imdb_urls.txt','wb')

def get_content(link, f):
	movie_page = requests.get(link)
	soup = BeautifulSoup(movie_page.content, "lxml")

	for row in soup.find_all('td',class_='result_text'):
		try:
			f.write('www.imdb.com'+row.find('a').get('href')+'\n')
			print(iter)
		except:
			print("Go Ahead")
		break


link = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='

iter=0
for name in book_better:
	iter = iter+1
	if(is_ascii(name)):
		link1 = link+name
		get_content(link1, imdb_urls)
		if(iter%100==0):
			time.sleep(10)

imdb_urls.close()