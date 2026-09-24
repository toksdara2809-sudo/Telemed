from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date, timedelta, time
from patients.models import PatientProfile
from doctors.models import DoctorProfile, DoctorAvailability
from appointments.models import Appointment

User = get_user_model()


class AppointmentValidationTests(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(
            username='pat', password='test', role='patient',
            first_name='Pat', last_name='Test'
        )
        self.doctor_user = User.objects.create_user(
            username='doc', password='test', role='doctor',
            is_approved_doctor=True, first_name='Doc', last_name='Test'
        )
        self.patient = PatientProfile.objects.create(
            user=self.patient_user, contact_number='5550001',
            address='123 St', blood_group='O+',
            emergency_contact_name='E', emergency_contact_phone='5550002'
        )
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user, specialization='General',
            qualifications='MBBS', bio='GP'
        )
        # Available Monday 9am-12pm
        self.availability = DoctorAvailability.objects.create(
            doctor=self.doctor, day_of_week='Monday',
            start_time=time(9, 0), end_time=time(12, 0)
        )

    def _next_monday(self):
        today = date.today()
        days_ahead = 0 - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)

    def test_valid_appointment_creates(self):
        monday = self._next_monday()
        app = Appointment(
            patient=self.patient, doctor=self.doctor,
            date=monday, time_slot=time(9, 0), status='pending'
        )
        app.save()
        self.assertEqual(Appointment.objects.count(), 1)

    def test_past_date_raises_error(self):
        past = date.today() - timedelta(days=1)
        app = Appointment(
            patient=self.patient, doctor=self.doctor,
            date=past, time_slot=time(9, 0), status='pending'
        )
        with self.assertRaises(ValidationError):
            app.save()

    def test_outside_availability_raises_error(self):
        monday = self._next_monday()
        app = Appointment(
            patient=self.patient, doctor=self.doctor,
            date=monday, time_slot=time(14, 0), status='pending'
        )
        with self.assertRaises(ValidationError):
            app.save()

    def test_double_booking_raises_error(self):
        monday = self._next_monday()
        Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=monday, time_slot=time(9, 0), status='approved'
        )
        app2 = Appointment(
            patient=self.patient, doctor=self.doctor,
            date=monday, time_slot=time(9, 0), status='pending'
        )
        with self.assertRaises(ValidationError):
            app2.save()

    def test_status_transitions(self):
        monday = self._next_monday()
        app = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=monday, time_slot=time(9, 0), status='pending'
        )
        self.assertEqual(app.status, 'pending')
        app.status = 'approved'
        app.save()
        app.refresh_from_db()
        self.assertEqual(app.status, 'approved')
        app.status = 'completed'
        app.save()
        app.refresh_from_db()
        self.assertEqual(app.status, 'completed')
