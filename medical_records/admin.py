from django.contrib import admin
from .models import MedicalRecord, LabResult

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'diagnosis', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'diagnosis')

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_name', 'test_date', 'uploading_doctor')
    list_filter = ('test_date',)
    search_fields = ('patient__user__first_name', 'test_name')
