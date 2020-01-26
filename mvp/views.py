from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import api_view, action, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from utility.generics import upload_file_to_s3
from .filtersets import OrderFilterSet, ProductFilterSet, CartFilterSet, OrderItemFilterSet
from .models import Order, Product, Cart, OrderItem

from .serializers import OrderSerializer, OrderSerializerPatch, OrderInstanceSerializer, ProductSerializer, \
    CartSerializer, OrderItemSerializer, \
    CartSerializerPatch, CartSerializerPost, CartSerializerDeleteSupplierWise, SendOrderSerializer, CheckinSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('invoice_no', 'supplier__name')
    filter_class = OrderFilterSet

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = OrderInstanceSerializer
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = OrderSerializerPatch
        return super().update(request, *args, **kwargs)


class AnalyticsOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderInstanceSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = OrderInstanceSerializer
        return super().list(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = OrderItemFilterSet


@api_view(['GET'])
def get_order_aggregates(request):
    restaurant_id = request.query_params.get('restaurant_id', None)
    return Response(Order.objects.get_order_aggregates(restaurant_id))

# Not sure where you can put the associated vendor API, should it be an API view or whatever
"""
something = AssociatedSupplier.objects.filter(restaurant_id=restaurant_id).select_related('supplier')
response = map(lambda x:x.supplier, something)
something like this LOL
"""


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('supplier__name', 'name', 'sku', 'description')
    filter_class = ProductFilterSet


@api_view(['POST'])
@transaction.atomic
def send_orders(request):
    serializer = SendOrderSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    # At this point validation errors have not been raised, or a HTTP 400 would have been sent out
    # Therefore the async sms task can be sent out here
    return Response({}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@transaction.atomic
def checkin(request):
    serializer = CheckinSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@parser_classes((FileUploadParser,))
def upload_file(request):
    if request.data:
        url = upload_file_to_s3(request.data["file"], str(request.data["file"]))
        return Response({"url": url}, status=status.HTTP_201_CREATED)
    else:
        return Response({"non_field_errors": "File content empty"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('supplier__name')
    serializer_class = CartSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = CartFilterSet

    def create(self, request, *args, **kwargs):
        self.serializer_class = CartSerializerPost
        # This is a copy-pasta of the django mixin code
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # I want to return data of the format that CartSerializer specifies
        cart = Cart.objects.get(pk=serializer.data["id"])
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        self.serializer_class = CartSerializerPatch
        # this is a copy-pasta of the django mixin code
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # I want to return data of the format that CartSerializer specifies
        cart = Cart.objects.get(pk=serializer.data["id"])
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_suppliers_cart(self, request):
        self.serializer_class = CartSerializerDeleteSupplierWise
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.perform_delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
