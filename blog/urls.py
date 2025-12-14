# urls.py
from django.urls import path, re_path, register_converter
from blog.views import post_list, category_list, post_detail
from academy.utils import FourdigitYear # ensure exact class name

register_converter(FourdigitYear, 'fourdigit')

urlpatterns = [
    # archives first (fine either way)
    path('archive/<fourdigit:year>/', post_list),
    re_path(r'^archive/(?P<year>[0-9]{2,4})/$',post_detail),
    path('archive/<int:year>/<int:month>/', post_list),

    # detail: most specific → most generic
    path('detail/<int:post_id>/', post_detail),
    path('detail/<uuid:post_uuid>/', post_detail),
    re_path(r'detail/(?P<post_slug>[\w-])+/', post_detail),              # simpler than re_path
    # If you really want regex for slug:
    # re_path(r'^detail/(?P<post_slug>[\w-]+)/$', post_detail),
    path('archive/<fourdigit:year>/',post_list),
    # put this LAST; it will match almost anything
    path('detail/<str:post_title>/', post_detail),
    re_path(r"archive/(?P<year>[0-9]{2,4})/",post_list),

    path('list/', post_list),
    path('categories/', category_list),
    
    re_path(r"archive/(?P<code>[0-9]{4})/",post_list),
    re_path(r"archive/(?P<code>[0-9]{6})/",post_list),
]
