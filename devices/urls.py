from django.urls import path
from . import views

urlpatterns = [
    path('readings/', views.view_readings, name='view_readings'),
    path('readings/record/', views.record_reading, name='record_reading'),
    path('simulator/', views.ble_simulator, name='ble_simulator'),
    path('ai-diagnosis/', views.ai_diagnosis_flow, name='ai_diagnosis'),
]
