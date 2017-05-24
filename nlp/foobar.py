#coding=utf-8

import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import time
import sys
import io


def get_pages():
	my_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
	my_Accept_Encoding = "deflate, sdch"
	my_Accept_Language = "zh-CN,zh;q=0.8"
	my_Upgrade_Insecure_Requests = "1"
	my_User_Agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"

	headers = {"acceptt":my_accept,  'Accept-Encoding':my_Accept_Encoding, 'Accept-Language':my_Accept_Language,"Upgrade-Insecure-Requests":my_Upgrade_Insecure_Requests, "User-Agent":my_User_Agent}
	req = urllib.request.Request("http://1024.97luhi.com/pw/thread.php?fid=14", None, headers)
	

	print("reading thread list\n")
	try:
		resp = urllib.request.urlopen(req, timeout=10)
	except:
		print("open web page error!!stop!!")
		exit()
	
	html = resp.read().decode("utf-8", "ignore")
	
	soup = BeautifulSoup(html,"html.parser")
	#for h3 in soup.h3:
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
	#print(soup)

	trs = soup.find_all(id=re.compile("^a_ajax"))
	link_re = re.compile("^htm_")
	for tr in trs:
		page_link = tr["href"]
		#print(page_link)
		if link_re.match(page_link):
			print(page_link)
			get_pic(page_link)
			#return






def get_pic(page_link):
	total_url = "http://1024.97luhi.com/pw/" + page_link
	print(total_url)
	thread_id=re.search("[0-9]+.html$", page_link).group(0)
	thread_id=re.search("[0-9]+", thread_id).group(0)

	my_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
	my_Accept_Encoding = "deflate, sdch"
	my_Accept_Language = "zh-CN,zh;q=0.8"
	my_Upgrade_Insecure_Requests = "1"
	my_User_Agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36"

	headers = {"acceptt":my_accept,  'Accept-Encoding':my_Accept_Encoding, 'Accept-Language':my_Accept_Language,"Upgrade-Insecure-Requests":my_Upgrade_Insecure_Requests, "User-Agent":my_User_Agent}
	req = urllib.request.Request(total_url, None, headers)
	

	print("reading thread detail\n")
	try:
		resp = urllib.request.urlopen(req, timeout=10)
	except:
		print("open web page error!!stop!!")
		exit()
	
	html =resp.read().decode("utf-8", "ignore")
	#print(html)
	#exit()
	
	#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
	print("start get pic\n")
	soup = BeautifulSoup(html,"html.parser")
	images = soup.find(id="read_tpc").find_all("img")

	j = 1
	for image in images:
		image_url = image.get("src")
		print("DOWNLOADING:" + image_url)
		try:
			file_request = urllib.request.Request(image_url, None, headers) 
			file_response = urllib.request.urlopen(file_request, timeout=10)
			f = open(thread_id + "_" + str(j) + ".jpg", "wb")
			f.write(file_response.read())
			f.close()
		except:
			print("ERROR:" + image_url)
		j = j + 1

if __name__ == "__main__":
	#get_pic()
	get_pages()



