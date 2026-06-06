from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from .models import Course, LectureSession, Attendance
import qrcode
import base64
from io import BytesIO

def is_lecturer(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_lecturer)
def start_session(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # close any active for session this first
    LectureSession.objects.filter(lecturer=request.user, is_active=True).update(is_active=False)

    session = LectureSession.objects.create(course=course, lecturer=request.user, is_active=True)
    return redirect('attendance_app:session_qr', session_id=session.id) 




@login_required
@user_passes_test(is_lecturer)
def session_qr(request, session_id):
    session = get_object_or_404(LectureSession, id=session_id, lecturer=request.user)
    return render(request, 'attendance/session_qr.html', {'session':session,})




@login_required
@user_passes_test(is_lecturer)
def get_qr_image(request, session_id):
    session = get_object_or_404(LectureSession, id=session_id, lecturer=request.user)

    # Rotate token every time this is called
    session.rotate_token()

    qr_url = request.build_absolute_uri(f"/attend/{session.qr_token}/")
    qr = qrcode.make(qr_url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_b64 = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({
        'qr_b64':qr_b64 ,
        'token_age_sec': (timezone.now() - session.token_created_at).seconds
    })





@login_required
@user_passes_test(is_lecturer)
def end_session(request, session_id):
    session =  get_object_or_404(LectureSession, id=session_id, lecturer=request.user)
    session.is_active = False
    session.save()
    return redirect('attendance_app:start_session', course_id=session.course.id)


@login_required
def scan_page(request):
    return render(request, 'Attendance/scan.html')



@login_required
def mark_attendance(request, token):
    session = get_object_or_404(LectureSession, qr_token=token)
    
    # 1. Check if session is active
    if not session.is_active:
        return render(request, 'attendance/attend_result.html', {'status': 'ended', 'session': session})
    
    # 2. Check token expiry - 2 min window
    if not session.is_token_valid():
        return render(request, 'attendance/attend_result.html', {'status': 'expired', 'session': session})
    
    # 3. Check if user is student, not lecturer
    if request.user.is_staff:
        return HttpResponseForbidden("Lecturers can't mark attendance")
    
    # 4. Check if already marked - prevents double scan
    if Attendance.objects.filter(student=request.user, session=session).exists():
        return render(request, 'attendance/attend_result.html', {'status': 'already', 'session': session})
    
    # 5. All good - create record
    Attendance.objects.create(student=request.user, session=session)
    return render(request, 'attendance/attend_result.html', {'status': 'success', 'session': session})





@login_required
@user_passes_test(is_lecturer)
def attendance_list(request, session_id):
    session = get_object_or_404(LectureSession, id=session_id, lecturer=request.user)
    if request.GET.get('json'):
        count = Attendance.objects.filter(session=session).count()
        return JsonResponse({'count':count})
    records = Attendance.objects.filter(session=session).select_related('student')
    return render(request, 'attendance/attendance_list.html', {'records': records})
