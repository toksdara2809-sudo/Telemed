import os
import joblib
import numpy as np

# Pinned list of symptoms matching training features
SYMPTOMS = [
    'fever', 'cough', 'fatigue', 'body_ache', 'headache',
    'nausea', 'vomiting', 'diarrhea', 'high_blood_pressure', 'dizziness',
    'frequent_urination', 'increased_thirst', 'vision_blur', 'stomach_pain', 'sore_throat',
    'chills', 'sweating', 'joint_pain', 'chest_pain', 'weight_loss',
    'night_sweats', 'watery_diarrhea', 'muscle_pain', 'jaundice', 'bleeding',
    'sadness', 'anxiety', 'insomnia', 'loss_of_interest',  # Psychiatry
    'pelvic_pain', 'abnormal_vaginal_bleeding', 'painful_menstruation',  # OB/GYN
    'skin_rash', 'itching', 'skin_lesions',  # Dermatology
    'severe_bone_pain', 'joint_swelling', 'inability_to_bear_weight',  # Orthopedics
    'eye_pain', 'cloudy_vision', 'halos_around_lights',  # Ophthalmology
    'childhood_rash', 'blisters'  # Pediatrics
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'symptom_model.joblib')

def predict_condition(selected_symptoms):
    """
    selected_symptoms: list of symptom names that are checked (e.g. ['fever', 'cough'])
    returns: sorted list of tuples (condition, confidence_percentage)
    """
    if not os.path.exists(MODEL_PATH):
        # Fallback if model file is not found
        return [("Model not trained", 0.0)]
        
    try:
        model = joblib.load(MODEL_PATH)
    except Exception:
        return [("Failed to load model", 0.0)]

    # Build binary feature vector
    vector = [1 if s in selected_symptoms else 0 for s in SYMPTOMS]
    X_input = np.array([vector])

    # Predict probabilities
    classes = model.classes_
    probabilities = model.predict_proba(X_input)[0]

    # Zip classes and probabilities
    results = []
    for c, prob in zip(classes, probabilities):
        confidence = float(prob * 100)
        if confidence > 0.0:  # Only return conditions with > 0% confidence
            results.append((c, round(confidence, 2)))

    # Sort by confidence descending
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# Nigeria-relevant drug recommendations per condition
DRUG_RECOMMENDATIONS = {
    'Flu / Common Cold': [
        {'name': 'Paracetamol (Acetaminophen)', 'dosage': '500mg', 'frequency': '3 times daily after meals', 'duration': '3-5 days'},
        {'name': 'Vitamin C Tablets', 'dosage': '200mg', 'frequency': 'Once daily', 'duration': '5-7 days'},
        {'name': 'Chlorpheniramine (Antihistamine)', 'dosage': '4mg', 'frequency': 'Twice daily', 'duration': '3-5 days'},
        {'name': 'Dextromethorphan Cough Syrup', 'dosage': '10ml', 'frequency': '3 times daily', 'duration': '5 days'},
    ],
    'Migraine': [
        {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': 'As needed, max 3 times daily', 'duration': '3 days'},
        {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'As needed', 'duration': '3 days'},
        {'name': 'Sumatriptan', 'dosage': '50mg', 'frequency': 'At onset of migraine', 'duration': 'As needed'},
        {'name': 'Caffeine Citrate', 'dosage': '65mg', 'frequency': 'With pain reliever', 'duration': '2-3 days'},
    ],
    'Gastroenteritis (Stomach Flu)': [
        {'name': 'Oral Rehydration Salts (ORS)', 'dosage': '1 sachet per litre of water', 'frequency': 'After each loose stool', 'duration': 'Until diarrhea stops'},
        {'name': 'Zinc Tablets', 'dosage': '20mg', 'frequency': 'Once daily', 'duration': '10-14 days'},
        {'name': 'Metronidazole', 'dosage': '400mg', 'frequency': '3 times daily after meals', 'duration': '5-7 days'},
        {'name': 'Probiotic Capsules', 'dosage': '1 capsule', 'frequency': 'Twice daily', 'duration': '7 days'},
    ],
    'Hypertension': [
        {'name': 'Amlodipine', 'dosage': '5mg', 'frequency': 'Once daily', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Hydrochlorothiazide', 'dosage': '12.5mg', 'frequency': 'Once daily in the morning', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Aspirin (Low Dose)', 'dosage': '75mg', 'frequency': 'Once daily', 'duration': 'As directed by doctor'},
    ],
    'Diabetes (Type 2)': [
        {'name': 'Metformin', 'dosage': '500mg', 'frequency': 'Twice daily after meals', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Glibenclamide', 'dosage': '5mg', 'frequency': 'Once daily before breakfast', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Insulin Glargine (Lantus)', 'dosage': '10-20 units', 'frequency': 'Once daily at bedtime', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Multivitamin Tablets', 'dosage': '1 tablet', 'frequency': 'Once daily', 'duration': 'Ongoing'},
    ],
    'Malaria': [
        {'name': 'Artemether-Lumefantrine (ACT)', 'dosage': '80mg/480mg', 'frequency': 'Twice daily for 3 days', 'duration': '3 days'},
        {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': '3 times daily (for fever)', 'duration': '3-5 days'},
        {'name': 'Vitamin B Complex', 'dosage': '1 tablet', 'frequency': 'Once daily', 'duration': '7 days'},
        {'name': 'Ferrous Sulphate (Iron)', 'dosage': '200mg', 'frequency': 'Once daily', 'duration': '14 days'},
    ],
    'Typhoid Fever': [
        {'name': 'Ciprofloxacin', 'dosage': '500mg', 'frequency': 'Twice daily', 'duration': '10-14 days'},
        {'name': 'Azithromycin', 'dosage': '500mg', 'frequency': 'Once daily', 'duration': '7 days'},
        {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': '3 times daily (for fever)', 'duration': '3-5 days'},
        {'name': 'Probiotic Capsules', 'dosage': '1 capsule', 'frequency': 'Twice daily', 'duration': '10 days'},
    ],
    'Cholera': [
        {'name': 'Oral Rehydration Salts (ORS)', 'dosage': '1 sachet per litre of water', 'frequency': 'Continuously after each stool', 'duration': 'Until rehydrated'},
        {'name': 'Doxycycline', 'dosage': '100mg', 'frequency': 'Twice daily', 'duration': '3-5 days'},
        {'name': 'Azithromycin', 'dosage': '500mg', 'frequency': 'Once daily', 'duration': '3 days'},
        {'name': 'Zinc Tablets', 'dosage': '20mg', 'frequency': 'Once daily', 'duration': '10-14 days'},
    ],
    'Tuberculosis': [
        {'name': 'Rifampicin', 'dosage': '600mg', 'frequency': 'Once daily on empty stomach', 'duration': '6 months (DOTS)'},
        {'name': 'Isoniazid', 'dosage': '300mg', 'frequency': 'Once daily', 'duration': '6 months (DOTS)'},
        {'name': 'Pyrazinamide', 'dosage': '1500mg', 'frequency': 'Once daily', 'duration': 'First 2 months'},
        {'name': 'Ethambutol', 'dosage': '800mg', 'frequency': 'Once daily', 'duration': 'First 2 months'},
        {'name': 'Vitamin B6 (Pyridoxine)', 'dosage': '25mg', 'frequency': 'Once daily', 'duration': 'Throughout TB treatment'},
    ],
    'Lassa Fever': [
        {'name': 'Ribavirin', 'dosage': 'Loading 30mg/kg then 15mg/kg', 'frequency': 'Every 6 hours for 4 days, then every 8 hours for 6 days', 'duration': '10 days (hospital setting)'},
        {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'As needed for fever/pain', 'duration': 'As needed'},
        {'name': 'IV Fluids (Normal Saline)', 'dosage': '1 litre', 'frequency': 'As needed for hydration', 'duration': 'Per clinical need'},
    ],
    'Sickle Cell Crisis': [
        {'name': 'Hydroxyurea', 'dosage': '500mg', 'frequency': 'Once daily', 'duration': 'Long-term (as prescribed)'},
        {'name': 'Folic Acid', 'dosage': '5mg', 'frequency': 'Once daily', 'duration': 'Ongoing'},
        {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': '3 times daily (for pain)', 'duration': 'During crisis'},
        {'name': 'Morphine (or Pethidine)', 'dosage': 'As per hospital protocol', 'frequency': 'As needed for severe pain', 'duration': 'During crisis (hospital)'},
        {'name': 'Penicillin V Prophylaxis', 'dosage': '125mg (children) / 250mg (adults)', 'frequency': 'Twice daily', 'duration': 'Long-term'},
    ],
    'Clinical Depression': [
        {'name': 'Fluoxetine', 'dosage': '20mg', 'frequency': 'Once daily', 'duration': 'Long-term'},
        {'name': 'Cognitive Behavioral Therapy (CBT)', 'dosage': 'N/A', 'frequency': 'Weekly', 'duration': 'As advised by psychiatrist'},
    ],
    'Generalized Anxiety': [
        {'name': 'Sertraline', 'dosage': '50mg', 'frequency': 'Once daily', 'duration': 'Long-term'},
        {'name': 'Propranolol', 'dosage': '10mg', 'frequency': 'As needed for physical symptoms', 'duration': 'As needed'},
    ],
    'Endometriosis': [
        {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': 'Every 6-8 hours for pain', 'duration': 'During menstruation'},
        {'name': 'Hormonal Contraceptives', 'dosage': '1 pill', 'frequency': 'Once daily', 'duration': 'Long-term'},
    ],
    'Pelvic Inflammatory Disease': [
        {'name': 'Ceftriaxone', 'dosage': '500mg IM', 'frequency': 'Single dose', 'duration': '1 day'},
        {'name': 'Doxycycline', 'dosage': '100mg', 'frequency': 'Twice daily', 'duration': '14 days'},
        {'name': 'Metronidazole', 'dosage': '400mg', 'frequency': 'Twice daily', 'duration': '14 days'},
    ],
    'Eczema': [
        {'name': 'Hydrocortisone Cream (1%)', 'dosage': 'Thin layer', 'frequency': 'Twice daily', 'duration': 'Up to 2 weeks'},
        {'name': 'Emollient Moisturizer', 'dosage': 'Apply generously', 'frequency': '3-4 times daily', 'duration': 'Ongoing'},
    ],
    'Fungal Skin Infection': [
        {'name': 'Clotrimazole Cream', 'dosage': 'Thin layer', 'frequency': 'Twice daily', 'duration': '2-4 weeks'},
        {'name': 'Fluconazole', 'dosage': '150mg', 'frequency': 'Single dose', 'duration': '1 day'},
    ],
    'Osteoarthritis': [
        {'name': 'Paracetamol', 'dosage': '500mg', 'frequency': 'As needed for pain', 'duration': 'Ongoing'},
        {'name': 'Diclofenac Gel', 'dosage': 'Apply to joint', 'frequency': '3 times daily', 'duration': 'As needed'},
    ],
    'Bone Fracture': [
        {'name': 'Immobilization (Cast/Splint)', 'dosage': 'N/A', 'frequency': 'Continuous', 'duration': '4-8 weeks'},
        {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': '3 times daily', 'duration': 'As needed for pain'},
    ],
    'Glaucoma': [
        {'name': 'Timolol Eye Drops', 'dosage': '1 drop per eye', 'frequency': 'Twice daily', 'duration': 'Long-term'},
        {'name': 'Latanoprost Eye Drops', 'dosage': '1 drop per eye', 'frequency': 'Once daily at night', 'duration': 'Long-term'},
    ],
    'Cataract': [
        {'name': 'Surgical Consultation', 'dosage': 'N/A', 'frequency': 'N/A', 'duration': 'Refer to Ophthalmologist'},
    ],
    'Measles': [
        {'name': 'Vitamin A', 'dosage': '200,000 IU', 'frequency': 'Once daily', 'duration': '2 days'},
        {'name': 'Paracetamol', 'dosage': 'As per weight', 'frequency': 'Every 6 hours for fever', 'duration': 'As needed'},
    ],
    'Chickenpox': [
        {'name': 'Calamine Lotion', 'dosage': 'Apply to spots', 'frequency': '3 times daily', 'duration': 'Until blisters dry'},
        {'name': 'Paracetamol', 'dosage': 'As per weight', 'frequency': 'For fever', 'duration': 'As needed'},
        {'name': 'Acyclovir (Severe cases)', 'dosage': '20mg/kg', 'frequency': '4 times daily', 'duration': '5 days'},
    ],
}

def get_drug_recommendations(condition):
    """Return drug list for a predicted condition, or empty list if unknown."""
    return DRUG_RECOMMENDATIONS.get(condition, [])
