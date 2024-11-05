from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.db.models import Count, Q
from .models import Product, Category, Review
from .forms import CommentForm

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(product_count=Count('products'))
        return context

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_products.html', context)

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Izoh qo'shildi!")
            return redirect('home')  
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

def submit_review(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if product_id and comment and rating:
            product = get_object_or_404(Product, id=product_id)
            Review.objects.create(product=product, comment=comment, rating=rating)
            messages.success(request, "Sizning sharhingiz qo'shildi!")
            return redirect('product_detail', pk=product_id)
        else:
            messages.error(request, "Barcha maydonlar to'ldirilishi kerak.")
    return redirect('product_list')

def home(request):
    return render(request, 'index.html')

def jewellery(request):
    return render(request, 'jewellery.html')

def electronic(request):
    return render(request, 'electronic.html')
