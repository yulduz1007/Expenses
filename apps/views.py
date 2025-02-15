from django.db.models import Sum
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.models import User, Expense, Category
from apps.serializers import UserRegisterSerializer, ExpensesSerializer


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


@extend_schema(tags=['Expenses'])
class ExpensesCreateView(CreateAPIView):
    serializer_class = ExpensesSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Expenses'])
class ExpensesDeleteView(DestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpensesSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = {
            "pk": instance.pk,
            "price": instance.amount,
            "description": instance.description
        }
        instance.delete()
        return response_data


@extend_schema(tags=['Expenses'])
class ExpenseUpdateView(UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpensesSerializer


@extend_schema(tags=['Expenses'])
class ExpenseDetailView(RetrieveAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpensesSerializer


@extend_schema(tags=['Expenses'],
               )
class ExpensesListView(ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpensesSerializer


@extend_schema(tags=['Balance'])
class BalanceAPIView(APIView):
    def get(self, request):
        income_sum = Expense.objects.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expense_sum = Expense.objects.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        balance = income_sum - expense_sum
        return Response({"balance": balance}, status=status.HTTP_200_OK)


@extend_schema(tags=['Category'])
class CategoryListAPIView(APIView):
    def get(self, request, type):
        categories = Category.objects.filter(type=type).values('id', 'name')
        return Response(categories, status=status.HTTP_200_OK)
