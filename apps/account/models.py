#import
from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _




#classes 
class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        
        return self.create_user(email, first_name, last_name, password, **extra_fields)



class UserAccount(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('verified', _('Verified')),
        ('blocked', _('Blocked')),
    ]

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_status = models.CharField(_('Status'), choices=STATUS_CHOICES, default='pending', blank=True, max_length=20)
    is_active = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_verified = models.BooleanField(_('is_verified'), default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(_('admin'), default=False)
    otp = models.CharField(max_length=256, null=True,blank=True)
    activation_key = models.CharField(max_length=150,blank=True,null=True)


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
   
    
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


