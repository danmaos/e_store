from django_filters import FilterSet
from .models import Goods


class ProductFilter(FilterSet):
    class Meta:
        model = Goods
        fields = ['name']