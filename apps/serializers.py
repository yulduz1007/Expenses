from django.contrib.auth.hashers import make_password
from rest_framework.relations import PrimaryKeyRelatedField
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
    category = CategorySerializer(read_only=True)
    category_id = PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category', 'category_id', 'description', 'type']



