from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.view_my_records, name='view_my_records'),
    path('add/', views.add_medical_record, name='add_medical_record'),
    path('upload/', views.upload_lab_result, name='upload_lab_result'),
]
