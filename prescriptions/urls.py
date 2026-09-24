from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_prescription, name='create_prescription'),
    path('list/', views.prescription_list, name='prescription_list'),
    path('download/<int:prescription_id>/', views.download_prescription_pdf, name='download_prescription_pdf'),
]
