from django.contrib import admin
from .models import Category, Product, Images, Review, Comment


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
    inlines = [ImageInline]


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
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
