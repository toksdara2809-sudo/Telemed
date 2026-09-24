from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .forms import PatientSignUpForm

def register_patient(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please check the errors below.")
    else:
        form = PatientSignUpForm()
        
    return render(request, 'authentication/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        if user.role == 'doctor' and not user.is_approved_doctor:
            messages.warning(self.request, "Your doctor account is pending administrator approval.")
            return redirect('login')
        messages.success(self.request, f"Welcome back, {user.first_name or user.username}!")
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
