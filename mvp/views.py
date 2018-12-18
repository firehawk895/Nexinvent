from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
from rest_framework import viewsets

from .filtersets import OrderFilterSet
from .models import Order

from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('invoice_no', 'supplier__name')
    filter_class = OrderFilterSet

    def get_queryset(self):
        queryset = Order.objects.all()

        return queryset
