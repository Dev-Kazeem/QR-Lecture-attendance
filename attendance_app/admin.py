from django.contrib import admin
from .models import Course, LectureSession, Attendance

# Register your models here.
admin.site.register(Course)
admin.site.register(LectureSession)
admin.site.register(Attendance)