from django_filters import DateTimeFromToRangeFilter, FilterSet, MultipleChoiceFilter, ModelMultipleChoiceFilter

from .models import Order, Product, Supplier


class OrderFilterSet(FilterSet):
    created_at = DateTimeFromToRangeFilter()
    status = MultipleChoiceFilter(
        choices=Order.STATUSES
    )

    class Meta:
        model = Order
        fields = ['supplier', 'employee', 'restaurant', 'payment_status', 'status']


class ProductFilterSet(FilterSet):
    supplier = ModelMultipleChoiceFilter(
        queryset=Supplier.objects.all()
    )

    class Meta:
        model = Product
        fields = ['supplier']
