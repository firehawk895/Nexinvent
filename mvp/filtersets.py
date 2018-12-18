from django_filters import DateTimeFromToRangeFilter, FilterSet, MultipleChoiceFilter

from .models import Order


class OrderFilterSet(FilterSet):
    created_at = DateTimeFromToRangeFilter()
    status = MultipleChoiceFilter(
        choices=Order.STATUSES
    )

    class Meta:
        model = Order
        fields = ['supplier', 'employee', 'restaurant', 'payment_status', 'status']
