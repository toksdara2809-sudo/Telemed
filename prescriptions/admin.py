from django.contrib import admin
from .models import Prescription, PrescriptionItem

class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'doctor', 'patient', 'date_written')
    list_filter = ('date_written',)
    search_fields = ('patient__user__first_name', 'doctor__user__last_name')
    inlines = [PrescriptionItemInline]

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medication_name', 'dosage', 'frequency', 'duration')
    search_fields = ('medication_name',)
