from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
from rest_framework import viewsets

from .filtersets import OrderFilterSet, ProductFilterSet
from .models import Order, Product

from .serializers import OrderSerializer, ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('invoice_no', 'supplier__name')
    filter_class = OrderFilterSet


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('supplier__name', 'name', 'sku', 'description')
    filter_class = ProductFilterSet
