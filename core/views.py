# coding: utf-8

from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import *
from django.db.models import Q
from django.db import connection
from collections import OrderedDict

def home(request):
    return render(request, 'search.html')

def about(request):
    return render(request, 'about.html')

def search(request):
    product_name = request.POST['product']
    if not product_name:
        return render(request, "search.html", {'msg' : u'Type the name of the product you want to search!'})
    cursor = connection.cursor()
    cursor.execute("SELECT core_product.code, name, brand, description, photo, value FROM core_product" + 
                   " INNER JOIN core_productstore ON core_product.id =  core_productstore.product_code_id" + 
                   " INNER JOIN core_brand ON core_product.brand_id = core_brand.id"
                   " WHERE UPPER(core_product.name) LIKE UPPER('%" + product_name + "%') AND value > 0 ORDER BY core_productstore.value ASC")    
    row = cursor.fetchall()
    if not bool(row):
        return render(request, "search.html", {'msg' : u'We did not find any record for product {0} :('.format(product_name)})
    search_result = {}
    for r in row :
        code = r[0]        
        if code not in search_result.keys() :
            photo = r[4]
            if not photo :
                photo = "products_photos/no-photo.png"
            search_result[code] = {'name': r[1], 'brand' : r[2], 'description' : r[3], 'photo' : photo, 'lowest_value' : r[5], 'highest_value' : r[5]}
        else :
            value = r[5]
            if(search_result[code]['lowest_value'] > value) :
                search_result[code]['lowest_value'] = value
            if(search_result[code]['highest_value'] < value) :
                search_result[code]['highest_value'] = value
    search_result = OrderedDict(sorted(search_result.items(), key=lambda kv: kv[1]['lowest_value']))        
    return  render(request, 'products.html', {'products' : search_result})
        

def stores(request):
    product = request.GET['product']
    cursor = connection.cursor()
    cursor.execute("SELECT core_store.code, core_store.name, address, phone, core_store.photo, value, core_product.name, brand  FROM core_store" +                    
                   " INNER JOIN core_productstore ON core_store.id =  core_productstore.store_code_id" +
                   " INNER JOIN core_product ON core_product.id =  core_productstore.product_code_id" +
                   " INNER JOIN core_brand ON core_product.brand_id = core_brand.id" +
                   " WHERE core_product.code = '" + product + "' AND value > 0 ORDER BY core_productstore.value ASC")    
    row = cursor.fetchall()
    if not bool(row):
        return HttpResponseBadRequest(u'We did not find any record for product {0} :('.format(product))
    search_result = {}
    product_name = None
    brand = None
    for r in row :
        if product_name is None and brand is None :
            product_name = r[6]
            brand  = r[7]
        code = r[0]
        if code not in search_result.keys() :
            photo = r[4]
            if not photo :
                photo = "stores_photos/no-photo.png"
            search_result[code] = {'name': r[1], 'address' : r[2], 'phone' : r[3], 'photo': photo, 'value' : r[5]}                
    search_result = OrderedDict(sorted(search_result.items(), key=lambda kv: kv[1]['value']))
    return  render(request, 'stores.html', {'stores' : search_result, 'product': product_name, "brand" : brand})

