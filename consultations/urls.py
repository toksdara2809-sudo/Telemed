from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:appointment_id>/', views.consultation_room, name='consultation_room'),
    path('get-messages/<int:consultation_id>/', views.get_messages, name='get_messages'),
    path('send-message/<int:consultation_id>/', views.send_message, name='send_message'),
    path('complete/<int:consultation_id>/', views.complete_consultation, name='complete_consultation'),
]
