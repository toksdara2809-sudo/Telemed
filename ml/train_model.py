import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# Define symptoms list (features)
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

# Define diseases and their primary symptoms
DISEASE_PROFILES = {
    'Flu / Common Cold': ['fever', 'cough', 'fatigue', 'body_ache', 'sore_throat'],
    'Migraine': ['headache', 'nausea', 'dizziness', 'vision_blur'],
    'Gastroenteritis (Stomach Flu)': ['nausea', 'vomiting', 'diarrhea', 'stomach_pain'],
    'Hypertension': ['high_blood_pressure', 'dizziness', 'headache'],
    'Diabetes (Type 2)': ['frequent_urination', 'increased_thirst', 'fatigue', 'vision_blur'],
    'Malaria': ['fever', 'chills', 'sweating', 'headache', 'muscle_pain', 'fatigue', 'nausea'],
    'Typhoid Fever': ['fever', 'headache', 'stomach_pain', 'fatigue', 'body_ache'],
    'Cholera': ['watery_diarrhea', 'vomiting', 'nausea', 'muscle_pain'],
    'Tuberculosis': ['cough', 'night_sweats', 'weight_loss', 'chest_pain', 'fatigue', 'fever'],
    'Lassa Fever': ['fever', 'sore_throat', 'chest_pain', 'vomiting', 'headache', 'muscle_pain', 'bleeding'],
    'Sickle Cell Crisis': ['joint_pain', 'fatigue', 'jaundice', 'fever', 'body_ache'],
    
    # New Diseases to cover missing doctors' specializations
    'Clinical Depression': ['sadness', 'insomnia', 'loss_of_interest', 'fatigue', 'weight_loss'], # Psychiatry
    'Generalized Anxiety': ['anxiety', 'insomnia', 'fatigue', 'dizziness', 'sweating'], # Psychiatry
    'Endometriosis': ['pelvic_pain', 'painful_menstruation', 'fatigue', 'nausea'], # OB/GYN
    'Pelvic Inflammatory Disease': ['pelvic_pain', 'abnormal_vaginal_bleeding', 'fever', 'painful_menstruation'], # OB/GYN
    'Eczema': ['skin_rash', 'itching', 'skin_lesions'], # Dermatology
    'Fungal Skin Infection': ['itching', 'skin_rash'], # Dermatology
    'Osteoarthritis': ['joint_pain', 'joint_swelling', 'severe_bone_pain'], # Orthopedics
    'Bone Fracture': ['severe_bone_pain', 'joint_swelling', 'inability_to_bear_weight'], # Orthopedics
    'Glaucoma': ['eye_pain', 'vision_blur', 'halos_around_lights', 'headache'], # Ophthalmology
    'Cataract': ['cloudy_vision', 'vision_blur', 'halos_around_lights'], # Ophthalmology
    'Measles': ['fever', 'cough', 'childhood_rash', 'sore_throat'], # Pediatrics
    'Chickenpox': ['fever', 'fatigue', 'childhood_rash', 'blisters', 'itching'] # Pediatrics
}

def generate_synthetic_data(num_samples=2000):
    np.random.seed(42)
    data = []
    diseases = list(DISEASE_PROFILES.keys())
    
    for _ in range(num_samples):
        # Choose a random disease
        disease = np.random.choice(diseases)
        profile_symptoms = DISEASE_PROFILES[disease]
        
        # Build features: primary symptoms have a high probability of being 1, others have a low probability
        row = {}
        for s in SYMPTOMS:
            if s in profile_symptoms:
                # 85% chance of symptom being present
                row[s] = int(np.random.rand() < 0.85)
            else:
                # 10% chance of random background noise symptom
                row[s] = int(np.random.rand() < 0.10)
                
        row['disease'] = disease
        data.append(row)
        
    return pd.DataFrame(data)

def train_and_evaluate():
    print("Generating synthetic symptom dataset...")
    df = generate_synthetic_data(8000)
    
    X = df[SYMPTOMS]
    y = df['disease']
    
    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training Random Forest Classifier model...")
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:\n", report)
    print("\nConfusion Matrix:\n", cm)
    
    # Save the model
    service_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'devices', 'services')
    os.makedirs(service_dir, exist_ok=True)
    model_path = os.path.join(service_dir, 'symptom_model.joblib')
    joblib.dump(model, model_path)
    print(f"\nSaved model file to: {model_path}")
    
    # Save training report docs
    docs_path = os.path.join(os.path.dirname(__file__), 'model_evaluation_report.md')
    with open(docs_path, 'w') as f:
        f.write(f"# AI Symptom Classifier Model Evaluation Report\n\n")
        f.write(f"- **Algorithm**: Random Forest Classifier\n")
        f.write(f"- **Feature count**: {len(SYMPTOMS)} binary symptoms\n")
        f.write(f"- **Label count**: {len(DISEASE_PROFILES)} conditions\n")
        f.write(f"- **Dataset size**: 5000 samples (synthetic)\n")
        f.write(f"- **Test accuracy**: {accuracy:.2%}\n\n")
        f.write(f"## Classification Metrics\n```\n{report}\n```\n\n")
        f.write(f"## Confusion Matrix\n```\n{cm}\n```\n")
    print(f"Saved evaluation report to: {docs_path}")

if __name__ == "__main__":
    train_and_evaluate()
