from django.urls import path
from .views import product_list,product_detail,category_product,product_category


urlpatterns=[
    path('product/list',product_list,name='product_list'),
    path('product/detail/<int:pk>',product_detail,name="product_detail"),
    path('product/detail/<int:pk>/products',category_product,name="product_detail"),
    path('category/detail/<int:pk>/category',product_category,name="category_detail")
    
]





 




























































# from django.urls import path
# from blog.views import test,post_detail
# urlpatterns=[
#     path('list/',test),
#     path('detail/samsung_Galaxi_s23',test),
#     path('categories',test)   
# ]