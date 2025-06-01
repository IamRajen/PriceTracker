
import re

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, ProductPrice, TrackedProduct
from .serializers import ProductSerializer, ProductPriceSerializer, TrackedProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .crawler import Crawler

# Create your views here.
class SearchProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.query_params.get('query')

        if query:
            products = Product.objects.filter(title_identifier__icontains=query)

            if not products:
                products = []
                crawler = Crawler(query)
                crawler_products = crawler.crawl()

                for source, products_list in crawler_products.items():
                    for product in products_list:
                        product_serializer = ProductSerializer(data=product)

                        if product_serializer.is_valid():
                            product_serializer.save()
                            products.append(product_serializer.data)

            return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)
        return Response([])
    
class ProductDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductPriceView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        prices = ProductPrice.objects.filter(product=product)
        serializer = ProductPriceSerializer(prices, many=True)
        return Response(serializer.data)
    
class TrackedProductView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tracked_products = TrackedProduct.objects.filter(user=request.user)
        serializer = TrackedProductSerializer(tracked_products, many=True)
        # track_product_price()
        return Response(serializer.data)
    
    def post(self, request, pk):
        request.data['user'] = request.user.id
        request.data['product'] = pk
        if TrackedProduct.objects.filter(user=request.user, product=pk).exists():
            return Response({'message': 'Product already tracked'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TrackedProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)