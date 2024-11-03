from django.urls import path
from shop import views
from .views import ProductListView, ProductDetailView, submit_review

urlpatterns = [
    path('', views.home, name='home'),
    path('jewellery/', views.jewellery, name='jewellery'),
    path('electronic/', views.electronic, name='electronic'),
    # path('submit_review/', views.submit_review, name='submit_review'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('submit_review/', submit_review, name='submit_review'),
]


