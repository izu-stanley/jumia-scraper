#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:58:14 2019

@author: izuchukwu
"""
import urllib.parse
import requests
from bs4 import BeautifulSoup


def topDeals(query, sorter='', params=''):
    url = 'https://www.jumia.com.ng/catalog/?q='
    query = query.split()
    query = '+'.join(query)
    url = url + query + sorter + params
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    name = [x.text for x in soup.find_all('span', {'class': 'name'})]
    price = [x.text.split('₦')[1] for x in soup.find_all(
        'span', {'class': 'price-box ri'})]
    image = [x.find_next('img')['data-src']
             for x in soup.find_all('div', {'class': 'image-wrapper default-state'})]
    return name[:5], price[:5], image[:5]


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


re = topDeals(query='airpods')
print(re)
