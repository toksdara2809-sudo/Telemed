from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from patients.models import PatientProfile
from doctors.models import DoctorProfile

User = get_user_model()


class AuthAndRBACTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient_user = User.objects.create_user(
            username='patient1', password='testpass123', role='patient',
            first_name='Alice', last_name='Patient'
        )
        self.doctor_user = User.objects.create_user(
            username='doctor1', password='testpass123', role='doctor',
            is_approved_doctor=True, first_name='Bob', last_name='Doctor'
        )
        self.unapproved_doc = User.objects.create_user(
            username='pendingdoc', password='testpass123', role='doctor',
            is_approved_doctor=False
        )
        self.admin_user = User.objects.create_superuser(
            username='admin1', password='testpass123', role='admin'
        )
        PatientProfile.objects.create(
            user=self.patient_user, contact_number='5550001',
            address='123 St', blood_group='O+',
            emergency_contact_name='Emer', emergency_contact_phone='5550002'
        )
        DoctorProfile.objects.create(
            user=self.doctor_user, specialization='Cardiology',
            qualifications='MD', bio='Heart doctor'
        )

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard_home')}")

    def test_patient_login_redirects_to_patient_dashboard(self):
        self.client.login(username='patient1', password='testpass123')
        response = self.client.get(reverse('dashboard_home'))
        self.assertRedirects(response, reverse('dashboard_patient'))

    def test_doctor_login_redirects_to_doctor_dashboard(self):
        self.client.login(username='doctor1', password='testpass123')
        response = self.client.get(reverse('dashboard_home'))
        self.assertRedirects(response, reverse('dashboard_doctor'))

    def test_admin_login_redirects_to_admin_dashboard(self):
        self.client.login(username='admin1', password='testpass123')
        response = self.client.get(reverse('dashboard_home'))
        self.assertRedirects(response, reverse('dashboard_admin'))

    def test_patient_cannot_access_doctor_view(self):
        self.client.login(username='patient1', password='testpass123')
        response = self.client.get(reverse('dashboard_doctor'))
        self.assertNotEqual(response.status_code, 200)

    def test_doctor_cannot_access_patient_view(self):
        self.client.login(username='doctor1', password='testpass123')
        response = self.client.get(reverse('dashboard_patient'))
        self.assertNotEqual(response.status_code, 200)

    def test_unapproved_doctor_blocked(self):
        self.client.login(username='pendingdoc', password='testpass123')
        response = self.client.get(reverse('dashboard_doctor'))
        self.assertNotEqual(response.status_code, 200)

    def test_patient_registration_creates_profile(self):
        response = self.client.post(reverse('register_patient'), {
            'username': 'newpatient',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'first_name': 'New',
            'last_name': 'Patient',
            'email': 'new@example.com',
            'date_of_birth': '1990-01-01',
            'gender': 'female',
            'contact_number': '5551234',
            'blood_group': 'A+',
            'allergies': 'None',
            'emergency_contact_name': 'Test',
            'emergency_contact_phone': '5555678',
            'address': '456 Demo St',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newpatient').exists())
        self.assertTrue(PatientProfile.objects.filter(user__username='newpatient').exists())

    def test_logout(self):
        self.client.login(username='patient1', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'patient1', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')
