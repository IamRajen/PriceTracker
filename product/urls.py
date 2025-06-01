from django.urls import path
from .views import SearchProductView, ProductDetailView, ProductPriceView, TrackedProductView

urlpatterns = [
    path('search/', SearchProductView.as_view(), name='search-product'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('price/<int:pk>/', ProductPriceView.as_view(), name='product-price'),
    path('tracked/', TrackedProductView.as_view(), name='tracked-product'),
    path('tracked/<int:pk>/', TrackedProductView.as_view(), name='tracked-product'),
]