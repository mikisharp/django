from rest_framework import serializers
from .models import Category, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # '__all__'
        # fields = '__all__'
        fields = (
                  'name',
                  'id',
                  )

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User,
        fields = (
            'first_name',
            'last_name',
            'email',
        )