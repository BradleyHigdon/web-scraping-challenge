from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import pymongo
import requests


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #NASA Mars News
    NASA_news_url = "https://mars.nasa.gov/news/"
    browser.visit(NASA_news_url)
    NASA_news_html = browser.html
    NASA_news_soup = bs(NASA_news_html,'lxml')
    NASA_news_title = NASA_news_soup.find("div", class_="content_title").text
    NASA_news_paragraph = NASA_news_soup.find("div", class_="article_teaser_body").text

    #JPL Mars Space Images - Featured Image
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)
    html = browser.html
    JPL_soup = bs(html, 'html.parser')
    JPL_image = (JPL_soup.find_all('div', class_='button_fancybox')[0].a.get('fancybox-image'))
    JPL_featured = 'https://www.jpl.nasa.gov'+ JPL_image
    JPL_mars_web['featured_image'] = JPL_featured

    #Mars Facts
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_tables_df = ((pd.read_html(url))[0]).rename(columns={0: "Attribute", 1: "Value"}).set_index(['Attribute'])
    mars_html_table = (tables_df.to_html()).replace('\n', '')
    mars_web['mars_data'] = mars_html_table

    # Mars Hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)  
    hemispheres_html = browser.html 
    hemispheres_soup = bs(hemispheres_html,"html.parser") 
    hemispheres_results = hemispheres_soup.find_all("div",class_='item')
    hemispheres_image_urls = []
    for result in results:
        product_dict = {}
        hemispheres_titles = item.find('h3').text
        hemispheres_image_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(primary_url + hemispheres_image_url)
        hemispheres_image_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_image_html, 'html.parser')
        hemispheres_image_url = primary_url + hemispheres_soup.find('img', class_='wide-image')['src']
        product_dict['title']= hemispheres_titles
        product_dict['image_url']= hemispheres_image_url        
        urls_of_hemisphere_images.append({"Title" : hemispheres_titles, "Image_URL" : hemispheres_image_url})



mars_data ={
		'news_title' : NASA_news_title,
		'summary': NASA_news_para,
        'featured_image': JPL_feature_url,
		'featured_image_title': JPL_mars_web,
        'news_url': news_url,
		'fact_table': mars_web,
		'hemisphere_image_urls': hemisphere_image_urls,
        'jpl_url': jurl,
        'hemisphere_url': urls_of_hemisphere_images
        }
    db = mars_data
