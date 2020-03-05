"""
This function is designed to scrape SpaceNK website to get information about the products' ingredients, price, rating, and more
"""

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re
from urllib.request import urlopen


url = "https://www.spacenk.com/uk/en_GB/skincare/moisturisers/day-moisturiser/cr%C3%A8me-de-la-mer-moisturizing-cream-MUK200020070.html?dwvar_MUK200020070_size=UK200020070"
ourURL = urllib.request.urlopen(url)
soup = BeautifulSoup(ourURL, "html.parser")
print(soup.prettify())


ingredients = []
product_names = []
average_ratings = []
unit_prices = []
currencies = []
categories = []
manufacturers = []
skin_types = []

"""Functions to get different information"""

def getIngredients(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    div = soup.findAll("div", {"class": "pdp-accordion-description"})
    ing = div[1].get_text().replace('\n','')
    s = ''
    ing = s.join(ing)
    return ing
    
def getProduct(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    info = soup.findAll("script", {"type": "text/javascript"})
    info = info[2].get_text()
    info = info.strip("\n\t\t").split(",")
#     important.split(",")
    product = info[-1].strip('')
    product = info[-1].lstrip('"productName":') 
    product_name = product.rstrip('"}}];')
    return product_name
        
        
def getRating(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    info = soup.findAll("script", {"type": "text/javascript"})
    info = info[2].get_text()
    info = info.strip("\n\t\t").split(",")
    average_rating = info[-5][16:].strip('""')
    return average_rating
    
def getPrice(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    info = soup.findAll("script", {"type": "text/javascript"})
    info = info[2].get_text()
    info = info.strip("\n\t\t").split(",")
    unit_price = info[-7][13:].strip('')
    return unit_price
    
def getCurrency(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    info = soup.findAll("script", {"type": "text/javascript"})
    info = info[2].get_text()
    info = info.strip("\n\t\t").split(",")
    currency = info[-8][11:].strip('""')
    return currency
    
def getCat(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    info = soup.findAll("script", {"type": "text/javascript"})
    info = info[2].get_text()
    info = info.strip("\n\t\t").split(",")
    category = info[-13][14:].strip('""')
    return category
    
def getMan(self, link):
    html = urlopen(link)
    soup = BeautifulSoup(html, "html.parser")
    info = soup.findAll("script", {"type": "text/javascript"})
    info = info[2].get_text()
    info = info.strip("\n\t\t").split(",")
    manufacturer = info[-19][15:].strip('""')
    return manufacturer
    
def getSkin(self, link):    
    to_get_skin = soup.find("div", {"class": "pdp-accordion-keybenefits"}, "li")
    to_get_skin = to_get_skin.get_text()
    to_get_skin = to_get_skin.replace("\n", "")
    to_get_skin = to_get_skin.split(",")
    skin = to_get_skin[0][13:].strip('')
    return skin
        
"""
Creating a class to put all functions together
"""

class Beauty():
    def into_content(self, link):
        html = urlopen(link)
        soup = BeautifulSoup(html, "html.parser")
        div = soup.findAll("div", {"class": "pdp-accordion-description"})
        ing = div[1].get_text().replace('\n','')
        s = ''
        ing = s.join(ing) 
        
        info = soup.findAll("script", {"type": "text/javascript"})
        info = info[2].get_text()
        info = info.strip("\n\t\t").split(",")
        
        product = info[-1].strip('')
        product = info[-1].lstrip('"productName":') 
        product_name = product.rstrip('"}}];')
        
        average_rating = info[-5][16:].strip('""')
        
        unit_price = info[-7][13:].strip('')
        
        currency = info[-8][11:].strip('""')
        
        category = info[-13][14:].strip('""')
        
        manufacturer = info[-19][15:].strip('""')
        
        to_get_skin = soup.find("div", {"class": "pdp-accordion-keybenefits"}, "li")
        to_get_skin = to_get_skin.get_text()
        to_get_skin = to_get_skin.replace("\n", "")
        to_get_skin = to_get_skin.split(",")
        skin = to_get_skin[0][13:].strip('')
        
        ingredients.append(ing)
        product_names.append(product_name)
        average_ratings.append(average_rating)
        unit_prices.append(unit_price)
        currencies.append(currency)
        categories.append(category)
        manufacturers.append(manufacturer)
        skin_types.append(skin)
        return ingredients, product_names, average_ratings, unit_prices, currencies, categories, manufacturers, skin_types


"""
Putting everything into a dataframe
"""

df = pd.DataFrame({'ingredients': ingredients, 'product': product_names,
'ratings': average_ratings, 'price': unit_prices, 'currency': currencies, 'category': categories, 'manufacturer': manufacturers, 'skin': skin_types
})
print(df.info())
df
