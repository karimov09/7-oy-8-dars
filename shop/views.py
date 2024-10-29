from django.shortcuts import render
from django.views.generic import View

from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def get(self, request):
        return render(request, "index.html")
    
def jewellery(request):
    return render(request, 'jewellery.html')

def electronic(request):
    return render(request, 'electronic.html')