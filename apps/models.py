from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.db import models
from django.db.models import TextChoices
from django.db.models import CharField

from apps import apps


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, password, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone_number must be set")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'admin')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    class UserRole(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    username = None
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=12, unique=True)
    role = CharField(max_length=10, choices=UserRole.choices, default=UserRole.USER)


class TypeEnum(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'


class Category(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TypeEnum.choices)
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"
