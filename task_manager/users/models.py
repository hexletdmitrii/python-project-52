from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, confirm_password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        if confirm_password and password != confirm_password:
            raise ValueError('The confirmed_password field must match the password')
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name=_('Имя пользователя'),
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name=_('Имя'),
        max_length=100,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия'),
        max_length=100,
        null=False,
        blank=False,
    )
    password = models.CharField(
        verbose_name=_('Пароль'),
        max_length=128,
        null=False,
        blank=False,
    )
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff status'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name=_('Groups')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        verbose_name=_('User permissions')
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username
