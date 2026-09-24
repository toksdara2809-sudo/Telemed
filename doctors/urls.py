from django.urls import path
from . import views

urlpatterns = [
    path('profile/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('availability/', views.manage_availability, name='manage_availability'),
    path('availability/delete/<int:slot_id>/', views.delete_availability, name='delete_availability'),
]
