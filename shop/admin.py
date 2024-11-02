from django.contrib import admin
from .models import Category, Product, Images


class ImageInline(admin.StackedInline):
    model = Images
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    prepopulated_fields = {'slug': ('name',)}
   

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category')
    list_editable = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ImageInline
    ]