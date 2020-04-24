import requests
from bs4 import BeautifulSoup
import numpy as np 
import mimetypes
import os
def names():
	website = "https://en.wikipedia.org/wiki/List_of_Indian_film_actors"
	result  = requests.get(website)
	text_result = result.text
	print("hey")
	#if result.status_code==200:
	soup = BeautifulSoup(result.content,"html.parser")
	#else:
	#	print("parse error !")
	names = []
	hrefs= []
	data = soup.findAll('div',{'class':'div-col columns column-width'})
	for div in data:	
		links = div.findAll('a')
		for link in links:
			href = 'https://en.wikipedia.org/' + link.get('href')
			hrefs.append(href)
			title = link.get('title')
			if(str(link.string) in str(title)):
			#print("sup")
				name = link.string
				names.append(name)
				#print(name)
	names = np.asarray(names)
	hrefs = np.asarray(hrefs)
	print(names.shape)
	return hrefs
def imgs():
	imgs = []
	i=1
	links = names()
	for href in links:
		img_search = requests.get(href)
		img_soup = BeautifulSoup(img_search.content,"html.parser")
		for img_link in img_soup.findAll('img'):

			while(img_link.get('height')):
				if int(img_link.get('height')) > 100:
					img_src = 'https:' + img_link.get('src')
					imgs.append(img_src)
				break

		print(i)
		i=i+1
		#if i == 3:
		#	break
	imgs = np.asarray(imgs)
	print(imgs.shape)
	return imgs
def file_write():
	locs = imgs()
	total = 1

	for i in range(len(locs)):
		r = requests.get(locs[i])
		typ = r.headers['content-type']
		ext = mimetypes.guess_extension(typ)
		p = "C:\\Users\\Asus\\Desktop\\Images\\"+str(total).zfill(4)+ext
		file = open(p,'wb')
		file.write(r.content)
		file.close()
		#print(total)
		total = total +1

file_write()