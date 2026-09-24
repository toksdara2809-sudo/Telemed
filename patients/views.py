from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from authentication.permissions import patient_required
from .models import PatientProfile
from .forms import UserUpdateForm, PatientProfileForm

@login_required
@patient_required
@transaction.atomic
def edit_patient_profile(request):
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = PatientProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('dashboard_patient')
        else:
            messages.error(request, "Failed to update profile. Please correct the errors.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = PatientProfileForm(instance=profile)
        
    return render(request, 'patients/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
