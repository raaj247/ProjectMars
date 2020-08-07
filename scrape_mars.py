#Imports
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
from flask import Flask, render_template
import requests
from splinter import Browser
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #Scrape the NASA Mars News Site
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(7)

# # HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    news_title=soup.find_all('div', class_= 'content_title')
    news_title= soup.find_all('div', class_= 'content_title')[1].text
# Retrieve elements that containnews detail information
    news_p =soup.find ('div', class_='article_teaser_body').text
#Print news tile and details
#print("News Title = "+news_title)
#print("--------------------------------------")
#print("News = "+news_p)
## JPL Mars Space Images - Featured Image
#JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url) 
    time.sleep(7)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # the image stays on the article and style 
    latest_image=soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_img_url = "https://www.jpl.nasa.gov" + latest_image
#Display
#featured_img_url
#Scrape url
    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(7)
    # time.sleep() goes here
    # # HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather=[]
    tweets = soup.find_all('span',class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    for weather in tweets:
        tweet_weather = weather.text
        if 'InSight' in tweet_weather:
            mars_weather=tweet_weather
            break
        else:
            pass
 
#print(mars_weather)
#Scrape url
    url="https://space-facts.com/mars/"
    #using read_html
    tables = pd.read_html(url)
    df=tables[0]
##Namning the columns
    df.columns=["Description","Values"]
    html_table = df.to_html().replace('\n', '')
    

    #Mars Hemisphere
    #Scrap url
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(7)
# # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    #Empty table
    hemisphere_image_urls=[]
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all('div',{'class':'item'})
    #hemispheres
    #Loop using for
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        image = hemisphere.find('a', class_='itemLink product-item')['href']
        browser.visit('https://astrogeology.usgs.gov' + image)
        time.sleep(7)
        hemi_html = browser.html
        soup = BeautifulSoup(hemi_html, 'html.parser')
        url = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
        title = title.replace('Enhanced', '')
        hemisphere_image_urls.append({"title" : title, "img_url" : url})
    #hemisphere_image_urls
    marsDetails={"NewsTitle":news_title,
    "NewsDetails":news_p,
    "Image":featured_img_url,
    "MarsWeather":mars_weather,
    "MarsTable":html_table,
    "HemisphereImageUrl":hemisphere_image_urls
    }
    browser.quit()
    return marsDetails
if __name__ == '__main__':
    scrape()  



