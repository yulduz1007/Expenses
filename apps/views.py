from django.shortcuts import render
from django.views.generic import CreateView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.models import User, Expense
from apps.serializers import UserRegisterSerializer, ExpensesSerializer, ExpensesListSerializer


# Create your views here.
@extend_schema(tags=['Auth'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['Auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Auth'])
class RegisterCreateView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


@extend_schema(tags=['Expenses'],
               responses=ExpensesListSerializer
               )
class ExpensesListView(ListAPIView):
    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()
        serializer = ExpensesListSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Expenses'])
class ExpensesCreateView(CreateAPIView):
    serializer_class = ExpensesSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance

        response_data = {
            "pk": instance.pk,
            "amount": instance.amount,
            "category": {
                "pk": instance.category.pk,
                "name": instance.category.name,
                "type": instance.category.type,
                "icon": instance.category.icon
            },
            "description": instance.description,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Expenses'])
class ExpensesDeleteView(DestroyAPIView):
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        expense = self.get_object()
        self.perform_destroy(expense)
        return Response({"detail": "Xarajat muvaffaqiyatli o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)
