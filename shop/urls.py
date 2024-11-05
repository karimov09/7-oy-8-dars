from django.urls import path
from shop import views
from .views import ProductListView, ProductDetailView, submit_review, category_products, search_products 

urlpatterns = [
    path('', views.home, name='home'),  
    path('jewellery/', views.jewellery, name='jewellery'), 
    path('electronic/', views.electronic, name='electronic'), 
    path('products/', ProductListView.as_view(), name='product_list'), 
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'), 
    path('submit_review/', submit_review, name='submit_review'),
    path('category/<slug:slug>/', category_products, name='category_products'),  
    path('search/', search_products, name='search_products'),  
]
