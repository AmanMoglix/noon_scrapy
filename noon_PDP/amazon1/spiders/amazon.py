#-*- coding: utf-8 -*-
# any thing you want
from operator import le
import re
import selectors
from time import time
import scrapy
import sys
import random
import requests
from bs4 import BeautifulSoup
import chompjs
import json



class AmazonSpider(scrapy.Spider):
    name = 'amazonsearchterm'
 
    abc=open('/home/moglix/Desktop/amazonsearchterm.txt').read().splitlines()
    data_analysy={}
    for intercept_url in abc:
            ur_l=intercept_url
            base_url=ur_l.split('||')[0]
            msn_url=ur_l.split('||')[1]
            data_analysy[base_url]=msn_url
            #print(base_url,msn_url)

    start_urls=data_analysy.keys()

    #start_urls=abc
    
    def parse(self, response):
        data={}
       
        price_now=""
        price_now=price_now.join(response.xpath("//div[contains(@class,'priceNow')]/text()").getall()).replace('AED','')
        
        price_was=""
        price_was=price_was.join(response.xpath("//div[contains(@class,'priceWas')]/text()").getall()).replace('AED','')
        
        price_saving=""
        price_saving=price_saving.join(response.xpath("//div[contains(@class,'priceSaving')]/text()").getall()).replace('AED','')

        sold_by=response.xpath("//*[contains(@class,'allOffers')]/text()").get()

        #capture the remaining data from script tag
        text = response.xpath(
            "//*/script[contains(@type,'application/json')]/text()").extract_first()
        json_text = json.loads(text)
        #print("text :",json_text)
        breadcrumbs = json_text.get('props').get('pageProps').get('catalog').get('product').get('breadcrumbs')
        #print("brand crumbs :",breadcrumbs)
        #capture the taxonomy
        l1=""
        l2=""
        l3=""
        l4=""
        l5=""
        if(len(breadcrumbs)>1):
            l1=breadcrumbs[0]['name']
        if(len(breadcrumbs)>=2):
            l2=breadcrumbs[1]['name']
        if(len(breadcrumbs)>=3):
            l3=breadcrumbs[2]['name']
        if(len(breadcrumbs)>=4):
            l4=breadcrumbs[3]['name']
        if(len(breadcrumbs)>=5):
            l5=breadcrumbs[4]['name']
        # print(" l1 ",l1 ,l2  ,l3 ,l4 ,l5)
        product_title=json_text.get('props').get('pageProps').get('catalog').get('product').get('product_title')
        # print('product_title ',product_title)
        brand =json_text.get('props').get('pageProps').get('catalog').get('product').get('brand')
        # print('brand ',brand)
        brand_code=json_text.get('props').get('pageProps').get('catalog').get('product').get('brand_code')
        # print('brand_code ',brand_code)
        long_description=json_text.get('props').get('pageProps').get('catalog').get('product').get('long_description')
        # print('description ',long_description)
        feature_bullets=json_text.get('props').get('pageProps').get('catalog').get('product').get('feature_bullets')
        heighlights=""
        k=1
        if len(feature_bullets) !=0:
            while k <len(feature_bullets):
                for heighlight in feature_bullets:
                    heighlights= heighlights+heighlight+ " || "
                    k=k+1
        print("heigh ligjts :" ,heighlights)
        #capture the model number
        model_name=''
        model_number=''
        #print(' feature bulltes ',feature_bullets)
        specifications=json_text.get('props').get('pageProps').get('catalog').get('product').get('specifications')
        specification=""
        s=1
        if len(specifications) !=0:
            while s < len(specifications):
                for spec in specifications:
                    spec_json=spec
                    
                    model_name=spec_json['name']
                    if model_name == 'Model Number':
                        model_number=(spec_json['value'])

                    specification=specification+(spec_json['name']+" : "+spec_json['value'])+" || "
                    s=s+1
        #print("specification : ",specification)
        #print("model number : ",model_number)
        #print('specification ',specifications)

        image_keys=json_text.get('props').get('pageProps').get('catalog').get('product').get('image_keys')
        image1=""
        image2=""
        image3=""
        image4=""
        image5=""
        image6=""
        cdn_url="https://f.nooncdn.com/products/tr:n-t_400/"
        image_type=".jpg"
        if len(image_keys) !=0:
            if(len(image_keys)>=1):
                image1=cdn_url+image_keys[0]+image_type
            if(len(image_keys)>=2):
                image2=cdn_url+image_keys[1]+image_type
            if(len(image_keys)>=3):
                image3=cdn_url+image_keys[2]+image_type
            if(len(image_keys)>=4):
                image4=cdn_url+image_keys[3]+image_type
            if(len(image_keys)>=5):
                image5=cdn_url+image_keys[4]+image_type
            if(len(image_keys)>=6):
                image6=cdn_url+image_keys[5]+image_type

        print('image_keys ',image1,image2,image3,image4,image5,image6)
        
       
        if len(json_text)==0 :
             filet=open('failed_netmart.txt','a')
             filet.write(str(response.url)+"\n")
        
        data={
            'product_link':response.url,
            'category_l1':l1,
            'category_l2':l2,
            'category_l3':l3,
            'category_l4':l4,
            'category_l5':l5,
            'brand':brand,
            'product_name':product_title,
            'model_number':model_number,
            'highlights':heighlights,
            'overview':long_description,
            'specifications':specification,
            'image1':image1,
            'image2':image2,
            'image3':image3,
            'image4':image4,
            'image5':image5,
            'image6':image6,
            'was_price':price_was,
            'now_price':price_now,
            'sold_by':sold_by
            
        }
        
        yield data

