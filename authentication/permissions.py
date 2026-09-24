from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []
    
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        if user.role in self.allowed_roles:
            if user.role == 'doctor' and not user.is_approved_doctor:
                return False
            return True
        return False
        
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.request.user.role == 'doctor' and not self.request.user.is_approved_doctor:
            messages.warning(self.request, "Your doctor account is pending administrator approval.")
            return redirect('login')
        messages.error(self.request, "Access Denied: You do not have the required permissions.")
        return redirect('dashboard_home')

class PatientRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['patient']

class DoctorRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['doctor']

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['admin']


# Decorators for function-based views
def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role == 'patient' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access Denied: Patient role required.")
        return redirect('dashboard_home')
    return wrapper

def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if (request.user.role == 'doctor' and request.user.is_approved_doctor) or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        if request.user.role == 'doctor' and not request.user.is_approved_doctor:
            messages.warning(request, "Your doctor account is pending administrator approval.")
            return redirect('login')
        messages.error(request, "Access Denied: Approved Doctor role required.")
        return redirect('dashboard_home')
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role == 'admin' or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Access Denied: Administrator role required.")
        return redirect('dashboard_home')
    return wrapper
