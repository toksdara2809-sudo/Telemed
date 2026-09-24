from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from prescriptions.models import Prescription
from .models import Notification

@receiver(post_save, sender=Appointment)
def appointment_notification(sender, instance, created, **kwargs):
    if created:
        # Notify doctor of pending appointment
        Notification.objects.create(
            recipient=instance.doctor.user,
            title="New Appointment Booking Request",
            message=f"Patient {instance.patient.user.get_full_name()} has requested an appointment on {instance.date} at {instance.time_slot.strftime('%I:%M %p')}."
        )
    else:
        # Notify patient when status changes
        if instance.status == 'approved':
            Notification.objects.create(
                recipient=instance.patient.user,
                title="Appointment Approved",
                message=f"Your appointment with Dr. {instance.doctor.user.last_name} on {instance.date} at {instance.time_slot.strftime('%I:%M %p')} has been approved."
            )
        elif instance.status == 'rejected':
            Notification.objects.create(
                recipient=instance.patient.user,
                title="Appointment Rejected",
                message=f"Your appointment with Dr. {instance.doctor.user.last_name} on {instance.date} has been rejected."
            )
        elif instance.status == 'cancelled':
            Notification.objects.create(
                recipient=instance.doctor.user,
                title="Appointment Cancelled",
                message=f"Patient {instance.patient.user.get_full_name()} has cancelled their appointment on {instance.date}."
            )

@receiver(post_save, sender=Prescription)
def prescription_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.patient.user,
            title="New Prescription Ready",
            message=f"Dr. {instance.doctor.user.last_name} has uploaded a new prescription for you."
        )
