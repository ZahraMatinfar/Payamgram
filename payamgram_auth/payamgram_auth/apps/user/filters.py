import django_filters as filters
from django.contrib.auth.models import User


class UserFilter(filters.FilterSet):
    """
    a custom filter by username.
    """

    username = filters.CharFilter(label='username', lookup_expr='istartswith')

    class Meta:
        model = User
        fields = ['username']
