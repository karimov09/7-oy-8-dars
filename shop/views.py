from django.shortcuts import render
from django.views.generic import View
from .models import Product, Category
from django.shortcuts import render

class Index(View):
    def get(self, request):
          products = Product.objects.all()
          categories = Category.objects.all()
          context = {
               "products": products,
               "categories": categories,
          }
          return render(request, 'index.html', {'products': products, 'categories': categories})


def home(request):
    return render(request, 'index.html')

def get(self, request):
        return render(request, "index.html")
    
def jewellery(request):
    return render(request, 'jewellery.html')

def electronic(request):
    return render(request, 'electronic.html')