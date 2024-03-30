from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils.translation import gettext as _

class Restaurant(models.Model):
    restaurant_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    subscription_token = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.restaurant_code

class Outlet(models.Model):
    outlet_code = models.CharField(max_length=255, primary_key=True)
    addresss = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, to_field='restaurant_code', related_name='restaurant', blank=True, null=True)

    def __str__(self):
        return self.outlet_code

class UserManager(BaseUserManager):
    def create_user(self, email, name, contact_no, address, role, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            contact_no=contact_no,
            address=address,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            name="Restronova",
            contact_no="9810937611",
            address="Bhaktapur, Nepal",
            role="Super Admin",
            password=password
        )
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=32, blank=True, null=True)
    password_reset_token_created_at = models.DateTimeField(blank=True, null=True)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, to_field='outlet_code', related_name='outlet', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='user_users'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='user_users'
    )

    def __str__(self):
        return self.name
