from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        max_length=200, unique=False,
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=60, unique=True,
    )
    full_name = models.CharField(
        max_length=200, blank=True,
        null=True, verbose_name='ФИО'
    )
    brigades_name = models.CharField(
        max_length=100, blank=True,
        null=True, verbose_name='Название бригады'
    )
    brigades_list = RichTextField(
        max_length=255, blank=True,
        null=True, verbose_name='Список участников бригады'
    )
    brigade_status = models.BooleanField(
        default=False, verbose_name='Бригада на выезде?',
        blank=True,
    )
    company_name = models.CharField(
        max_length=100, blank=True,
        null=True, verbose_name='Название компании'
    )
    address = models.CharField(
        max_length=150, blank=True,
        null=True, verbose_name='Адрес компании'
    )
    phone = models.CharField(
        max_length=50, blank=True,
        null=True, verbose_name='Номер телефона'
    )

    USER_TYPE = (
        ('OPERATOR', 'Operator'),
        ('BRIGADE', 'Brigade'),
        ('CLIENT', 'Client'),
    )
    user_type = models.CharField(max_length=200, choices=USER_TYPE)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
