from selenium import webdriver
#from bs4 import BeautifulSoup
import time
import requests
import re
import json 
import config
import telebot
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains 
id_list= []
def create_url():
	options = Options()
	options.set_headless()
	assert options.headless 
	browser = Firefox(options=options)
	browser.get('https://www.re-store.ru/discount/')
	time.sleep(10)
	button=[]
	while button == []:

		button = browser.find_elements_by_xpath("//button[@class='r-discount-section__btn-more gray-bttn-normal']")
		for i in button:
			i.click()
			time.sleep(5)
	r_content=browser.page_source
	browser.quit()
	#print(r_content)
	return(r_content)
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'])
def handle_audio(message):
	while True:
		with open('id_list.json', 'r') as filehandle:  
			id_list = json.load(filehandle)
		if message.chat.id not in id_list:
			id_list.append(message.chat.id)
		bot.send_message(message.chat.id,"Я работаю и скоро пришлю тебе что нового на витрине ")
		r_content=create_url()
		with open('sample.json', 'r') as openfile:
		  tova_old = json.load(openfile)
		list_old=[]
		for i in tova_old:
		  list_old.append(i['id'])
		art = re.findall(r'r-discount-table__product-article\">([^<]*)',r_content, re.DOTALL)
		name = re.findall(r'r-discount-table__product-name\">([^<]*)',r_content, re.DOTALL)
		lok = re.findall(r'js-show-store-popup\"[^>]*>([^<]*)',r_content, re.DOTALL)
		price = re.findall(r'r-discount-table__product-price-current\">([^<]*)',r_content, re.DOTALL)
		deff = re.findall(r'r-discount-table__product-description\">([^<]*)',r_content, re.DOTALL)
		tova=[]
		for n,i in enumerate(art):
		  tov={}
		  i=i.strip(' \t\n\r') 
		  tov["id"]=i
		  tov['name']=name[n].strip(' \t\n\r') 
		  tov['lok']=lok[n].strip(' \t\n\r') 
		  tov['price']=price[n].strip(' \t\n\r') 
		  tov['deff']=deff[n].strip(' \t\n\r') 
		  tova.append(tov)
		list_new=[]
		ot=False
		for i in tova:
		  list_new.append(i['id'])
		for n, i in enumerate(list_new):
		  if i not in list_old:
		  	for id_ in id_list:
			  	ot=True
			  	bot.send_message(id_, """ Нашел новый товар 
			    	это {0} стоит {1} 
			    	его дефект это {2}
			    	в {3}
			    	""".format(tova[n]['name'],tova[n]['price'],tova[n]['deff'],tova[n]['lok']))
			  	time.sleep(3)
		json_object = json.dumps(tova)
		with open('id_list.json', 'w') as filehandle:
			json.dump(id_list, filehandle)
		with open("sample.json", "w") as outfile: 
		    outfile.write(json_object) 
		time.sleep(3600)



if __name__ == '__main__':
     bot.polling(none_stop=True)