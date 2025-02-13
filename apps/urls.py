from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import RegisterCreateView, ExpensesCreateView, ExpensesDeleteView, ExpensesListView

urlpatterns = [
    path('Auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('Auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterCreateView.as_view(), name='register'),

    path('Expenses/get', ExpensesListView.as_view(), name='expenses-get'),
    path('Expenses/post', ExpensesCreateView.as_view(), name='expenses-post'),
    path('Expenses/delete/<int:pk>/', ExpensesDeleteView.as_view(), name='expenses-delete'),

]