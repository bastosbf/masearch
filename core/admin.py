from django.contrib import admin
from core.models import *

class BrandAdmin(admin.ModelAdmin):    
    list_display = ('code', 'brand',)
    search_fields = ['code', 'brand']
  
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'category')
    search_fields = ['code', 'category']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'brand', 'category',)
    search_fields = ['code', 'name', 'brand__brand', 'category__category']
    
    def save_model(self, request, obj, form, change): 
        if not obj.pk: # verify is it was already inserted
            obj.save() 
            stores = Store.objects.all()
            for store in stores:
                product_store = ProductStore(store_code=store, product_code=obj, value=0)
                product_store.save()
        else:
            obj.save()

class StoreAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'address', 'phone',)    
    search_fields = ['code', 'name', 'address']
    
    def save_model(self, request, obj, form, change): 
        if not obj.pk: # verify is it was already inserted
            obj.save() 
            products = Product.objects.all()
            for product in products:
                product_store = ProductStore(store_code=obj, product_code=product, value=0)
                product_store.save()
        else:
            obj.save()
    
class ProductStoreAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'value')
    search_fields = ['product_code__name', 'value']
    fields = ['product_code', 'value']
    readonly_fields = ['product_code']

    def get_queryset(self, request):
        qs = super(ProductStoreAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.profile.store is None:
            return qs
        return qs.filter(store_code=request.user.profile.store)

    def save_model(self, request, obj, form, change): 
        obj.store_code = request.user.profile.store
        obj.save() 
        
class NewProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category',)
    search_fields = ['name', 'brand', 'category']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store',)
    search_fields = ['user__username', 'store__name']
    
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(ProductStore, ProductStoreAdmin)
admin.site.register(NewProduct, NewProductAdmin)
admin.site.register(Profile, ProfileAdmin)