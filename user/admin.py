# from djaa_list_filter.admin import AjaxAutocompleteListFilterModelAdmin
from django.contrib import admin

from apps.user.models import User


# @admin.register(User)
# class PersonAdmin(AjaxAutocompleteListFilterModelAdmin):
#     list_display = ['username', 'email']
#     autocomplete_list_filter = ('username')
#
#     def show_tags(self, obj):
#         return ' , '.join(obj.tags.values_list('name', flat=True))

#
@admin.register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    list_display_links = ['username']
