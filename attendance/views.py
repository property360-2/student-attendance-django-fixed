# [attendance/views.py]
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from .models import AttendanceRecord
from .forms import DateSelectForm, AttendanceLineForm
from students.models import Student

@login_required
def attendance_list(request):
    date_str = request.GET.get('date')
    student_id = request.GET.get('student')
    
    # Base queryset: only records created by this user
    qs = AttendanceRecord.objects.filter(created_by=request.user)
    
    selected_date = None
    selected_student = None
    
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            qs = qs.filter(date=selected_date)
        except (ValueError, TypeError):
            messages.warning(request, "Invalid date format provided.")
    
    if student_id:
        try:
            # Enforce ownership check
            selected_student = get_object_or_404(Student, id=student_id, owner=request.user)
            qs = qs.filter(student=selected_student)
        except Exception:
            messages.error(request, "Student not found or access denied.")
            return redirect('attendance:list')
    
    qs = qs.select_related('student').order_by('-date', 'student__last_name')
    
    return render(
        request,
        'attendance/attendance_list.html',
        {
            'records': qs,
            'selected_date': selected_date,
            'selected_student': selected_student,
        },
    )

@login_required
def attendance_mark(request):
    # Enforce ownership: only mark attendance for students YOU own
    students = list(
        Student.objects.filter(is_active=True, owner=request.user).order_by('last_name', 'first_name')
    )
    
    if not students:
        messages.info(request, "You need to add active students before marking attendance.")
        return redirect('students:add')

    num_students = len(students)
    FormSet = formset_factory(AttendanceLineForm, extra=0, min_num=num_students, max_num=num_students)

    if request.method == 'GET':
        date_param = request.GET.get('date')
        if date_param:
            form = DateSelectForm(request.GET)
        else:
            form = DateSelectForm(initial={'date': timezone.localdate()})
        
        if form.is_valid():
            date = form.cleaned_data['date']
        else:
            date = timezone.localdate()
            # If date was invalid (e.g. future), DateSelectForm.clean_date raised error, 
            # but for GET we fall back to today quietly or show form errors.
            if date_param:
                messages.error(request, "Invalid date selected. Falling back to today.")

        existing = {
            r.student_id: r
            for r in AttendanceRecord.objects.filter(
                date=date,
                created_by=request.user,
            )
        }
        
        initial = []
        for s in students:
            record = existing.get(s.id)
            initial.append({
                'student_id': s.id,
                'status': getattr(record, 'status', 'present'),
                'remarks': getattr(record, 'remarks', ''),
                'late_reason': getattr(record, 'late_reason', ''),
            })

        formset = FormSet(initial=initial)
        rows = zip(students, formset.forms)
        
        return render(
            request,
            'attendance/attendance_mark.html',
            {
                'date_form': form,
                'formset': formset,
                'rows': rows,
                'date': date,
            },
        )

    # POST handling
    form = DateSelectForm(request.POST)
    formset = FormSet(request.POST)
    
    date = timezone.localdate() # Default
    if form.is_valid() and formset.is_valid():
        date = form.cleaned_data['date']
        
        # Double check: ensure sid is actually one of the user's students
        allowed_sids = {s.id for s in students}
        
        count = 0
        for f in formset:
            cd = f.cleaned_data
            sid = cd.get('student_id')
            
            if sid in allowed_sids:
                status = cd.get('status', 'present')
                AttendanceRecord.objects.update_or_create(
                    student_id=sid,
                    date=date,
                    defaults={
                        'status': status,
                        'remarks': cd.get('remarks', ''),
                        'late_reason': cd.get('late_reason', '') if status == 'late' else '',
                        'created_by': request.user,
                    },
                )
                count += 1
            else:
                # Security/Validation: Log or handle unauthorized student ID attempt
                pass

        messages.success(request, f"Successfully recorded attendance for {count} students on {date}.")
        return redirect('attendance:list')

    # If we reached here, there were validation errors
    messages.error(request, "Failed to save attendance. Please check the errors below.")
    
    # Safe date fallback for rendering
    try:
        date_val = request.POST.get('date')
        date = datetime.strptime(date_val, '%Y-%m-%d').date() if date_val else timezone.localdate()
    except:
        date = timezone.localdate()

    rows = zip(students, formset.forms)
    return render(
        request,
        'attendance/attendance_mark.html',
        {
            'date_form': form,
            'formset': formset,
            'rows': rows,
            'date': date,
        },
    )
