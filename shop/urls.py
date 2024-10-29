from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jewellery/', views.jewellery, name='jewellery'),
    path('electronic/', views.electronic, name='electronic'),
]