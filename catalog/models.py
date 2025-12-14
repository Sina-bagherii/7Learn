from django.db import models

class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True,verbose_name="this for alternative of (title)")
    
    
    create_time=models.DateTimeField(auto_now_add=True)
    modified_time=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title

    
class Category(models.Model):
    name=models.CharField(max_length=32)
    parent=models.ForeignKey("self",on_delete=models.CASCADE,related_name="category",null=True,blank=True)
    class Meta:
        verbose_name_plural="Categories"
    def __str__(self):
        return self.name
    
    
class Brand(models.Model):
    name=models.CharField(max_length=32)
    parent=models.ForeignKey("self",on_delete=models.CASCADE,related_name="brand",null=True,blank=True)
    
    def __str__(self):
        return self.name 
    
class Product(models.Model):
    producttype=models.ForeignKey(ProductType,on_delete=models.CASCADE,related_name="products")
    upc=models.IntegerField(unique=True)
    title=models.CharField(max_length=32)
    description=models.CharField(max_length=32,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    
    

class ProductAttribute(models.Model): 
    INTEGER=1
    STRING=2
    FLOAT=3
    
    ATTRIBUTE_TYPE_FIELDS=(
        (INTEGER,"Integer"),
        (STRING,"String"),
        (FLOAT,"Float"),
    )
    title=models.CharField(max_length=32)
    producttype=models.ForeignKey(ProductType,on_delete=models.CASCADE,related_name="attribute",null=True,blank=True)
    attribute_type=models.PositiveSmallIntegerField(default=INTEGER,choices=ATTRIBUTE_TYPE_FIELDS)
   
    
    
class ProductAttributevalue(models.Model):
    value=models.CharField(max_length=32)
    productattribute=models.ForeignKey(ProductAttribute,on_delete=models.CASCADE)
    
    
    
