# AI Symptom Classifier Model Evaluation Report

- **Algorithm**: Random Forest Classifier
- **Feature count**: 43 binary symptoms
- **Label count**: 23 conditions
- **Dataset size**: 5000 samples (synthetic)
- **Test accuracy**: 87.00%

## Classification Metrics
```
                               precision    recall  f1-score   support

                Bone Fracture       0.78      0.79      0.79        68
                     Cataract       0.82      0.84      0.83        75
                   Chickenpox       0.77      0.87      0.82        69
                      Cholera       0.89      0.83      0.86        65
          Clinical Depression       0.88      0.87      0.87        67
            Diabetes (Type 2)       0.88      0.90      0.89        67
                       Eczema       0.95      0.83      0.89        72
                Endometriosis       0.77      0.83      0.80        65
            Flu / Common Cold       0.91      0.77      0.84        66
        Fungal Skin Infection       0.75      0.73      0.74        71
Gastroenteritis (Stomach Flu)       0.93      0.94      0.94        70
          Generalized Anxiety       0.89      0.92      0.90        72
                     Glaucoma       0.86      0.88      0.87        67
                 Hypertension       0.88      0.92      0.90        79
                  Lassa Fever       0.96      0.97      0.96        69
                      Malaria       0.90      0.94      0.92        70
                      Measles       0.93      0.91      0.92        69
                     Migraine       0.90      0.90      0.90        69
               Osteoarthritis       0.89      0.77      0.83        66
  Pelvic Inflammatory Disease       0.83      0.96      0.89        72
           Sickle Cell Crisis       0.84      0.83      0.84        71
                 Tuberculosis       0.96      0.92      0.94        71
                Typhoid Fever       0.88      0.86      0.87        70

                     accuracy                           0.87      1600
                    macro avg       0.87      0.87      0.87      1600
                 weighted avg       0.87      0.87      0.87      1600

```

## Confusion Matrix
```
[[54  1  0  1  1  1  0  0  0  2  0  1  1  1  0  0  0  0  3  2  0  0  0]
 [ 0 63  1  0  1  0  0  1  0  1  0  0  5  0  0  1  0  0  0  1  1  0  0]
 [ 0  0 60  1  0  0  0  1  0  1  0  0  0  0  0  1  1  0  1  1  1  1  0]
 [ 3  2  0 54  0  0  0  1  0  0  3  0  0  0  2  0  0  0  0  0  0  0  0]
 [ 1  0  1  0 58  0  1  1  0  2  0  2  0  0  0  0  0  0  0  0  0  0  1]
 [ 1  1  0  0  2 60  0  1  0  0  1  0  0  0  0  0  0  0  0  0  1  0  0]
 [ 0  0  1  0  0  0 60  1  0  9  0  0  0  1  0  0  0  0  0  0  0  0  0]
 [ 0  1  2  0  0  1  0 54  0  0  1  1  0  0  0  0  0  0  0  3  1  1  0]
 [ 0  0  1  0  2  1  0  0 51  0  0  0  0  0  1  1  1  0  0  0  3  0  5]
 [ 1  3  3  1  0  1  2  1  0 52  0  0  1  1  0  0  1  0  1  3  0  0  0]
 [ 0  0  0  2  0  0  0  1  0  0 66  0  0  0  0  0  0  1  0  0  0  0  0]
 [ 0  0  1  0  1  0  0  0  0  0  0 66  0  0  0  0  0  2  0  0  1  1  0]
 [ 0  3  0  0  0  0  0  1  0  0  0  0 59  1  0  0  0  3  0  0  0  0  0]
 [ 0  1  0  0  0  1  0  0  0  0  0  1  1 73  0  0  0  1  0  1  0  0  0]
 [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0 67  2  0  0  0  0  0  0  0]
 [ 0  0  1  0  0  0  0  3  0  0  0  0  0  0  0 66  0  0  0  0  0  0  0]
 [ 0  0  3  0  0  0  0  1  2  0  0  0  0  0  0  0 63  0  0  0  0  0  0]
 [ 0  1  0  1  0  0  0  0  0  0  0  1  1  2  0  0  0 62  0  0  0  0  1]
 [ 9  0  1  1  0  0  0  0  0  0  0  0  0  1  0  0  1  0 51  2  0  0  0]
 [ 0  0  1  0  0  0  0  1  0  0  0  0  0  0  0  0  0  0  1 69  0  0  0]
 [ 0  1  0  0  1  1  0  2  1  0  0  2  1  1  0  0  0  0  0  1 59  0  1]
 [ 0  0  1  0  0  1  0  0  1  2  0  0  0  0  0  0  1  0  0  0  0 65  0]
 [ 0  0  1  0  0  1  0  0  1  0  0  0  0  2  0  2  0  0  0  0  3  0 60]]
```
