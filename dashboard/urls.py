from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    path('', views.landing_page, name='landing_page'),
    path('patient/', views.dashboard_patient, name='dashboard_patient'),
    path('doctor/', views.dashboard_doctor, name='dashboard_doctor'),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),
    path('admin/approve/<int:doctor_user_id>/', views.approve_doctor, name='approve_doctor'),
    path('search/', views.global_search, name='global_search'),
]
