
from django.contrib import admin
from django.contrib.admin import register
from .models import Category,Brand,ProductType,Product,ProductAttribute,ProductAttributevalue
# Register your models here.



 

@register(Product)
class Productadmin(admin.ModelAdmin ):
    list_display=('upc','producttype','title','is_active','category_id','brand_id')
    list_display_links=['title']
    list_filter=['is_active']
    list_editable=['is_active']
    search_fields=['upc','title','category_id__name','brand_id__name'  ]
    actions=['active_all']
    # inlines=[ProductAttributeiInline]
    def has_delete_permission(self, request, obj = ...):
        return False
    def has_view_permission(self, request, obj = ...):
        return True
    def has_change_permission(self, request, obj = ...):
        return True

    def active_all(self,request,queryset):
        pass 
    
@register(ProductAttribute)
class ProductAttributeadmin(admin.ModelAdmin):
    list_display=("title","producttype","attribute_type")
    list_filter=["producttype"]
    
    
class ProductAttributeiInline(admin.TabularInline):
    model=ProductAttribute
    extra=2 
    
    
    
    
class ProductTypeadmin(admin.ModelAdmin):
    list_display=("title",)
    inlines=[ProductAttributeiInline]

    
    
    
@register(ProductAttributevalue)


class ProductAttributevalueadmin(admin.ModelAdmin):
    list_display=['value']
    # inlines=[ProductAttributeValueInline]




admin.site.register(Category)
admin.site.register(Brand) 
# admin.site.register(Product,Productadmin)
admin.site.register(ProductType,ProductTypeadmin)