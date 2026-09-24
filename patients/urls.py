from django.urls import path
from . import views

urlpatterns = [
    path('profile/edit/', views.edit_patient_profile, name='edit_patient_profile'),
]
