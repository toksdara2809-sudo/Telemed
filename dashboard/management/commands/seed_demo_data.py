from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from patients.models import PatientProfile
from doctors.models import DoctorProfile, DoctorAvailability
from appointments.models import Appointment
from prescriptions.models import Prescription, PrescriptionItem
from medical_records.models import MedicalRecord
from devices.models import BloodPressureReading
from notifications.models import Notification
import datetime
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with demo data for development and project defense'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create admin user (superuser)
        admin_user, created = User.objects.get_or_create(
            username='admin', defaults={
                'email':'admin@pticlinic.com', 'first_name':'Admin', 'last_name':'User',
                'role':'admin', 'is_superuser': True, 'is_staff': True
            }
        )
        if not admin_user.check_password('admin123') or not admin_user.is_superuser:
            admin_user.set_password('admin123')
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()

        # Create various doctors with profiles and availability
        doctors_data = [
            {'username': 'dr_smith', 'first_name': 'John', 'last_name': 'Smith', 'specialization': 'Cardiology', 'qualifications': 'MD, FACC', 'bio': 'Experienced cardiologist with 15 years of practice.', 'fee': 150.00},
            {'username': 'dr_jones', 'first_name': 'Sarah', 'last_name': 'Jones', 'specialization': 'General Practice', 'qualifications': 'MBBS, MRCGP', 'bio': 'Family medicine specialist.', 'fee': 75.00},
            {'username': 'dr_patel', 'first_name': 'Raj', 'last_name': 'Patel', 'specialization': 'Neurology', 'qualifications': 'MD, PhD Neuroscience', 'bio': 'Neurologist specializing in headache disorders.', 'fee': 200.00},
            {'username': 'dr_okonkwo', 'first_name': 'Chidi', 'last_name': 'Okonkwo', 'specialization': 'Pediatrics & Child Health', 'qualifications': 'MBBS, FWACP (Paed)', 'bio': 'Child health specialist with expertise in malaria and malnutrition management.', 'fee': 100.00},
            {'username': 'dr_adebayo', 'first_name': 'Funmi', 'last_name': 'Adebayo', 'specialization': 'Obstetrics & Gynecology', 'qualifications': 'MBBS, FMCOG', 'bio': 'Maternal health expert focused on safe childbirth and antenatal care.', 'fee': 180.00},
            {'username': 'dr_ogunlesi', 'first_name': 'Tunde', 'last_name': 'Ogunlesi', 'specialization': 'Orthopedics & Trauma', 'qualifications': 'MBBS, FWACS (Ortho)', 'bio': 'Orthopedic surgeon experienced in road traffic accident trauma care.', 'fee': 220.00},
            {'username': 'dr_ekwueme', 'first_name': 'Ngozi', 'last_name': 'Ekwueme', 'specialization': 'Psychiatry & Mental Health', 'qualifications': 'MBBS, FWACP (Psych)', 'bio': 'Mental health advocate specializing in depression, anxiety, and PTSD.', 'fee': 130.00},
            {'username': 'dr_balogun', 'first_name': 'Kayode', 'last_name': 'Balogun', 'specialization': 'Ophthalmology', 'qualifications': 'MBBS, FMCOph', 'bio': 'Eye care specialist treating cataracts, glaucoma, and refractive errors.', 'fee': 160.00},
            {'username': 'dr_adiara', 'first_name': 'Mariam', 'last_name': 'Adiara', 'specialization': 'Dermatology', 'qualifications': 'MBBS, FWACP (Derm)', 'bio': 'Skin health expert managing eczema, fungal infections, and vitiligo.', 'fee': 140.00},
            {'username': 'dr_usman', 'first_name': 'Ibrahim', 'last_name': 'Usman', 'specialization': 'Internal Medicine', 'qualifications': 'MBBS, FWACP (Int Med)', 'bio': 'Internist managing hypertension, diabetes, and infectious diseases.', 'fee': 120.00},
            {'username': 'dr_obi', 'first_name': 'Adaora', 'last_name': 'Obi', 'specialization': 'Emergency Medicine', 'qualifications': 'MBBS, MSc Emergency Med', 'bio': 'Emergency physician trained in acute care and disaster response.', 'fee': 200.00},
            {'username': 'dr_bello', 'first_name': 'Sani', 'last_name': 'Bello', 'specialization': 'Public Health & Community Medicine', 'qualifications': 'MBBS, MPH', 'bio': 'Community health specialist focusing on disease surveillance and immunization.', 'fee': 80.00},
            {'username': 'dr_emenike', 'first_name': 'Chioma', 'last_name': 'Emenike', 'specialization': 'Radiology', 'qualifications': 'MBBS, FWACS (Rad)', 'bio': 'Radiologist specializing in ultrasound, X-ray, and MRI diagnostics.', 'fee': 190.00},
        ]

        created_doctors = []
        for doc_data in doctors_data:
            user, created = User.objects.get_or_create(
                username=doc_data['username'],
                defaults={
                    'password': 'doctor123', 'first_name': doc_data['first_name'],
                    'last_name': doc_data['last_name'],
                    'email': f"{doc_data['username']}@pticlinic.com", 'role': 'doctor',
                    'is_approved_doctor': True
                }
            )
            if created:
                user.set_password('doctor123')
                user.save()
            profile, _ = DoctorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'specialization': doc_data['specialization'],
                    'qualifications': doc_data['qualifications'],
                    'bio': doc_data['bio'],
                    'consultation_fee': doc_data['fee']
                }
            )
            # Add availability: Mon-Fri 9am-5pm (skip if already exists)
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                DoctorAvailability.objects.get_or_create(
                    doctor=profile, day_of_week=day,
                    defaults={'start_time': datetime.time(9, 0), 'end_time': datetime.time(17, 0)}
                )
            created_doctors.append(profile)
        
        # Create 5 patients with profiles
        patients_data = [
            {'username': 'patient1', 'first_name': 'Alice', 'last_name': 'Brown', 'dob': '1990-05-15', 'gender': 'female', 'blood': 'A+', 'allergies': 'Penicillin'},
            {'username': 'patient2', 'first_name': 'Bob', 'last_name': 'Williams', 'dob': '1985-08-22', 'gender': 'male', 'blood': 'O-', 'allergies': ''},
            {'username': 'patient3', 'first_name': 'Carol', 'last_name': 'Davis', 'dob': '1978-03-10', 'gender': 'female', 'blood': 'B+', 'allergies': 'Aspirin'},
            {'username': 'patient4', 'first_name': 'David', 'last_name': 'Miller', 'dob': '1995-11-28', 'gender': 'male', 'blood': 'AB+', 'allergies': ''},
            {'username': 'patient5', 'first_name': 'Eva', 'last_name': 'Wilson', 'dob': '2000-01-07', 'gender': 'female', 'blood': 'O+', 'allergies': 'Latex'},
        ]
        
        created_patients = []
        for p_data in patients_data:
            user, created = User.objects.get_or_create(
                username=p_data['username'],
                defaults={
                    'first_name': p_data['first_name'], 'last_name': p_data['last_name'],
                    'email': f"{p_data['username']}@example.com", 'role': 'patient'
                }
            )
            if created:
                user.set_password('patient123')
                user.save()
            profile, _ = PatientProfile.objects.get_or_create(
                user=user,
                defaults={
                    'date_of_birth': p_data['dob'], 'gender': p_data['gender'],
                    'contact_number': f"555{random.randint(1000000, 9999999)}",
                    'address': f"{random.randint(100, 999)} Demo Street, Demo City",
                    'blood_group': p_data['blood'], 'allergies': p_data['allergies'],
                    'emergency_contact_name': f"Emergency Contact for {p_data['first_name']}",
                    'emergency_contact_phone': f"555{random.randint(1000000, 9999999)}"
                }
            )
            created_patients.append(profile)
        
        # Create appointments (idempotent: skip if exact record exists)
        today = datetime.date.today()
        statuses = ['pending', 'approved', 'completed', 'cancelled', 'rejected']
        time_slots = [datetime.time(9, 0), datetime.time(10, 0), datetime.time(11, 0), datetime.time(14, 0), datetime.time(15, 0)]
        
        for i in range(15):
            patient = random.choice(created_patients)
            doctor = random.choice(created_doctors)
            days_ahead = random.randint(-30, 14)
            app_date = today + datetime.timedelta(days=days_ahead)
            if app_date.weekday() >= 5:
                app_date += datetime.timedelta(days=(7 - app_date.weekday()))
            
            time_slot = random.choice(time_slots)
            status = random.choice(statuses)
            
            if not Appointment.objects.filter(
                patient=patient, doctor=doctor, date=app_date, time_slot=time_slot
            ).exists():
                try:
                    Appointment.objects.create(
                        patient=patient, doctor=doctor, date=app_date,
                        time_slot=time_slot, status=status,
                        reason=f"Demo appointment reason {i+1}"
                    )
                except Exception:
                    pass
        
        # Create some medical records
        for patient in created_patients[:3]:
            doctor = random.choice(created_doctors)
            MedicalRecord.objects.create(
                patient=patient, doctor=doctor,
                diagnosis="Seasonal flu with mild symptoms",
                treatment_plan="Rest, fluids, and paracetamol as needed",
                notes="Patient responded well to treatment."
            )
        
        # Create some prescriptions
        for patient in created_patients[:2]:
            doctor = random.choice(created_doctors)
            prescription = Prescription.objects.create(
                doctor=doctor, patient=patient,
                additional_notes="Take with food. Avoid alcohol."
            )
            PrescriptionItem.objects.create(
                prescription=prescription, medication_name='Paracetamol',
                dosage='500mg', frequency='Three times daily', duration='5 days'
            )
            PrescriptionItem.objects.create(
                prescription=prescription, medication_name='Ibuprofen',
                dosage='200mg', frequency='Twice daily after meals', duration='3 days'
            )
        
        # Create some BP readings
        for patient in created_patients[:2]:
            for _ in range(5):
                BloodPressureReading.objects.create(
                    patient=patient,
                    systolic=random.randint(110, 160),
                    diastolic=random.randint(70, 100),
                    pulse=random.randint(60, 100),
                    device_id='Simulator-BLE'
                )
        
        self.stdout.write(self.style.SUCCESS(
            'Successfully seeded database!\n'
            '  Admin: admin / admin123\n'
            '  Doctors: dr_smith, dr_jones, dr_patel, dr_okonkwo, dr_adebayo,\n'
            '           dr_ogunlesi, dr_ekwueme, dr_balogun, dr_adiara,\n'
            '           dr_usman, dr_obi, dr_bello, dr_emenike  / doctor123\n'
            '  Patients: patient1-5 / patient123'
        ))
