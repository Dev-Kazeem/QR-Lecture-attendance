from django.db import models

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import uuid


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, limit_choices_to={'is_staff': True})
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    

class LectureSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff':True})
    date = models.DateTimeField(auto_now_add=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    token_created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    TOKEN_LIFETIME_SEC = 45 # qr refresh every 45 seconds
    SCAN_WINDOW_SEC = 120  # student can scan within two minute of token creation

    def rotate_token(self):
         self.qr_token = uuid.uuid4()
         self.token_created_at = timezone.now()
         self.save(update_fields=['qr_token', 'token_created_at'])

    def is_token_valid(self):
         if not self.is_active:
              return False
         age = timezone.now() - self.token_created_at
         return age.total_seconds() < self.SCAN_WINDOW_SEC     


    def __str__(self):
        return f"{self.course.code} - {self.date.strftime('%Y-%m-%d  %H:%M')}"
    


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(LectureSession, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together =('student', 'session')
        ordering = ['-timestamp']

    def __str__(self):
            return f"{self.student.username} - {self.session}"

