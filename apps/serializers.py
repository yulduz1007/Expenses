from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from apps.models import User, Expense, Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'password']

    def validate_password(self, value):
        return make_password(value)


class ExpensesSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = 'id', 'amount', 'category', 'description'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['category'] = instance.category.name
        return repr


