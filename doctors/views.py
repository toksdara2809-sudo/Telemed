from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from authentication.permissions import doctor_required
from .models import DoctorProfile, DoctorAvailability
from .forms import DoctorUserUpdateForm, DoctorProfileForm, DoctorAvailabilityForm

@login_required
@doctor_required
@transaction.atomic
def edit_doctor_profile(request):
    profile = get_object_or_404(DoctorProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = DoctorUserUpdateForm(request.POST, instance=request.user)
        profile_form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your doctor profile has been updated successfully.")
            return redirect('dashboard_doctor')
        else:
            messages.error(request, "Failed to update profile. Please correct the errors.")
    else:
        user_form = DoctorUserUpdateForm(instance=request.user)
        profile_form = DoctorProfileForm(instance=profile)
        
    return render(request, 'doctors/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@doctor_required
def manage_availability(request):
    profile = get_object_or_404(DoctorProfile, user=request.user)
    availabilities = DoctorAvailability.objects.filter(doctor=profile).order_by('day_of_week', 'start_time')
    
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = profile
            # Check for overlapping slot
            # Simple check: start_time < end_time
            if slot.start_time >= slot.end_time:
                messages.error(request, "End time must be after start time.")
            else:
                try:
                    slot.save()
                    messages.success(request, "Availability slot added successfully.")
                    return redirect('manage_availability')
                except Exception as e:
                    messages.error(request, "This availability slot already exists.")
        else:
            messages.error(request, "Invalid slot details.")
    else:
        form = DoctorAvailabilityForm()
        
    return render(request, 'doctors/manage_availability.html', {
        'availabilities': availabilities,
        'form': form
    })

@login_required
@doctor_required
def delete_availability(request, slot_id):
    profile = get_object_or_404(DoctorProfile, user=request.user)
    slot = get_object_or_404(DoctorAvailability, id=slot_id, doctor=profile)
    slot.delete()
    messages.success(request, "Availability slot removed successfully.")
    return redirect('manage_availability')
