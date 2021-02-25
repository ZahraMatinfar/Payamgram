from rest_framework import serializers

from apps.user.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
