from bs4 import BeautifulSoup
import requests
import io
import time
import re

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def clean_text(text):
    return ' '.join(text.split())

def getnum(s):
	return ''.join(s.split(','))

with io.open("imdb_urls_new.txt", "r", encoding="utf-8") as my_file:
     movie_file = my_file.read() 

movie_data = open('movie_data_releasedate.csv','wb')

skipped = open('skipped_urls_imdb_data.txt','wb')
skipped_urls = []

def get_content(link, f, a_href):
	try:
		movie_page = requests.get(link, timeout=30)
		soup = BeautifulSoup(movie_page.content, "lxml")
		print a_href
		li = soup.find_all('a',href=a_href)
		if(len(li)!=0):
			for row in li:
				releasedate = ''
				print row
				re_obj = re.search(">(.*)(USA)", str(row))
				if(re_obj!=None):
					releasedate = getnum(re_obj.group(1))
					releasedate = releasedate[:-1].strip()

			print(releasedate)
			f.write(link+','+releasedate+'\n')								
	except Exception as exception:
		skipped_urls.append(link)
		print(exception)

iter=0
for line in movie_file.split("\n"):
	link = 'http://' + line.split('\t<>\t')[1]
	re_obj = re.search("(.*)[?]", link)
	a_href = re_obj.group(1)+'releaseinfo?ref_=tt_ov_inf'
	a_href = a_href[19:]
	iter = iter+1
	get_content(link, movie_data, a_href)
	print(iter)

movie_data.close()


for i in skipped_urls:
	skipped.write(i+'\n')

skipped.close()