import requests
from bs4 import BeautifulSoup
import numpy as np 
import mimetypes
import os
from model import detect
import cv2 
from skimage import io
import pandas as pd 

def get_names(celeb):
	website = "https://en.wikipedia.org/wiki/" + celeb    #diff celebs
	result  = requests.get(website)
	text_result = result.text
	print("Starting to crawl Wiki Pages,..")
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
	print(len(names), "Names found")
	#print(hrefs.shape)
	return hrefs,names
def imgs(href):               #functn to get the images links
	imgs = []
	lock=1
	img_count = 0
	flag =0

	img_search = requests.get(href)
	img_soup = BeautifulSoup(img_search.content,"html.parser")
	for img_link in img_soup.findAll('img'):
		
		while(img_link.get('height')):

			if int(img_link.get('height')) > 100:
				img_src = 'https:' + img_link.get('src')
				imgs.append(img_src)
				img_count = img_count+1
			break

	if img_count==0:
		print("No Viable Images on WIKI")
		flag = 1
	else:
		print(img_count," Image(s) Found")
	#print(lock)
	imgs = np.asarray(imgs)
	#print(imgs.shape)
	return imgs, flag
def file_write(x):                                     #fnctn to write the image files in a local path
	links,name = get_names(x)
	no_images=[]
	total = 1

	for i in range(len(name)):
		print(name[i],":")
		locs,flag = imgs(links[i])
		if flag==0:
			p = "C:\\Users\\Asus\\Desktop\\Images\\" + name[i] +"\\"
			os.mkdir(p)
			for j in range(len(locs)):
				r = requests.get(locs[j])
				#print (locs[j])
				img = io.imread(locs[j])
				img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #scikit image reads in bgr

				model = detect.model()							#importing model
				result = detect.predict(img,model)	
				#print(result)

				if 'person' in result:
					typ = r.headers['content-type']
					ext = mimetypes.guess_extension(typ)
					p = p +str(total).zfill(4)+ext
					file = open(p,'wb')
					file.write(r.content)
					file.close()
					#print(total)
					total = total +1
				else:
					print("Bad Image Found, Ignoring")
		else:
			print("Noted that Image not available, No folder created")
			no_images.append(name[i])
	#print(no_images)
	return name,no_images
celebs = ['List_of_Indian_film_actors','List_of_Indian_film_actresses','List_of_Indian_film_directors']
names = []
clean = []
for i in range(len(celebs)):
	x = celebs[i]
	a=file_write(x)
	names.extend(a[0])
	clean.extend(a[1])
	pic_avail = []
	for i in range(len(names)):
		if names[i] in clean:
			pic_avail.append('Pic not available')
		else:
			pic_avail.append('Pics added')
data = np.array([names,pic_avail])                                                      
data = np.transpose(data)
df= pd.DataFrame({'Name': data[:,0], 'Picture Availability': data[:,1]})                    #creating the dataframe
#print(df)
df.to_csv("Results.csv")