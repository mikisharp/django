from django.db import models
from django.contrib.auth.base_user import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from typing import Any
from django.contrib import auth

username_validator = UnicodeUsernameValidator()

class UserCustomManager(BaseUserManager):
    use_in_migrations: bool = True
    def _create_user(
        self, username: str, email: str, password: str, **extra_fields
    ) -> object:
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email: str = self.normalize_email(email)
        username: str = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(
        self, username: str, email: str, password: str | None = None, **extra_fields
    ) -> object:
        """
        @type username: object
        @param username:
        @param email:
        @param password:
        @param extra_fields:
        @return:
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    def create_superuser(
        self, username: str, email: str, password: str, **extra_fields
    ) -> object:
        """
        @param username:
        @param email:
        @param password:
        @param extra_fields:
        @return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(username, email, password, **extra_fields)
    def with_perm(
        self,
        perm,
        is_active: bool = True,
        include_superusers: bool = True,
        backend: Any | None = None,
        obj: Any | None = None,
    ):
        """
        @type is_active: object
        @param perm:
        @param is_active:
        @param include_superusers:
        @param backend:
        @param obj:
        @return:
        """
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()
    
class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
   
class User(AbstractBaseUser, PermissionsMixin, TimeMixin):
    """ user class"""
    email = models.EmailField(null=False, unique=True)
    first_name = models.CharField(max_length=255, null=True, default='')
    last_name = models.CharField(max_length=255, null=True, default='')
    username = models.CharField(max_length=255, unique=True, null=False,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserCustomManager()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    
    class Meta:
        db_table = 'user'
        
    def __str__(self):
        return f"{self.first_name}{self.last_name}"
    
# Create your models here.

class Category(TimeMixin):
    name = models.CharField(max_length=255, unique=True, null=False)

    
    class Meta:
        db_table='category'
        
    def __str__(self):
        return f"{self.name}"

class Post(TimeMixin):
    """ Post model """
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    title = models.CharField(null=False, max_length=255)
    subject = models.CharField(null=True, default='No subject', max_length=255)
    description = models.TextField(null=False)
    main_image = models.ImageField(upload_to='post')
    
    class Meta:
        db_table = 'post'
    
    def __str__(self):
        return f"{self.title} {self.created_at.strftime('%d-%m-%Y')}"
    @property 
    def get_image(self):
        if self.main_image:
            return self.main_image.url
        return 'https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg'
    
    