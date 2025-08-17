from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_date
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from django.shortcuts import render
from .models import StudentRegistration, Class
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date
from .models import StudentRegistration, Class, Batch
from django.shortcuts import render, redirect
from .models import StudentRegistration, Class, Batch
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Staff
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Staff
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Staff
from django.shortcuts import render, get_object_or_404, redirect
from .models import Staff
from .models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet

from textwrap import wrap
from io import StringIO
import os
import csv
import random
import datetime
from django.views.decorators.csrf import csrf_exempt


def home(request):
    privacy_policy = PrivacyPolicy.objects.first()  # or filter by some condition if needed

    return render(request, 'foresight_app/index.html', {'privacy_policy': privacy_policy})
def credit(request):
    return render(request, 'foresight_app/credits.html')
def resources(request):
    privacy_policy = PrivacyPolicy.objects.first()
    posts=Post.objects.all()

    return render(request, 'foresight_app/resources.html',{
        'posts':posts,
        'privacy_policy': privacy_policy

    })

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        errors = []

        # Validate first & last name (letters and spaces only)
        if not re.match(r'^[A-Za-z\s]+$', first_name):
            errors.append("First name should contain only letters and spaces.")
        if not re.match(r'^[A-Za-z\s]+$', last_name):
            errors.append("Last name should contain only letters and spaces.")

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            errors.append("Invalid email address.")

        # Validate phone (optional but must be digits if provided)
        if phone and not re.match(r'^\+?[0-9]{7,15}$', phone):
            errors.append("Phone number must be 7–15 digits (with optional +).")

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Safe ORM (prevents SQL injection automatically)
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                message=message
            )
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')  # Ensure 'contact' URL name is set correctly

    privacy_policy = PrivacyPolicy.objects.first()
    return render(request, 'foresight_app/contact.html', {'privacy_policy': privacy_policy})



def our_team(request):
    privacy_policy = PrivacyPolicy.objects.first()

    return render(request, 'foresight_app/our_team.html',{'privacy_policy': privacy_policy})
def learning_modules(request):
    privacy_policy = PrivacyPolicy.objects.first()

    return render(request, 'foresight_app/learning_modules.html',{'privacy_policy': privacy_policy})


from django.contrib import messages
from django.shortcuts import redirect
from .models import StudentRegistration

import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

def student_registration_view(request):
    if request.method == 'POST':
        try:
            # Get inputs safely
            full_name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            whatsapp = request.POST.get('whatsapp', '').strip()
            father_name = request.POST.get('father_name', '').strip()
            father_phone = request.POST.get('father_phone', '').strip()
            mother_name = request.POST.get('mother_name', '').strip()
            mother_phone = request.POST.get('mother_phone', '').strip()
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            qualification = request.POST.get('qualification')
            course = request.POST.get('course')
            address = request.POST.get('address', '').strip()
            adhaar_number = request.POST.get('adhaar', '').strip()
            photo = request.FILES.get('photo')
            email = request.POST.get('email', '').strip()

            # ---------- VALIDATION ----------
            errors = []

            # Name validation (letters + spaces only)
            name_pattern = r'^[A-Za-z\s]+$'
            if not re.match(name_pattern, full_name):
                errors.append("Name must contain only letters and spaces.")
            if father_name and not re.match(name_pattern, father_name):
                errors.append("Father's name must contain only letters and spaces.")
            if mother_name and not re.match(name_pattern, mother_name):
                errors.append("Mother's name must contain only letters and spaces.")

            # Phone validation (10-digit Indian numbers, starting 6-9)
            phone_pattern = r'^[6-9]\d{9}$'
            for field, value in [("Phone", phone), ("WhatsApp", whatsapp), ("Father phone", father_phone), ("Mother phone", mother_phone)]:
                if value and not re.match(phone_pattern, value):
                    errors.append(f"{field} must be a valid 10-digit Indian mobile number.")

            # Email validation
            try:
                validate_email(email)
            except ValidationError:
                errors.append("Invalid email address.")

            # DOB validation
            if dob:
                parsed_dob = parse_date(dob)
                if not parsed_dob:
                    errors.append("Invalid Date of Birth.")
            
            # File validation (image < 3 MB)
            if photo:
                if photo.size > 3 * 1024 * 1024:
                    errors.append("Photo must be less than 3 MB.")
                if not photo.content_type.startswith('image/'):
                    errors.append("Invalid file type. Only images allowed.")

            # Duplicate checks
            if StudentRegistration.objects.filter(email=email).exists():
                errors.append("Email already exists.")
            if StudentRegistration.objects.filter(phone=phone).exists():
                errors.append("Phone number already exists.")
            if StudentRegistration.objects.filter(whatsapp=whatsapp).exists():
                errors.append("WhatsApp number already exists.")

            # If validation fails
            if errors:
                for error in errors:
                    messages.error(request, error)
                return redirect('home')

            # Academic Info
            college_name = request.POST.get('college_name', '').strip()
            college_year = request.POST.get('college_year', '').strip()
            college_score = request.POST.get('college_score', '').strip()

            school_12 = request.POST.get('school_12', '').strip()
            year_12 = request.POST.get('year_12', '').strip()
            score_12 = request.POST.get('score_12', '').strip()
            school_10 = request.POST.get('school_10', '').strip()
            year_10 = request.POST.get('year_10', '').strip()
            score_10 = request.POST.get('score_10', '').strip()
            achievements = request.POST.get('achievements', '').strip()

            # Work Experience
            company_name = request.POST.get('company_name', '').strip()
            position = request.POST.get('position', '').strip()
            work_from = request.POST.get('work_from')
            work_to = request.POST.get('work_to')

            # ---------- SAVE ----------
            StudentRegistration.objects.create(
                full_name=full_name,
                phone=phone,
                whatsapp=whatsapp,
                father_name=father_name,
                father_phone=father_phone,
                mother_name=mother_name,
                mother_phone=mother_phone,
                gender=gender,
                dob=dob,
                qualification=qualification,
                course=course,
                address=address,
                adhaar_number=adhaar_number,
                photo=photo,
                email=email,
                college_name=college_name,
                college_year=college_year,
                college_score=college_score,
                school_12=school_12,
                year_12=year_12,
                score_12=score_12,
                school_10=school_10,
                year_10=year_10,
                score_10=score_10,
                achievements=achievements,
                company_name=company_name,
                position=position,
                work_from=work_from,
                work_to=work_to
            )

            messages.success(request, 'Registration submitted successfully!')
            return redirect('home')

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('home')

    return redirect('home')





# def dashboard(request):
#     # Check if user is logged in
#     if 'user_id' not in request.session:
#         messages.error(request, "You must log in first.")
#         return redirect('admin_login')

#     # Get enquiry and student search parameters separately
#     enquiry_query = request.GET.get('enquiry_q', '')
#     enquiry_date_from = request.GET.get('enquiry_from', '')
#     enquiry_date_to = request.GET.get('enquiry_to', '')

#     student_query = request.GET.get('student_q', '')
#     student_date_from = request.GET.get('student_from', '')
#     student_date_to = request.GET.get('student_to', '')

#     # Filter Students
#     students = StudentRegistration.objects.all()
#     if student_query:
#         students = students.filter(full_name__icontains=student_query)
#     if student_date_from and student_date_to:
#         students = students.filter(created_at__date__range=[student_date_from, student_date_to])
#     elif student_date_from:
#         students = students.filter(created_at__date__gte=student_date_from)

#     # Filter Enquiries
#     enquiries = Contact.objects.all()
#     if enquiry_query:
#         enquiries = enquiries.filter(first_name__icontains=enquiry_query)
#     if enquiry_date_from and enquiry_date_to:
#         enquiries = enquiries.filter(submitted_at__date__range=[enquiry_date_from, enquiry_date_to])
#     elif enquiry_date_from:
#         enquiries = enquiries.filter(submitted_at__date__gte=enquiry_date_from)

#     posts=Post.objects.all()
#     classs=Class.objects.all()
#     policies = PrivacyPolicy.objects.all()
#     return render(request, 'foresight_app/dashboard.html', {
#         'students': students,
#         'query': student_query,
#         'date_from': student_date_from,
#         'date_to': student_date_to,
#         'enquiries': enquiries,
#         'enquiry_query': enquiry_query,
#         'enquiry_date_from': enquiry_date_from,
#         'enquiry_date_to': enquiry_date_to,
#         'posts':posts,
#         'policies': policies,
#         'class_list':classs
#     })





def export_enquiries_csv(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    enquiries = Contact.objects.all()

    if query:
        enquiries = enquiries.filter(first_name__icontains=query)

    if date_from and date_to:
        enquiries = enquiries.filter(submitted_at__date__range=[date_from, date_to])
    elif date_from:
        enquiries = enquiries.filter(submitted_at__date__gte=date_from)

    # Get today's date and format it as YYYY-MM-DD
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')

    # Prepare CSV response with dynamic filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Enquiry_{today_date}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Submitted At', 'First Name', 'Last Name', 'Email', 'Phone', 'Message', 'Replied'])

    for enquiry in enquiries:
        # Convert the 'replied' field to 'YES' or 'NO'
        replied_status = 'YES' if enquiry.replied else 'NO'
        
        writer.writerow([
            enquiry.submitted_at, 
            enquiry.first_name, 
            enquiry.last_name, 
            enquiry.email, 
            enquiry.phone, 
            enquiry.message, 
            replied_status
        ])

    return response


def export_enquiries_pdf(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('from', '')
    date_to = request.GET.get('to', '')

    enquiries = Contact.objects.all()

    if query:
        enquiries = enquiries.filter(first_name__icontains=query)

    if date_from and date_to:
        enquiries = enquiries.filter(submitted_at__date__range=[date_from, date_to])
    elif date_from:
        enquiries = enquiries.filter(submitted_at__date__gte=date_from)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="enquiries.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Margin calculations
    left_margin = width * 0.02
    right_margin = width * 0.98
    usable_width = width * 0.96

    # Column widths based on % of usable width
    col_widths = [
        usable_width * 0.08,  # Date
        usable_width * 0.25,  # Name
        usable_width * 0.20,  # Email
        usable_width * 0.12,  # Phone
        usable_width * 0.28,  # Message
        usable_width * 0.03   # Replied
    ]

    # Column starting x-positions
    col_x_positions = [left_margin]
    for w in col_widths[:-1]:  # Ignore last because no gap after Replied
        col_x_positions.append(col_x_positions[-1] + w)

    # Draw Header Section with "Foresight"
    def draw_header_section():
        p.setFont("Helvetica-Bold", 14)
        p.drawString(width / 2 - 50, height - 30, "Foresight")

    # Draw the table header
    def draw_table_header():
        p.setFont("Helvetica-Bold", 9)
        headers = ["Date", "Name", "Email", "Phone", "Message", "Replied"]
        for i, header in enumerate(headers):
            p.drawString(col_x_positions[i], height - 50, header)

    # Draw the entire PDF
    draw_header_section()
    draw_table_header()

    y = height - 70
    p.setFont("Helvetica", 8)

    def draw_table_row(enquiry, y_position):
        name = f"{enquiry.first_name} {enquiry.last_name}".strip()
        replied_status = 'YES' if enquiry.replied else 'NO'
        formatted_date = enquiry.submitted_at.strftime('%Y-%m-%d')

        # Prepare field text and wrap according to column width
        fields = [
            (formatted_date, col_widths[0]),
            (name, col_widths[1]),
            (enquiry.email, col_widths[2]),
            (enquiry.phone, col_widths[3]),
            (enquiry.message, col_widths[4]),
            (replied_status, col_widths[5]),
        ]

        # Estimate chars per line roughly (approx 6 pts per character at font size 8)
        field_lines = []
        for text, width_value in fields:
            chars_per_line = int(width_value / 4.5)  # Adjust ratio for neatness
            wrapped = wrap(text or '', width=chars_per_line)
            field_lines.append(wrapped)

        # Find max number of lines needed
        max_lines = max(len(lines) for lines in field_lines)

        # Draw lines
        for line_num in range(max_lines):
            for i, lines in enumerate(field_lines):
                text = lines[line_num] if line_num < len(lines) else ''
                p.drawString(col_x_positions[i], y_position, text)
            y_position -= 12

        # Draw horizontal line
        p.line(left_margin, y_position + 6, right_margin, y_position + 6)

        return y_position - 5

    # Loop through enquiries to add each to the table
    for enquiry in enquiries:
        y = draw_table_row(enquiry, y)
        if y < 80:
            p.showPage()
            draw_header_section()
            draw_table_header()
            y = height - 70

    p.save()
    return response









import csv
from django.http import HttpResponse
from .models import StudentRegistration
import csv
from datetime import datetime
from django.http import HttpResponse
from .models import StudentRegistration

def export_students_csv(request):
    query = request.GET.get('student_q', '')
    date_from = request.GET.get('student_from', '')
    date_to = request.GET.get('student_to', '')

    students = StudentRegistration.objects.all()

    if query:
        students = students.filter(full_name__icontains=query)

    try:
        if date_from and date_to:
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            students = students.filter(created_at__date__range=[df, dt])
        elif date_from:
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            students = students.filter(created_at__date__gte=df)
    except ValueError:
        pass  # Ignore invalid date filters

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Full Name', 'Email', 'Phone', 'WhatsApp',
        'Father Name', 'Father Phone', 'Mother Name', 'Mother Phone',
        'Gender', 'Date of Birth', 'Qualification', 'Course',
        'Address', 'Adhaar Number',
        'College Name', 'College Year', 'College Score',
        'School 12th', 'Year 12th', 'Score 12th',
        'School 10th', 'Year 10th', 'Score 10th',
        'Achievements', 'Created At'
    ])

    for s in students:
        writer.writerow([
            s.full_name or '',
            s.email or '',
            s.phone or '',
            s.whatsapp or '',
            s.father_name or '',
            s.father_phone or '',
            s.mother_name or '',
            s.mother_phone or '',
            s.gender or '',
            s.dob.strftime('%Y-%m-%d') if s.dob else '',
            s.qualification or '',
            s.course or '',
            s.address or '',
            s.adhaar_number or '',
            s.college_name or '',
            s.college_year or '',
            s.college_score or '',
            s.school_12 or '',
            s.year_12 or '',
            s.score_12 or '',
            s.school_10 or '',
            s.year_10 or '',
            s.score_10 or '',
            s.achievements or '',
            s.created_at.strftime('%Y-%m-%d %H:%M:%S') if s.created_at else '',
        ])

    return response


# def export_students_pdf(request):
#     query = request.GET.get('q', '')
#     date_from = request.GET.get('from', '')
#     date_to = request.GET.get('to', '')

#     students = StudentRegistration.objects.all()

#     if query:
#         students = students.filter(full_name__icontains=query)

#     if date_from and date_to:
#         students = students.filter(created_at__date__range=[date_from, date_to])
#     elif date_from:
#         students = students.filter(created_at__date__gte=date_from)

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="students.pdf"'

#     p = canvas.Canvas(response, pagesize=A4)
#     width, height = A4

#     def draw_header():
#         p.setFont("Helvetica-Bold", 16)
#         p.drawString(180, height - 50, "Registered Students")

#         # Date range info
#         p.setFont("Helvetica", 10)
#         date_info = f"From: {date_from or 'All'}   To: {date_to or 'Latest'}"
#         p.drawString(40, height - 65, date_info)

#         # Column headings
#         p.setFont("Helvetica-Bold", 10)
#         p.drawString(40, height - 80, "Full Name")
#         p.drawString(150, height - 80, "Email")
#         p.drawString(280, height - 80, "Phone")
#         p.drawString(350, height - 80, "Course")
#         p.drawString(430, height - 80, "Date")

#     draw_header()
#     y = height - 100
#     p.setFont("Helvetica", 10)

#     for s in students:
#         p.drawString(40, y, s.full_name)
#         p.drawString(150, y, s.email)
#         p.drawString(280, y, str(s.phone))
#         p.drawString(350, y, s.course)
#         p.drawString(430, y, s.created_at.strftime('%Y-%m-%d'))
#         y -= 20

#         if y < 50:
#             p.showPage()
#             draw_header()
#             p.setFont("Helvetica", 10)
#             y = height - 100

#     p.save()
#     return response











# def enquiry_dashboard(request):
#     query = request.GET.get('q', '')
#     date_from = request.GET.get('from', '')
#     date_to = request.GET.get('to', '')
    
#     enquiries = Contact.objects.all()
    
#     if query:
#         enquiries = enquiries.filter(first_name__icontains=query) | enquiries.filter(last_name__icontains=query)
    
#     if date_from:
#         enquiries = enquiries.filter(submitted_at__gte=date_from)
    
#     if date_to:
#         enquiries = enquiries.filter(submitted_at__lte=date_to)
    
#     return render(request, 'enquiry_dashboard.html', {
#         'enquiries': enquiries,
#         'query': query,
#         'date_from': date_from,
#         'date_to': date_to
#     })

def toggle_replied(request):
    if request.method == 'POST':
        enquiry_id = request.POST.get('id')
        replied_status = request.POST.get('replied') == 'true'
        
        enquiry = Contact.objects.get(id=enquiry_id)
        enquiry.replied = replied_status
        enquiry.save()
        
        return JsonResponse({'status': 'success', 'replied': enquiry.replied})
    
    return JsonResponse({'status': 'fail'}, status=400)


def admission(request):
    privacy_policy = PrivacyPolicy.objects.first()

    return render(request, 'foresight_app/admission.html',{'privacy_policy': privacy_policy})




#################################################### admin dashboard section #######################################################


def register_user(request):
    if request.method == 'POST' and 'register' in request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User_reg.objects.exists():
            messages.error(request, "An admin is already registered. Only one admin allowed.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        elif User_reg.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        elif User_reg.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'register', 'form_type': 'register'})
        else:
            hashed_password = make_password(password)
            User_reg.objects.create(username=username, email=email, password=hashed_password)
            messages.success(request, "Registration successful. You can now log in.")
            return render(request, 'foresight_app/reg&login.html', {'active_tab': 'login', 'form_type': 'login'})

    return render(request, 'foresight_app/reg&login.html')



def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User_reg.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('enquiries')
            else:
                messages.error(request, "Invalid email or password.")
        except User_reg.DoesNotExist:
            messages.error(request, "Invalid email or password.")

        return render(request, 'foresight_app/reg&login.html', {'active_tab': 'login'})

    return render(request, 'foresight_app/reg&login.html')

def logout_user(request):
    request.session.flush()
    return redirect('admin_login')



def admin_forget(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            user = User_reg.objects.first()  # Only ONE user (admin) is there
            email = user.email
        except User_reg.DoesNotExist:
            user = None
            email = None

        if action == 'send_otp':
            if user:
                otp = random.randint(100000, 999999)
                request.session['reset_email'] = email
                request.session['otp'] = str(otp)

                send_mail(
                    subject="Foresight Password Reset OTP",
                    message=f"Your OTP is {otp}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
                messages.success(request, "OTP sent to your registered email.")
            else:
                messages.error(request, "No admin user found.")

        elif action == 'verify_otp':
            otp = request.POST.get('otp')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
            elif otp != request.session.get('otp'):
                messages.error(request, "Invalid OTP.")
            else:
                try:
                    user = User_reg.objects.get(email=request.session.get('reset_email'))
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, "Password reset successful. You may now log in.")
                    del request.session['reset_email']
                    del request.session['otp']
                    return redirect('admin_login')
                except User_reg.DoesNotExist:
                    messages.error(request, "User not found.")

    return render(request, 'foresight_app/forget.html', {'otp_sent': True if request.session.get('otp') else False})

from functools import wraps
from django.shortcuts import redirect

def login_required_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('admin_login')  # your login view name
        return view_func(request, *args, **kwargs)
    return wrapper


# enquiries section
@login_required_admin
def view_enquiries(request):
    # Get enquiry and student search parameters separately
    enquiry_query = request.GET.get('enquiry_q', '')
    enquiry_date_from = request.GET.get('enquiry_from', '')
    enquiry_date_to = request.GET.get('enquiry_to', '')
    # Filter Enquiries
    enquiries = Contact.objects.all()
    if enquiry_query:
        enquiries = enquiries.filter(first_name__icontains=enquiry_query)
    if enquiry_date_from and enquiry_date_to:
        enquiries = enquiries.filter(submitted_at__date__range=[enquiry_date_from, enquiry_date_to])
    elif enquiry_date_from:
        enquiries = enquiries.filter(submitted_at__date__gte=enquiry_date_from)
        
    return render(request, 'foresight_app/dashboard/enquiries_admin.html', {     
        'enquiries': enquiries,
        'enquiry_query': enquiry_query,
        'enquiry_date_from': enquiry_date_from,
        'enquiry_date_to': enquiry_date_to,})

@login_required_admin
@csrf_exempt
def update_replied(request, pk):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            contact = Contact.objects.get(pk=pk)
            contact.replied = data.get('replied', False)
            contact.save()
            return JsonResponse({"success": True})
        except Contact.DoesNotExist:
            return JsonResponse({"success": False, "error": "Enquiry not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

from django.http import JsonResponse
from .models import Contact  # adjust if your model name is different
@login_required_admin
def get_enquiry(request, pk):
    try:
        enquiry = Contact.objects.get(pk=pk)
        return JsonResponse({
            "id": enquiry.id,
            "first_name": enquiry.first_name,
            "last_name": enquiry.last_name,
            "email": enquiry.email,
            "phone": enquiry.phone,
            "message": enquiry.message,
            "date": enquiry.submitted_at.strftime("%B %d, %Y"),
            "replied": enquiry.replied,
        })
    except Contact.DoesNotExist:
        return JsonResponse({"error": "Enquiry not found."}, status=404)
@login_required_admin
def base_dash(request):
    policies = PrivacyPolicy.objects.all()

    return render(request, 'foresight_app/dashboard/base.html',{'policies': policies})
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.dateparse import parse_date
from .models import StudentRegistration, Class, Batch
from collections import defaultdict
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import StudentRegistration, Class, Batch, AdmittedStudent
from django.contrib.auth.decorators import login_required

@login_required_admin
def assign_students_toclass(request):
    # Only admitted students
    students = StudentRegistration.objects.filter(admittedstudent__admitted=True)
    classes = Class.objects.all()

    course_filter = request.GET.get('course')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    selected_batch = request.POST.get('batch') or request.GET.get('batch')

    if course_filter:
        students = students.filter(course=course_filter)

    if from_date:
        students = students.filter(created_at__date__gte=parse_date(from_date))

    if to_date:
        students = students.filter(created_at__date__lte=parse_date(to_date))

    # All current assignments
    assignments = Batch.objects.all()

    # Assign students to classes based on checkbox selection
    if request.method == 'POST' and selected_batch:
        count = 0
        for student in students:
            assigned = False
            for class_index, cls in enumerate(classes):
                checkbox_name = f'class{class_index}_{student.id}'
                if checkbox_name in request.POST:
                    Batch.objects.filter(student=student).delete()  # Clear previous
                    Batch.objects.create(batch=selected_batch, class_name=cls, student=student)
                    count += 1
                    assigned = True
                    break
            if not assigned:
                Batch.objects.filter(student=student).delete()

        if count:
            messages.success(request, f"{count} student(s) successfully updated.")
        else:
            messages.info(request, "No new assignments made.")
        return redirect('assign_students_toclass')

    return render(request, 'foresight_app/dashboard/assign_students_toclass.html', {
        'students': students,
        'classes': classes,
        'assignments': assignments,
        'selected_course': course_filter,
        'from_date': from_date,
        'to_date': to_date,
        'selected_batch': selected_batch,
    })



# Post section
@login_required_admin
def view_post(request):
    posts=Post.objects.all()
    return render(request, 'foresight_app/dashboard/posts_admin.html', {'posts':posts})
@login_required_admin  
def post_create(request):
    if request.method == 'POST':
        heading = request.POST.get('heading')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if not heading or not content or not image:
            return HttpResponseBadRequest("Missing required fields.")

        Post.objects.create(heading=heading, content=content, image=image)
        return redirect('posts')

    return render(request, 'foresight_app/dashboard/posts_admin.html')


@login_required_admin
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.heading = request.POST.get('heading')
        post.content = request.POST.get('content')

        new_image = request.FILES.get('image')
        if new_image:
            # Delete the old image if it exists
            if post.image and os.path.isfile(post.image.path):
                os.remove(post.image.path)

            post.image = new_image

        post.save()
        return redirect('posts')

    return render(request, 'foresight_app/dashboard/posts_admin.html', {'post': post})
@login_required_admin
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        # Delete the image file first
        if post.image and os.path.isfile(post.image.path):
            os.remove(post.image.path)

        post.delete()
        return redirect('posts')

    return render(request, 'foresight_app/dashboard/posts_admin.html', {'post': post})


# Privacy Policy section
@login_required_admin
def view_privacy_policy(request):
    policies = PrivacyPolicy.objects.all()

    return render(request, 'foresight_app/dashboard/privacy_policy_admin.html', {'policies': policies})
@login_required_admin
def add_privacy_policy(request):
    if request.method == 'POST':
        policy_text = request.POST.get('policy')
        if policy_text:
            PrivacyPolicy.objects.create(policy=policy_text)
    return redirect('privacy')
@login_required_admin
def edit_privacy_policy(request, pk):
    policy = get_object_or_404(PrivacyPolicy, pk=pk)
    if request.method == 'POST':
        updated_text = request.POST.get('policy')
        if updated_text:
            policy.policy = updated_text
            policy.save()
    return redirect('privacy')
@login_required_admin
def delete_privacy_policy(request, pk):
    policy = get_object_or_404(PrivacyPolicy, pk=pk)
    policy.delete()
    return redirect('privacy')

# class section
@login_required_admin
def view_class(request):

    classs=Class.objects.all()
    return render(request, 'foresight_app/dashboard/add_class.html', {'class_list':classs})
from django.shortcuts import render, get_object_or_404
from .models import Class, Batch

import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str

import csv
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.shortcuts import render, get_object_or_404
from .models import Class, Batch
from django.contrib.auth.decorators import login_required

@login_required_admin
def students_in_class(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)
    batch_entries = Batch.objects.filter(class_name=selected_class).select_related('student')
    students = [batch.student for batch in batch_entries]

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=students_in_{selected_class.name}.csv'

        writer = csv.writer(response)

        # ✅ CSV Header (must match fields below)
        writer.writerow([
            'Full Name', 'Email', 'Phone', 'Course', 'WhatsApp',
            'Father Name', 'Father Phone', 'Mother Name', 'Mother Phone',
            'Gender', 'Date of Birth', 'Qualification', 'Address',
            'College Name', 'College Year', 'College Score',
            'School (12th)', 'Score (12th)', 'School (10th)',
            'Year (10th)', 'Score (10th)', 'Registered Date'
        ])

        # ✅ CSV Rows
        for student in students:
            writer.writerow([
                smart_str(student.full_name),
                smart_str(student.email),
                smart_str(student.phone),
                smart_str(student.course),
                smart_str(student.whatsapp),
                smart_str(student.father_name),
                smart_str(student.father_phone),
                smart_str(student.mother_name),
                smart_str(student.mother_phone),
                smart_str(student.gender),
                smart_str(student.dob),
                smart_str(student.qualification),
                smart_str(student.address),
                smart_str(student.college_name),
                smart_str(student.college_year),
                smart_str(student.college_score),
                smart_str(student.school_12),
                smart_str(student.score_12),
                smart_str(student.school_10),
                smart_str(student.year_10),
                smart_str(student.score_10),
                student.created_at.strftime('%Y-%m-%d') if student.created_at else ''
            ])

        return response

    return render(request, 'foresight_app/dashboard/students_in_class.html', {
        'students': students,
        'class_name': selected_class.name
    })


@login_required_admin
def add_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('name')
        if class_name:
            Class.objects.create(name=class_name)
    return redirect('class')
@login_required_admin
def edit_class(request, pk):
    name = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        updated_name = request.POST.get('name')
        if updated_name:
            name.name = updated_name
            name.save()
    return redirect('class')
@login_required_admin
def delete_class(request, pk):
    name = get_object_or_404(Class, pk=pk)
    name.delete()
    return redirect('class')
@login_required_admin
def view_students(request):
    student_query = request.GET.get('student_q', '')
    student_date_from = request.GET.get('student_from', '')
    student_date_to = request.GET.get('student_to', '')

    students = StudentRegistration.objects.all()

    if student_query:
        students = students.filter(full_name__icontains=student_query)
    if student_date_from and student_date_to:
        students = students.filter(created_at__date__range=[student_date_from, student_date_to])
    elif student_date_from:
        students = students.filter(created_at__date__gte=student_date_from)

    context = {
        'students': students,
        'query': student_query,
        'date_from': student_date_from,
        'date_to': student_date_to,
    }
    return render(request, 'foresight_app/dashboard/registered_students.html', context)

@login_required_admin
def edit_student(request, student_id):
    student = get_object_or_404(StudentRegistration, id=student_id)

    if request.method == "POST":
        student.full_name = request.POST.get("full_name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.whatsapp = request.POST.get("whatsapp")
        student.father_name = request.POST.get("father_name")
        student.father_phone = request.POST.get("father_phone")
        student.mother_name = request.POST.get("mother_name")
        student.mother_phone = request.POST.get("mother_phone")
        student.gender = request.POST.get("gender")
        student.dob = request.POST.get("dob")
        student.qualification = request.POST.get("qualification")
        student.course = request.POST.get("course")
        student.address = request.POST.get("address")

        # Academic Info
        student.college_name = request.POST.get("college_name")
        student.college_year = request.POST.get("college_year")
        student.college_score = request.POST.get("college_score")
        student.school_12 = request.POST.get("school_12")
        student.year_12 = request.POST.get("year_12")
        student.score_12 = request.POST.get("score_12")
        student.school_10 = request.POST.get("school_10")
        student.year_10 = request.POST.get("year_10")
        student.score_10 = request.POST.get("score_10")
        student.achievements = request.POST.get("achievements")

        student.save()
        return redirect('all_students')

    return redirect('all_students')

@login_required_admin
def student_details_json(request, student_id):
    try:
        student = StudentRegistration.objects.get(id=student_id)
        data = {
            'full_name': student.full_name,
            'email': student.email,
            'phone': str(student.phone) if student.phone else '',
            'whatsapp': str(student.whatsapp) if student.whatsapp else '',
            'father_name': student.father_name,
            'father_phone': str(student.father_phone) if student.father_phone else '',
            'mother_name': student.mother_name,
            'mother_phone': str(student.mother_phone) if student.mother_phone else '',
            'gender': student.gender,
            'dob': student.dob.strftime('%Y-%m-%d') if student.dob else '',
            'qualification': student.qualification,
            'course': student.course,
            'address': student.address,
            'adhaar_number': student.adhaar_number,
            'photo': student.photo.url if student.photo else '',

            # Academic Info
            'college_name': student.college_name,
            'college_year': student.college_year,
            'college_score': student.college_score,
            'school_12': student.school_12,
            'year_12': student.year_12,
            'score_12': student.score_12,
            'school_10': student.school_10,
            'year_10': student.year_10,
            'score_10': student.score_10,
            'achievements': student.achievements,

            # Work Experience
            'company_name': student.company_name,
            'position': student.position,
            'work_from': student.work_from,
            'work_to': student.work_to,

            # Timestamp
            'created_at': student.created_at.strftime('%Y-%m-%d %H:%M:%S') if student.created_at else '',
        }
        return JsonResponse(data)
    except StudentRegistration.DoesNotExist:
        raise Http404("Student not found")

@login_required_admin
def delete_student(request, pk):
    student = get_object_or_404(StudentRegistration, pk=pk)

    # Check if the student has a profile picture and delete it
    if student.photo:
        # Get the path to the image and delete it
        image_path = student.photo.path
        if os.path.exists(image_path):
            default_storage.delete(image_path)

    # Now delete the student record
    student.delete()

    return redirect('all_students')

# staff section


@login_required_admin
def staff_management(request):
    staff_list = Staff.objects.all()
    
    # For editing
    edit_id = request.GET.get('edit')
    staff_to_edit = Staff.objects.filter(id=edit_id).first() if edit_id else None

    context = {
        'staff_list': staff_list,
        'staff_to_edit': staff_to_edit,
    }
    return render(request, 'foresight_app/dashboard/add_staff.html', context)

@login_required_admin
def create_or_update_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('id')
        name = request.POST.get('name')
        qualification = request.POST.get('qualification')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        salary = request.POST.get('salary')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')

        if staff_id:
            # Updating existing staff
            staff = get_object_or_404(Staff, id=staff_id)

            # Check for email or mobile conflict (excluding current staff)
            if Staff.objects.filter(Q(email=email) | Q(mobile=mobile)).exclude(id=staff_id).exists():
                messages.error(request, "Email or Mobile already exists.")
                return redirect(f"/staff/?edit={staff_id}")

            staff.name = name
            staff.qualification = qualification
            staff.mobile = mobile
            staff.email = email
            staff.salary = salary
            if password:
                staff.password = password
            if photo:
                staff.photo = photo
            try:
                staff.save()
                messages.success(request, "Staff updated successfully.")
            except IntegrityError:
                messages.error(request, "Error updating staff.")
                return redirect(f"/staff/?edit={staff_id}")
        else:
            # Creating new staff
            if Staff.objects.filter(Q(email=email) | Q(mobile=mobile)).exists():
                messages.error(request, "Email or Mobile already exists.")
                return redirect('staff_management')

            try:
                Staff.objects.create(
                    name=name,
                    qualification=qualification,
                    mobile=mobile,
                    email=email,
                    salary=salary,
                    password=password,
                    photo=photo
                )
                messages.success(request, "Staff added successfully.")
            except IntegrityError:
                messages.error(request, "Error adding staff.")
                return redirect('staff_management')

    return redirect('staff_management')

@login_required_admin
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('staff_management')
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import StudentRegistration, Batch

@login_required_admin
def set_student_passwords(request):
    # Get distinct batches from the Batch model
    batches = Batch.objects.values_list('batch', flat=True).distinct()
    selected_batch = request.GET.get('batch')

    students = []
    if selected_batch:
        # Get student IDs under selected batch
        student_ids = Batch.objects.filter(batch=selected_batch).values_list('student_id', flat=True)
        students = StudentRegistration.objects.filter(id__in=student_ids)

    if request.method == 'POST' and selected_batch:
        for student in students:
            password = request.POST.get(f'password_{student.id}')
            if password:
                student.password = make_password(password)   
                student.save()
        messages.success(request, "Passwords updated successfully.")
        return redirect('set_student_passwords')  # Update this to your actual URL name

    return render(request, 'foresight_app/dashboard/set_student_passwords.html', {
        'students': students,
        'batches': batches,
        'selected_batch': selected_batch,
    })


from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from .models import Class, Batch, StudentRegistration, Attendance
@login_required_admin
def all_classes(request):
    all_class = Class.objects.all()
    
    return render(request, 'foresight_app/dashboard/attendance_class_list.html',{'all_class': all_class})

@login_required_admin
def view_class_attendance(request, class_id):
    selected_class = get_object_or_404(Class, id=class_id)

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    # Students in the selected class
    student_ids = Batch.objects.filter(class_name=selected_class).values_list('student_id', flat=True)
    students = StudentRegistration.objects.filter(id__in=student_ids)

    # Attendance filtering
    attendance_qs = Attendance.objects.filter(student__in=students)
    if from_date:
        attendance_qs = attendance_qs.filter(date__gte=parse_date(from_date))
    if to_date:
        attendance_qs = attendance_qs.filter(date__lte=parse_date(to_date))

    # Unique sorted dates
    dates = sorted(set(a.date for a in attendance_qs if a.date))

    # Build a flat list of records for easy lookup in template
    attendance_records = []
    for student in students:
        row = {"student": student, "records": []}
        for date in dates:
            att = attendance_qs.filter(student=student, date=date).first()
            row["records"].append(att)
        attendance_records.append(row)

    return render(request, "foresight_app/dashboard/class_attendance_view.html", {
        "selected_class": selected_class,
        "attendance_records": attendance_records,
        "dates": dates,
        "from_date": from_date,
        "to_date": to_date,
    })

from django.shortcuts import render, redirect
from .models import AdmittedStudent, StudentRegistration
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required_admin
def manage_admissions(request):
    # Handle filter inputs
    course = request.GET.get('course')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Base queryset
    students = StudentRegistration.objects.all()

    # Apply filters if provided
    if course:
        students = students.filter(course=course)

    if from_date:
        students = students.filter(created_at__date__gte=from_date)

    if to_date:
        students = students.filter(created_at__date__lte=to_date)

    # POST: Save admitted status
    if request.method == "POST":
        admitted_ids = request.POST.getlist('admitted_ids')
        AdmittedStudent.objects.all().update(admitted=False)

        for student_id in admitted_ids:
            student_obj, created = AdmittedStudent.objects.get_or_create(student_id=student_id)
            student_obj.admitted = True
            student_obj.save()

        return redirect('manage_admissions')

    admitted_students = AdmittedStudent.objects.filter(admitted=True).values_list('student_id', flat=True)

    return render(request, 'foresight_app/dashboard/manage_admissions.html', {
        'students': students,
        'admitted_ids': admitted_students,
        'selected_course': course,
        'from_date': from_date,
        'to_date': to_date,
        'courses': StudentRegistration.objects.values_list('course', flat=True).distinct()
    })

################################### teacher dashboard section ###################################
from django.db.models import Q

from django.contrib.auth.hashers import check_password

def login_staff(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Staff.objects.get(email=email)
            if check_password(password, user.password):
                request.session['staff_id'] = user.id
                request.session['username'] = user.email
                return redirect('teacher_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except Staff.DoesNotExist:  # ✅ FIXED HERE
            messages.error(request, "Invalid email or password.")

        return render(request, 'foresight_app/login_staff.html')

    return render(request, 'foresight_app/login_staff.html')


def logout_staff(request):
    request.session.flush()
    return redirect('login_staff')



from functools import wraps
from django.shortcuts import redirect

def login_required_staff(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('staff_id'):
            return redirect('login_staff')  # your login view name
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_staff
def teacher_dashboard(request):
    all_class = Class.objects.all()
    
    return render(request, 'foresight_app/dashboard/teacher_dashboard.html',{'all_class': all_class})

def Students(request, class_id):
    class_obj = Class.objects.get(id=class_id)

    current_year = timezone.now().year
    # Get all batches for this class that match current year
    batches = Batch.objects.filter(
        Q(batch__icontains=str(current_year)),
        class_name_id=class_id
    )

    # Get all students in those batches
    students = StudentRegistration.objects.filter(batch__in=batches)

    return render(request, 'foresight_app/dashboard/class.html', {'students': students,'class_name': class_obj.name})

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Attendance, StudentRegistration

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudentRegistration, Attendance
import json

@csrf_exempt
def save_attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data.get("date")
        period = data.get("period")
        attendance_list = data.get("attendance")

        for entry in attendance_list:
            student_id = entry["student_id"]
            present = entry["present"]
            student = StudentRegistration.objects.get(id=student_id)

            attendance, _ = Attendance.objects.get_or_create(student=student, date=date)

            if period == "Period 1":
                attendance.perid_1 = present
            elif period == "Period 2":
                attendance.perid_2 = present
            elif period == "Period 3":
                attendance.perid_3 = present
            elif period == "Period 4":
                attendance.perid_4 = present

            attendance.save()

        return JsonResponse({"message": "Attendance saved successfully!"})
    
    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def get_attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data.get("date")
        period = data.get("period")
        student_ids = data.get("student_ids", [])

        results = []

        for sid in student_ids:
            try:
                record = Attendance.objects.get(student_id=sid, date=date)
                is_present = getattr(record, f"perid_{period.split()[-1]}", False)
                results.append({ "student_id": sid, "present": is_present })
            except Attendance.DoesNotExist:
                results.append({ "student_id": sid, "present": False })

        return JsonResponse({ "data": results })

    return JsonResponse({"error": "Invalid request"}, status=400)







################################### Student dashboard section ###################################

def login_student(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = StudentRegistration.objects.get(email=email)
            if check_password(password, user.password):
                request.session['student_id'] = user.id
                request.session['username'] = user.email
                return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        except StudentRegistration.DoesNotExist:  # ✅ FIXED HERE
            messages.error(request, "Invalid email or password.")

        return render(request, 'foresight_app/login_student.html')

    return render(request, 'foresight_app/login_student.html')


def logout_student(request):
    request.session.flush()
    return redirect('login_student')



from functools import wraps
from django.shortcuts import redirect

def login_required_student(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('student_id'):
            return redirect('login_student')  # your login view name
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_student
def student_attendance_view(request):
    student_id = request.session.get('student_id')
    student = StudentRegistration.objects.get(id=student_id)

    # Sort by date in descending order (latest first)
    attendance_records = Attendance.objects.filter(
        student=student,
        date__isnull=False
    ).order_by('date')

    return render(request, 'foresight_app/dashboard/student_dashboard.html', {
        'attendance_records': attendance_records
    })
