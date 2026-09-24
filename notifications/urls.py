from django.urls import path
from . import views

urlpatterns = [
    path('mark/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('mark-all/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]
