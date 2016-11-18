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

with io.open("imdb_urls_all.txt", "r", encoding="utf-8") as my_file:
     movie_file = my_file.read() 

movie_data = open('movie_data.csv','wb')

skipped = open('skipped_urls_imdb_data.txt','wb')
skipped_urls = []

def get_content(link, f):
	try:
		movie_page = requests.get(link, timeout=30)
		soup = BeautifulSoup(movie_page.content, "lxml")

		budget = ''
		gross = ''

		for row in soup.find_all('div',class_='txt-block'):
			if 'Budget' in row.text:
				print clean_text(row.text)
				re_obj = re.search(".*\$(.*?)\s.*\)", clean_text(row.text.encode('utf8')))
				budget = getnum(re_obj.group(1))
			if 'Gross' in row.text:
				print clean_text(row.text)
				re_obj = re.search(".*\$(.*?)\s.*\)", clean_text(row.text.encode('utf8')))
				gross = getnum(re_obj.group(1))

		f.write(link+','+budget+','+gross+'\n')
								
	except requests.exceptions.Timeout:
		skipped_urls.append(link)
	except UnicodeEncodeError:
		skipped_urls.append(link)
	except AttributeError:
		skipped_urls.append(link)
	except:
		skipped_urls.append(link)

iter=0
for line in movie_file.split("\n"):
	re_obj = re.search(",www(.*)", line)
	link = 'http://www'+re_obj.group(1)
	iter = iter+1
	get_content(link, movie_data)
	print(iter)

movie_data.close()


for i in skipped_urls:
	skipped.write(i+'\n')

skipped.close()