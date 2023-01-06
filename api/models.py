from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


USER_ROLES = [
    ('SM', 'SM'),
]


# Create your CustomUserManager here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, first_name, last_name, role, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')
        if not username:
            raise ValueError('Username is not provided')
        if not role:
            raise ValueError('Role is not provided')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            role = role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, first_name, last_name, role, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(username, email, password, first_name, last_name, role, **extra_fields)

    def create_superuser(self, username, email, password, first_name, last_name, role, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(username, email, password, first_name, last_name, role, **extra_fields)


# Create your User Model here.
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=254, db_index=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=USER_ROLES)
    avatar = models.ImageField(upload_to='avatars/')

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'role']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
