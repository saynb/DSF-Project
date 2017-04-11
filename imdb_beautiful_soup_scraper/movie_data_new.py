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

movie_data = open('movie_data_new.csv','wb')

skipped = open('skipped_urls_imdb_data.txt','wb')
skipped_urls = []

def get_content(link, f):
	try:
		movie_page = requests.get(link, timeout=30)
		soup = BeautifulSoup(movie_page.content, "lxml")

		budget = ''
		gross = ''
		opening = ''

		li = soup.find_all('div',id='tn15content')
		if(len(li)!=0):
			for row in li:
				re_obj = re.search("Budget<\/h5>[\s]*\$(.*?)\s", str(row))
				if(re_obj!=None):
					budget = getnum(re_obj.group(1))
				re_obj = re.search("Gross<\/h5>[\s]*\$(.*?)\s", str(row))
				if(re_obj!=None):
					gross = getnum(re_obj.group(1))
				re_obj = re.search("Opening Weekend<\/h5>[\s]*\$(.*?)\s", str(row))
				if(re_obj!=None):
					opening = getnum(re_obj.group(1))
		
			print(budget+','+gross+','+opening)
			f.write(link+','+budget+','+gross+','+opening+'\n')
									
	except Exception as exception:
		skipped_urls.append(link)
		print(exception)

iter=0
for line in movie_file.split("\n"):
	link = 'http://' + line.split('\t<>\t')[1]
	re_obj = re.search("(.*)[?]", link)
	link = re_obj.group(1)+'business?ref_=tt_dt_bus'
	iter = iter+1
	get_content(link, movie_data)
	print(iter)

movie_data.close()


for i in skipped_urls:
	skipped.write(i+'\n')

skipped.close()