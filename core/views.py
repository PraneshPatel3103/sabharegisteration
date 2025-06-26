from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import (
    UserProfile, EventDetail, Pradesh, Sant, SabhaOption, DashboardContent
)

# Redirect to registration form
def redirect_to_register(request):
    return redirect('register')

# Registration form logic
def register_view(request):
    pradesh_names = Pradesh.objects.all()
    sant_names = Sant.objects.all()
    sabha_options = SabhaOption.objects.all()

    if request.method == 'POST':
        try:
            name = request.POST['name']
            city = request.POST['city']
            mobile = request.POST['mobile']
            country_code = request.POST['country_code']
            password = request.POST['password']
            re_password = request.POST['re_password']
            pradesh = request.POST['pradesh']
            reference_sant = request.POST['reference_sant']

            

            if password != re_password:
                messages.error(request, "Passwords do not match")
                return redirect('register')

            user = UserProfile.objects.create(
                name=name,
                city=city,
                mobile=mobile,
                country_code=country_code,
                password=password,  # ⚙️ consider hashing later
                pradesh=pradesh,
                reference_sant=reference_sant
            )

            

            return redirect('login')

        except IntegrityError:
            messages.error(request, "Mobile number already registered")

    return render(request, 'core/register.html', {
        'pradesh_names': pradesh_names,
        'sant_names': sant_names,
        'sabha_options': sabha_options
    })

# Login logic
def login_view(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        password = request.POST['password']
        try:
            user = UserProfile.objects.get(mobile=mobile)
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")
        except UserProfile.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, 'core/login.html')

# User dashboard view with admin-managed content
from django.shortcuts import render, redirect
from .models import UserProfile, EventDetail, DashboardContent
from django.utils import timezone

def dashboard_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = UserProfile.objects.get(id=user_id)

    if not user.is_approved:
        return render(request, 'core/waiting_approval.html')

    dashboard_content = DashboardContent.objects.last()

    if request.method == 'POST':
        sabha_name = request.POST.get('sabha_name')
        sabha_date = request.POST.get('sabha_date')

        if sabha_name and sabha_date:
            EventDetail.objects.create(
                user=user,
                sabha_name=sabha_name,
                sabha_date=sabha_date
            )
            return redirect('dashboard')  # Refresh page to show updated list

    user_sabhas = EventDetail.objects.filter(user=user).order_by('-sabha_date')

    return render(request, 'core/data_view.html', {
        'dashboard': dashboard_content,
        'sabhas': user_sabhas  # ✅ Template expects 'sabhas'
    })

# Admin approval
def approve_user(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    return redirect('/admin/')
from django.shortcuts import redirect

def logout_view(request):
    request.session.flush()  # Clears all session data
    return redirect('login')  # Redirects to login page
