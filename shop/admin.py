from django.contrib import admin
from .models import Category, Product, Image, Review, Comment


class ImageInline(admin.StackedInline):
    model = Image  
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
    inlines = [ImageInline]  

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')
    list_filter = ('product', 'rating')
    search_fields = ('user__username', 'text')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'created_at', 'rating')
    list_filter = ('product', 'user')
    search_fields = ('user__username', 'text')  
