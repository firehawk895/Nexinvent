from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filtersets import OrderFilterSet, ProductFilterSet
from .models import Order, Product

from .serializers import OrderSerializer, ProductSerializer, OrderNewSerializer


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


@api_view(['POST'])
def send_all_orders(request):
    serializer = OrderNewSerializer(data=request.data["data"], many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
