from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import Product, Category, Review, 


class Index(View):
    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()

        # Har bir mahsulot uchun sharhlarni qo'shish
        product_reviews = {}
        for product in products:
            product_reviews[product.id] = Review.objects.filter(product=product)

        context = {
            "products": products,
            "categories": categories,
            "product_reviews": product_reviews,  # Har bir mahsulot uchun sharhlar
            'organic_products': products.filter(quality='or')
        }
        return render(request, 'index.html', context)


def submit_review(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        product_id = request.POST.get('product_id')  # Form yoki URL orqali product_id ni olish

        # Check if product_id is provided
        if not product_id:
            messages.error(request, "Product ID is required.")
            return redirect('home')

        product = get_object_or_404(Product, id=product_id)

        # Ensure the rating and comment are valid
        if not rating or not comment:
            messages.error(request, "Both rating and comment are required.")
            return redirect('home')

        # Save the review to the database
        review = Review(product=product, rating=rating, comment=comment)
        review.save()
        
        messages.success(request, "Review successfully saved!")
        return redirect('home')
    else:
        return redirect('home')

def home(request):
    return render(request, 'index.html')

def jewellery(request):
    return render(request, 'jewellery.html')

def electronic(request):
    return render(request, 'electronic.html')
