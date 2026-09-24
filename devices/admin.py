from django.contrib import admin
from .models import BloodPressureReading, AIDiagnosisHistory

@admin.register(BloodPressureReading)
class BloodPressureReadingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'systolic', 'diastolic', 'pulse', 'device_id', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name')

@admin.register(AIDiagnosisHistory)
class AIDiagnosisHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'predicted_condition', 'confidence', 'timestamp')
    list_filter = ('predicted_condition',)
    search_fields = ('patient__user__first_name', 'predicted_condition')
