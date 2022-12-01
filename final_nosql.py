#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 13:10:17 2022

@author: mny_1026
"""

import requests
import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["count"]
collection = my_db["count"]
response = []
response.append(requests.get(url="https://restcountries.com/v3.1/all", headers={'User-Agent':'Custom'}))
response[0] = response[0].json()
print(response[0])
collection.insert_many(response[0])
