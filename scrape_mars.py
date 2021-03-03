#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from pprint import pprint

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    req =  requests.get(url)

    soup = bs(req.content, 'html.parser')


    # ### Latest News Article Title and Paragraph Text
    latest_news_title = soup.find_all("div", {"class" : "content_title"})[0].text.strip()
    latest_news_para_text = soup.find_all("div", {"class" : 'rollover_description_inner'})[0].text


    # ### JPL Mars Space Images - Featured Image
    browser = init_browser()

    # Navigate to mars images url
    mars_images_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    browser.visit(mars_images_url)
    html = browser.html


    url_base = mars_images_url.split("/")
    url_base.pop()
    url_base = "/".join(url_base)

    soup = bs(html, 'html.parser')
    featured_image_url = soup.find("img",{"class":"headerimage fade-in"})["src"]

    joined_image_url = url_base + "/" + featured_image_url
    browser.quit()


    # ### Mars Facts
    mars_facts_tables = pd.read_html("https://space-facts.com/mars/")
    html_table = mars_facts_tables[0].to_html().replace('\n', '')


    # ### Mars Hemispheres
    browser = init_browser()

    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    html = browser.html
    soup = bs(html, 'html.parser')

    prefix = "https://astrogeology.usgs.gov"

    link_list_top = soup.find_all("a",{"class":"itemLink product-item"})
    link_list = [link_list_top[i] for i in range(1,len(link_list_top),2)]

    hemisphere_image_urls = []

    for num in range(len(link_list)):
        #initialize dictionary for each link
        link_dict = {} 
    
        # get title
        link_dict["title"] = link_list[num].h3.text.replace(' Enhanced','')
    
        #click on url to get url for image
        browser.links.find_by_partial_text("Enhanced")[num].click()
        img_url = browser.links.find_by_partial_text("Original").first['href']
        browser.back()
        link_dict["img_url"] = img_url

        hemisphere_image_urls.append(link_dict)

    browser.quit()


    mars_info = {
        "latest_news_title" : latest_news_title,
        "latest_news_para_text" : latest_news_para_text,
        "featured_image_url" : joined_image_url,
        "mars_facts_table" : html_table,
        "hemis" : hemisphere_image_urls
    }

    return mars_info
    

