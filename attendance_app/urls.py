from django.urls import path
from . import views

app_name = 'attendance_app'

urlpatterns = [
     path('lecturer/start/<int:course_id>/',views.start_session, name='start_session'),
     path('lecturer/session/<int:session_id>/',views.session_qr, name='session_qr'),
     path('lecturer/session/<int:session_id>/qr-image/',views.get_qr_image, name='get_qr_image'),
     path('lecturer/session/<int:session_id>/end/',views.end_session, name='end_session'),
     path('attend/<uuid:token>/',views.mark_attendance, name='mark_attendance'),
     path('session/<int:session_id>/students',views.attendance_list, name='attendance_list'),
     path('scan/',views.scan_page, name='scan_page'),
]