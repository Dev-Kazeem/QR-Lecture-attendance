from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True, null=True,  blank=True, db_index=True)
    username = models.CharField(max_length=60, unique=True, default='temp_user')
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if self.student_id == '':
            self.student_id = None
        super().save(*args, **kwargs)    

    def __str__(self):
        return f"{self.username} - {self.student_id}"