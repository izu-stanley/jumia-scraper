#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:58:14 2019

@author: izuchukwu
"""
import urllib.parse
import requests
from bs4 import BeautifulSoup
import logging
import os
import pandas as pd

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

BASE_URL = 'https://www.jumia.com.ng'
CATALOG_URL = BASE_URL + '/catalog/?q='



def data_builder(i):
    try:
        product_url = BASE_URL + i.find('a').attrs['href']
    except (KeyError,AttributeError):
        product_url = ''
        
    try:
        product_id = i.find('a').attrs['data-id']
    except (KeyError,AttributeError):
        product_id = ''
        
    try:
        product_name = i.find('a').attrs['data-name']
    except (KeyError,AttributeError):
        product_name = ''
    
    try:
        product_price = ''.join(i.find('div',{'class':'prc'}).text.split('₦')[-1].strip().split(','))
    except (KeyError,IndexError,AttributeError):
        product_price = ''
    
    try:
        product_old_price = ''.join(i.find('div',{'class':'old'}).text.split('₦')[-1].strip().split(','))
    except (KeyError,IndexError,AttributeError):
        product_old_price = ''
        
    try:
        product_discount = i.find('div',{'class':'tag _dsct _sm'}).text
    except (KeyError,AttributeError):
        product_discount = ''
        
    try:
        product_brand = i.find('a').attrs['data-brand']
    except (IndexError,AttributeError):
        product_brand = ''
        
    try:
        product_category = i.find('a').attrs['data-category']
    except (IndexError,AttributeError):
        product_category = ''
        
    try:
        product_image = i.find('img').attrs['data-src']
    except (IndexError,AttributeError):
        product_image = ''
        
    try:
        image_width = i.find('img').attrs['width']
    except (IndexError,AttributeError):
        image_width = ''
    
    try:
        image_height = i.find('img').attrs['height']
    except (IndexError,AttributeError):
        image_height = ''
    
    try:
        shipping_type = i.find('div',{'class':'tag _glb _sm'}).text
    except (IndexError,AttributeError):
        shipping_type = ''
        
    try:
        rating_percent = i.find('div',{'class':'in'}).text
    except (IndexError,AttributeError):
        shipping_type = ''

    try:
        rating_percent = i.find('div',{'class':'in'}).attrs['style'].split(':')[-1]
    except (IndexError,AttributeError):
        rating_percent = ''
    
    try:
        num_of_ratings = i.find('div',{'class':'rev'}).text
    except (IndexError,AttributeError):
        num_of_ratings = ''
    
        
    
    
    data = {}
    keys = ['product_url','product_id','product_name','product_price','product_old_price','product_discount',
            'product_brand','product_category','product_image','product_image','product_image',
            'image_width','image_height','shipping_type','rating_percent','num_of_ratings']
    values = [product_url,product_id,product_name,product_price,product_old_price,product_discount,
            product_brand,product_category,product_image,product_image,product_image,
            image_width,image_height,shipping_type,rating_percent,num_of_ratings]
    
    for key,value in zip(keys,values):
        data[key] = value
    
    return data


def topDeals(query, sorter='', params=''):
    url = CATALOG_URL
    query = query.split()
    query = '+'.join(query)
    url = url + query + sorter + params
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    products = [x for x in soup.find_all('article', {'class': 'prd _fb col c-prd'})]
    
    product_results = [data_builder(product) for product in products]
    
    return product_results


def lowestPrice(query):
    return topDeals(query=query, sorter='&sort=Price%3A%20Low%20to%20High&dir=asc')


def highestPrice(query):
    return topDeals(query=query, sorter='&sort=Price%3A%20High%20to%20Low&dir=desc')


def sortPrice(query, prange, switch=0):
    params = {'price': prange}
    params = '&' + urllib.parse.urlencode(params, doseq=True)
    if switch == 1:
        return topDeals(query=query, params=params, sorter='&sort=Price%3A%20Low%20to%20High&dir=asc')
    elif switch == 2:
        return topDeals(query=query, params=params, sorter='&sort=Price%3A%20High%20to%20Low&dir=desc')
    else:
        return topDeals(query=query, params=params)


def rangePriceLow(query, prange):
    return sortPrice(query, prange, 1)


def rangePriceHigh(query, prange):
    return sortPrice(query, prange, 2)

def sortReviews(query):
    return topDeals(query=query, sorter='&sort=rating')


re = sortReviews(query='galaxy note 8')

results = pd.DataFrame(re)
results.to_csv('results.csv',index=False)




logging.info(re)
