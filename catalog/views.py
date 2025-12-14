from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product,Category,ProductType,Brand
from .models import Product,Category,ProductType,Brand






def product_list(request):
    products=Product.objects.filter(is_active=True)
    products=Product.objects.filter(is_active=False)
    category=Category.objects.first()
    category=Category.objects.last()
    
    # category=Category.objects.get(id=1)
    products=Product.objects.filter(is_active=True,category=Category)
    category=Category.objects.filter(name="Book").first()
    
    brand=Brand.objects.first()
    products=Product.objects.filter(is_active=True,category_id=1)
    products=Product.objects.filter(is_active=True,category__name=category)
    product_type=ProductType.objects.filter(title='Book')
    new_product=Product.objects.create(
        product_type=product_type,upc=3245,title='How to learn Java',description='Nothing',category=category,
        brand=brand
        
    )
    
    
    # Filter
    products=Product.objects.select_related('category').all()
    
    context="\n".join([f"{product.title},,{product.upc},,{product.category.name}" for product in products])
    return HttpResponse("product")



def product_detail(request,pk):
    # try:
        # product=Product.objects.get(pk=pk)
    # except product.DoesNotExist :
    #     try:
    #         product=Product.objects.get(upc=pk)
    #     except product.DoesNotExist:
    #         return HttpResponse ("Product does not exist" )
    # # OR
    queryset=Product.objects.filter(is_active=True).filter(Q(pk=pk)|Q(upc=pk))
    if queryset.exists():
        product=queryset.first()
        return HttpResponse (f"The title is {product.title}")
    # product=Product.objects.filter(Q(upc=pk)|Q(pk=pk))
    else:
        return HttpResponse("The product does not exist")

# Create your views here.

def category_product(request,pk):
    # return HttpResponse ("tst")
    try:
        category=Category.objects.prefetch_related("products").get(pk=pk)
    except Category.DoesNotexist:
        return HttpResponse("Product does not exist")
    # product=Product.objects.filter(category=category)
    
    
    #related_name  
    products=category.products.all() 

    #
    
    
    context="\n".join([f"{product.title},,{product.upc} " for product in products])
    return HttpResponse(context)
    


def product_category(request,pk):
    try:
        product=Product.objects.select_related('category').get(upc=pk)
    except Product.DoesNotExist:
        return HttpResponse("Category does npt exist")
    
    return HttpResponse (f"{product.category.name}")
    
    
        
    
