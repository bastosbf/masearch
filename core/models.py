# coding=utf-8

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models


class Brand(models.Model):
    code = models.CharField(u'Code', max_length=4, unique=True)
    brand = models.CharField(u'Brand', max_length=255)
    
    class Meta:
        verbose_name = u'Brand'
        verbose_name_plural = u'Brands'
        ordering = (u'brand',)

    def __unicode__(self):
        return self.brand


class Category(models.Model):
    code = models.CharField(u'Code', max_length=4, unique=True)
    category = models.CharField(u'Category', max_length=255)
    
    class Meta:
        verbose_name = u'Category'
        verbose_name_plural = u'Categories'
    
    def __unicode__(self):
        return self.category

class Product(models.Model):
    code = models.CharField(u'Code', max_length=4, unique=True)       
    name = models.CharField(u'Name', max_length=255)
    description = models.CharField(u'Description', max_length=255, null=True, blank=True)
    brand = models.ForeignKey(Brand, verbose_name=u'Brand')
    category = models.ForeignKey(Category, verbose_name=u'Category')
    photo = models.FileField(upload_to=u'products_photos/', null=True, blank=True)
    
    class Meta:
        verbose_name = u'Product'
        verbose_name_plural = u'Products'
        ordering = (u'name',)

    def __unicode__(self):
        return self.name + ' - ' + self.brand.brand
   

class Store(models.Model):
    code = models.CharField(u'Code', max_length=4, unique=True)
    name = models.CharField(u'Name', max_length=255)
    address = models.CharField(u'Address', max_length=255)
    phone = models.CharField(u'Phone', max_length=255)
    photo = models.FileField(upload_to=u'stores_photos/', null=True, blank=True)
    
    class Meta:
        verbose_name = u'Store'
        verbose_name_plural = u'Stores'
        
    def __unicode__(self):
        return self.name
    
    
    
class ProductStore(models.Model):
    product_code = models.ForeignKey(Product, verbose_name=u'Product')
    store_code = models.ForeignKey(Store, verbose_name=u'Store')
    value = models.FloatField(u'Value');    
    
    class Meta:
        verbose_name = u'Product'
        verbose_name_plural = u'Add/Edit Products Values'    
    
    
class NewProduct(models.Model):
    name = models.CharField(u'Name', max_length=255)
    description = models.CharField(u'Description', max_length=255, null=True, blank=True)
    brand = models.CharField(u'Brand', max_length=255)
    category = models.CharField(u'Category', max_length=255)
    photo = models.FileField(upload_to=u'new_products_photos/', null=True, blank=True)
    
    class Meta:
        verbose_name = u'New Product'
        verbose_name_plural = u'Order Registration of New Products'
        ordering = (u'name',)

    def __unicode__(self):
        return self.name + ' - ' + self.brand    
    
class Profile(models.Model):
    user = models.OneToOneField(User)
    store = models.ForeignKey(Store, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)   