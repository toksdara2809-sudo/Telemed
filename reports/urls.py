from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('data/', views.reports_json_data, name='reports_json_data'),
    path('export/csv/', views.export_appointments_csv, name='export_appointments_csv'),
]
