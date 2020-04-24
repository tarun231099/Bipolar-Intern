import requests
from bs4 import BeautifulSoup
import numpy as np 
import mimetypes
import os
from model import detect
import cv2 
from skimage import io

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
			
			title = link.get('title')
			if(str(link.string) in str(title)):
			#print("sup")
				name = link.string
				names.append(name)
				href = 'https://en.wikipedia.org/' + link.get('href')
				hrefs.append(href)
				#print(name)
	names = np.asarray(names)
	hrefs = np.asarray(hrefs)
	print(names.shape)
	print(hrefs.shape)
	return hrefs,names
def imgs(href):
	imgs = []
	lock=1
	#links,name = names()
	#for href in links:

	img_search = requests.get(href)
	img_soup = BeautifulSoup(img_search.content,"html.parser")
	for img_link in img_soup.findAll('img'):

		while(img_link.get('height')):

			if int(img_link.get('height')) > 100:
				img_src = 'https:' + img_link.get('src')
				imgs.append(img_src)
			break

	print(lock)
	#lock=lock+1
	#if lock == 2:
	#break
	imgs = np.asarray(imgs)
	print(imgs.shape)
	return imgs
def file_write():
	links,name = names()
	
	total = 1

	for i in range(10):
		locs = imgs(links[i])
		p = "C:\\Users\\Asus\\Desktop\\Images\\" + name[i] +"\\"
		os.mkdir(p)
		for j in range(len(locs)):
			r = requests.get(locs[j])
			print (locs[j])
			img = io.imread(locs[j])
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #scikit image reads in bgr

			model = detect.model()							#importing model
			result = detect.predict(img,model)	
			print(result)

			if 'person' in result:
				typ = r.headers['content-type']
				ext = mimetypes.guess_extension(typ)
				p = p +str(total).zfill(4)+ext
				file = open(p,'wb')
				file.write(r.content)
				file.close()
				print(total)
				total = total +1
			else:
				print("Bad Image Found, Ignoring")

file_write()