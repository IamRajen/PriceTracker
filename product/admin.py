from django.contrib import admin
from .models import Product, ProductPrice, TrackedProduct

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(TrackedProduct)
