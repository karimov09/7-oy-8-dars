from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from .models import Product, Category, Review, Comment
from .forms import CommentForm



class Index(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()

        product_reviews = {}
        for product in products:
            product_reviews[product.id] = Review.objects.filter(product=product)

        context = {
            "products": products,
            "categories": categories,
            "product_reviews": product_reviews, 
            'organic_products': products.filter(quality='or')
        }
        return render(request, 'index.html', context)


def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Izoh qo'shildi")
            return redirect('izohlar')  
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'  
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id') 
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        
        if product_id and comment and rating: 
            try:
                product = Product.objects.get(id=product_id)  
                Review.objects.create(product=product, comment=comment, rating=rating)  
                return redirect('product_detail', pk=product_id)  
            except Product.DoesNotExist:
                return redirect('product_list')  
        else:
            return redirect('product_list')
    return redirect('product_list')  

def home(request):
    return render(request, 'index.html')

def jewellery(request):
    return render(request, 'jewellery.html')

def electronic(request):
    return render(request, 'electronic.html')
