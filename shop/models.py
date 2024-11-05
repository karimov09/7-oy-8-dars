from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

QUALITY = [
    ('or', 'Organic'),
    ('gmo', 'GMO'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi", unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="categories/photos/", null=True, blank=True, verbose_name="Rasmi")
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Ota-kategoriya", related_name="subcategories")

    def __str__(self):
        return f"Sub: {self.name}" if self.parent else self.name

    def send_photo(self):
        return self.photo.url if self.photo else "https://avatars.mds.yandex.net/i?id=7944b3d2cb8a76e3d06265db5b82b258_l-5661780-images-thumbs&n=13"

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ('pk',)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(null=True, blank=True, verbose_name="Mahsulot haqida...")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    discount = models.IntegerField(null=True, blank=True, verbose_name="Chegirma (%)")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Ombordagi soni")
    weight = models.PositiveIntegerField(verbose_name="Vazni")
    made_in = models.CharField(max_length=100, verbose_name="Yetishtirilgan")
    quality = models.CharField(max_length=3, choices=QUALITY, verbose_name="Sifati")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Kategoriya", related_name="products")

    def __str__(self):
        return self.name

    def get_image(self):
        images = self.images.all()
        return images[0].image.url if images else "https://www.nugaedu.gr/style/images/no-image.jpg"

    def get_discount(self):
        '''Chegirmali narxini topish'''
        if self.discount:
            return round((self.price - (self.price * self.discount) / 100), 2)
        return self.price

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ('-pk',)


class Images(models.Model):
    image = models.ImageField(upload_to="products/images/", verbose_name="Rasmi")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot", related_name="images")

    def __str__(self):
        return f"{self.product.name} | {self.image.name}"

    class Meta:
        verbose_name = "Rasm"
        verbose_name_plural = "Rasmlar"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews", verbose_name="Foydalanuvchi")
    text = models.CharField(max_length=1000, verbose_name="Izoh matni")
    full_name = models.CharField(max_length=64, verbose_name="To'liq ismi")
    profession = models.CharField(max_length=100, null=True, verbose_name="Kasbi")
    rating = models.IntegerField(validators=[
        MinValueValidator(1, "Kamida 1 bo'lishi kerak"),
        MaxValueValidator(5, "Eng ko'pi bilan 5 bo'lishi kerak")
    ], verbose_name="Bahosi")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti!")

    def __str__(self):
        return f"{self.full_name} | {self.text[:100]}"

    def get_range(self):
        return range(1, 6)

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Izoh")
    rating = models.IntegerField(validators=[
        MinValueValidator(1, "Kamida 1 bo'lishi kerak"),
        MaxValueValidator(5, "Eng ko'pi bilan 5 bo'lishi kerak")
    ], default=0, verbose_name="Bahosi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return f"{self.user.username} - {self.product} - {self.rating}★"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
