from django.urls import path
from . import views

app_name = 'attendance_app'

urlpatterns = [
     path('lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
     path('session/start/',views.start_session, name='start_session'),
     path('session/<int:session_id>/',views.session_qr, name='session_qr'),
     path('session/<int:session_id>/qr-image/',views.get_qr_image, name='get_qr_image'),
     path('session/<int:session_id>/end/',views.end_session, name='end_session'),
     path('attend/<uuid:token>/',views.mark_attendance, name='mark_attendance'),
     path('session/<int:session_id>/students',views.attendance_list, name='attendance_list'),
     path('scan/',views.scan_page, name='scan_page'),


    
     path('session/<int:session_id>/', views.session_detail, name='session_detail'),
     path('session/<int:session_id>/export-csv/', views.export_csv, name='export_csv'),
     path('session/<int:session_id>/export-excel/', views.export_excel, name='export_excel'),
]


