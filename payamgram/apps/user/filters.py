import django_filters as filters

from apps.user.models import User


class UserFilter(filters.FilterSet):
    """
    a custom filter by username.
    """
    username = filters.CharFilter(label='نام کاربری', lookup_expr='istartswith')

    class Meta:
        model = User
        fields = ['username']
