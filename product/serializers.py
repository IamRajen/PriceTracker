from rest_framework import serializers
from .models import Product, ProductPrice, TrackedProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'title_identifier', 'price', 'rating', 'number_of_reviews', 'seller_name', 'link', 'source']
    
class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'

class ProductPriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'

class TrackedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedProduct
        fields = '__all__'