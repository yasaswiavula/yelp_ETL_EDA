#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import pandas as pd

yelp_url = "https://www.yelp.com"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
default_webpage="https://www.yelp.com/search?find_desc=Restaurants&find_loc=Mount+Pleasant%2C+MI+48858&start="
page_number=0
#initialize my_data as list
my_data = []

def yelpscraping(webpage, page_number):
    next_page = webpage + str(page_number)
    response= requests.get(str(next_page))
    soup=BeautifulSoup(response.content,'lxml') 
                           
    for item in soup.select('[class*=container]'):
        try:
            if item.find("h3"):
                h3_data= item.find("h3").get_text().split(".")[1]
                reviews=item.select('[class*=css-chan6m]')[0].get_text().split(" ")[0].split("(")[1]
                rating=item.select('[aria-label*=rating]')[0]['aria-label'].split(" ")[0]
                pricerange= item.select('[class*=priceRange]')[0].get_text()
                link=yelp_url+str(item.find("a").get('href'))
                description=item.select('[class*=css-16lklrv]')[0].get_text().strip("“")

                #append each coloumn data scraped to my_data 
                my_data.append({"Name": h3_data, "Review_count": reviews, "Rating": rating, "Pricerange": pricerange , "Link": link, "Top_comment": description})
        except Exception as e:
            #raise e
            print("")
    
#Generating the next page url
while(page_number < 120):
    page_number = page_number + 10
    yelpscraping(default_webpage, page_number)
    #calling the function with relevant parameters

df = pd.DataFrame(my_data)
header=['Name','Review_count','Rating','Pricerange','Link','Top_comment']
df.to_csv('restaurents_data.csv',columns=header,index=False)






