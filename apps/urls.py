from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.views import RegisterCreateView, ExpensesCreateView, ExpensesDeleteView, ExpensesListView, ExpenseDetailView, \
    ExpenseUpdateView, BalanceAPIView, CategoryListAPIView

urlpatterns = [
    path('Auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('Auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterCreateView.as_view(), name='register'),

]

urlpatterns += [
    path('expenses/list', ExpensesListView.as_view()),
    path('expenses/detail/<int:pk>', ExpenseDetailView.as_view()),
    path('expenses/create', ExpensesCreateView.as_view()),
    path('expenses/update/<int:pk>', ExpenseUpdateView.as_view()),
    path('expenses/delete/<int:pk>', ExpensesDeleteView.as_view())
]




urlpatterns += [
    path('expenses/balance', BalanceAPIView.as_view()),
]



urlpatterns += [
    path('category/<str:type>', CategoryListAPIView.as_view(), name='category-list'),
]
