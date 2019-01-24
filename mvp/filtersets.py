from django_filters import DateTimeFromToRangeFilter, FilterSet, MultipleChoiceFilter, ModelMultipleChoiceFilter

from .models import Order, Product, Supplier, Restaurant, Cart, OrderItem


class OrderFilterSet(FilterSet):
    created_at = DateTimeFromToRangeFilter()
    status = MultipleChoiceFilter(
        choices=Order.STATUSES
    )

    class Meta:
        model = Order
        fields = ['supplier', 'employee', 'restaurant', 'payment_status', 'status']


class OrderItemFilterSet(FilterSet):

    class Meta:
        model = OrderItem
        fields = ['order']


class ProductFilterSet(FilterSet):
    supplier = ModelMultipleChoiceFilter(
        queryset=Supplier.objects.all()
    )

    class Meta:
        model = Product
        fields = ['supplier']


class CartFilterSet(FilterSet):
    restaurant = ModelMultipleChoiceFilter(
        queryset=Restaurant.objects.all()
    )

    class Meta:
        model = Cart
        fields = ['restaurant']
