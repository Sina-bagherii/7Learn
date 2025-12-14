from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def post_list(request,year=None,month=None):
    if month is not None:
        return HttpResponse(f"Post list achieve on {year} and {month}")
    elif year is not None:
        return HttpResponse(f"Post list achieve on {year}") 
    # return HttpResponse("Posts list Page") 
def category_list(request):
    return HttpResponse("Category List page")

def post_detail(request,post_title):
    return HttpResponse(f"Post detail imported {post_title}")
def test(request):
    return HttpResponse("This is just test bro")
    