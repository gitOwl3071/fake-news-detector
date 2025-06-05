from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Email is required")
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user



class CustomUserModel(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class NewsDetection(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    text = models.TextField()
    detection = models.CharField(max_length=10)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.prediction}"