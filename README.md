# TeleMed Portal — Telemedicine Web Application

A full-featured telemedicine web application built for an academic final-year project. Enables patients to book appointments, conduct chat-based consultations with doctors, manage electronic medical records (EMR), receive prescriptions with PDF export, record blood pressure readings via BLE device simulator, and get AI-powered symptom-based disease predictions.

---

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5.3, Chart.js, Font Awesome 6.4
- **Backend:** Python 3.13, Django 5.x
- **Database:** MySQL (XAMPP) or SQLite3 (development)
- **PDF Generation:** xhtml2pdf
- **Machine Learning:** scikit-learn (Random Forest Classifier)
- **Environment Config:** django-environ (.env file)

---

## Project Structure

```
telemed_project/
├── telemed_project/          # Project configuration (settings, urls)
├── authentication/           # Custom user model, registration, login, RBAC
├── patients/                 # Patient profile management
├── doctors/                  # Doctor profile, availability scheduling
├── appointments/             # Appointment booking, approval, validation
├── consultations/            # Chat-based consultation rooms
├── medical_records/          # EMR (diagnosis, treatment records, lab results)
├── prescriptions/            # Prescriptions with inline medication items, PDF export
├── notifications/            # In-app notification system (signal-driven)
├── reports/                  # Admin analytics dashboard, CSV export
├── dashboard/                # Role-based dashboards + global search
├── devices/                  # BP monitoring, BLE simulator, AI symptom checker
│   └── services/
│       ├── diagnosis.py      # ML inference service
│       └── symptom_model.joblib  # Trained Random Forest model
├── ml/
│   ├── train_model.py        # ML training pipeline (synthetic data)
│   └── model_evaluation_report.md  # 97.4% accuracy report
├── templates/                # Global Django templates
├── static/                   # Static files (empty, uses CDN)
├── media/                    # User uploads (lab results, profile pics)
├── manage.py
├── requirements.txt
├── .env / .env.example
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- MySQL (via XAMPP or standalone) — OR use SQLite for quick start
- VS Code (recommended)

### 1. Clone and Virtual Environment

```bash
cd telemed_project
python -m venv venv
# Activate:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: SQLite (Quick Start — No MySQL needed)
The `.env` file is pre-configured for SQLite. Just run:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Option B: MySQL (Production-like)
1. Start MySQL via XAMPP or your local MySQL server
2. Create a database named `telemed_db`
3. Copy `.env.example` to `.env` and uncomment/update the `DATABASE_URL`:
   ```
   DATABASE_URL=mysql://root:@127.0.0.1:3306/telemed_db
   ```
4. Run:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Seed Demo Data (Recommended)

```bash
python manage.py seed_demo_data
```

This creates:
- **Admin:** `admin` / `admin123`
- **Doctors (13):** `dr_smith`, `dr_jones`, `dr_patel`, `dr_okonkwo`, `dr_adebayo`, `dr_ogunlesi`, `dr_ekwueme`, `dr_balogun`, `dr_adiara`, `dr_usman`, `dr_obi`, `dr_bello`, `dr_emenike` / `doctor123`
- **Patients:** `patient1` through `patient5` / `patient123`
- Sample appointments, medical records, prescriptions, and BP readings

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## Default Accounts (after seeding)

| Role     | Username        | Password    |
|----------|-----------------|-------------|
| Admin    | admin           | admin123    |
| Doctor   | dr_smith        | doctor123   |
| Doctor   | dr_jones        | doctor123   |
| Doctor   | dr_patel        | doctor123   |
| Doctor   | dr_okonkwo      | doctor123   |
| Doctor   | dr_adebayo      | doctor123   |
| Doctor   | dr_ogunlesi     | doctor123   |
| Doctor   | dr_ekwueme      | doctor123   |
| Doctor   | dr_balogun      | doctor123   |
| Doctor   | dr_adiara       | doctor123   |
| Doctor   | dr_usman        | doctor123   |
| Doctor   | dr_obi          | doctor123   |
| Doctor   | dr_bello        | doctor123   |
| Doctor   | dr_emenike      | doctor123   |
| Patient  | patient1        | patient123  |
| Patient  | patient2        | patient123  |
| Patient  | patient3        | patient123  |
| Patient  | patient4        | patient123  |
| Patient  | patient5        | patient123  |

---

## Module Overview

| Module | Purpose |
|--------|---------|
| **Authentication** | Custom user model with role (patient/doctor/admin), registration, login, password reset, RBAC decorators/mixins |
| **Patients** | Profile management (DOB, gender, blood group, allergies, emergency contact) |
| **Doctors** | Profile + weekly availability scheduling with unique time slots |
| **Appointments** | Booking with validation (doctor availability, double-booking prevention), status workflow (pending → approved → completed) |
| **Consultations** | AJAX-polling chat rooms tied to approved appointments, completion saves to EMR |
| **Medical Records** | EMR entries (diagnosis, treatment plan) and lab result file uploads |
| **Prescriptions** | Inline formset for medications, PDF download via xhtml2pdf |
| **Notifications** | Signal-driven (appointment events, prescription creation), context processor for navbar bell |
| **Dashboard** | Role-specific dashboards with global search across patients/doctors/appointments |
| **Devices** | Blood pressure readings, abnormal alerts, BLE simulator, AI symptom checker |
| **Reports** | Admin analytics with Chart.js visualization (monthly trends, top doctors, status distribution), CSV export |
| **AI Diagnosis** | Random Forest classifier (94.3% accuracy) trained on 25 symptoms × 11 Nigeria-relevant conditions (Malaria, Typhoid, Cholera, TB, Lassa Fever, Sickle Cell, etc.) with drug recommendations |

---

## Running Tests

```bash
python manage.py test
```

Tests cover:
- Authentication & RBAC (role-based access, login/logout, registration)
- Appointment validation (past dates, availability, double-booking)
- AI diagnosis service (predictions, confidence scoring, symptom input)

---

## Architecture Decisions

- **Custom User Model** with role field from the start (not retrofitted)
- **Profile Pattern** via OneToOneField (keeps auth model clean)
- **Signal-Driven Notifications** decoupled from business views
- **Context Processor** for unread notification count in navbar
- **ML as Service** — `devices/services/diagnosis.py` loads a pre-trained model, never trains in request cycle
- **Single Ingestion Endpoint** — `POST /devices/readings/record/` used by both real BLE and simulator

---

## Build Order

1. Project scaffolding + custom user model + auth
2. Patient and doctor profile modules + role-based dashboards
3. Appointment booking/approval flow
4. EMR + prescriptions
5. Chat-based consultation module
6. Notifications
7. Search + reports + admin dashboard
8. Devices module: BP/IoT ingestion + AI diagnosis classifier
9. Seed data command, README, and final polish

---

## Future Enhancements

- **Video Consultations:** Extension point exists in the consultation room (see the disabled "Start Video Call" button placeholder). Integrate WebRTC via libraries like PeerJS or LiveKit.
- **Real Web Bluetooth:** The BLE simulator shares the same backend endpoint (`record_reading`). Replace the simulator page with `navigator.bluetooth.requestDevice()` targeting the Blood Pressure Profile (`0x1810`).
- **Email Notifications:** Django's email backend is configured (console in dev). Swap to SMTP for real email alerts.
- **Django Admin Customization:** Basic admin registrations are in place; customize list displays, filters, and actions further as needed.
- **API Layer:** Add Django REST Framework for mobile app integration.

---

## Disclaimer

The AI Symptom Checker is for **informational/decision-support purposes only** and does not replace professional medical judgment. Always consult a qualified healthcare provider for medical advice.
