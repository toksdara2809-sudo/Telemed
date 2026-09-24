from django.test import TestCase
from devices.services.diagnosis import predict_condition, SYMPTOMS


class DiagnosisServiceTests(TestCase):
    def test_predict_returns_list(self):
        result = predict_condition(['fever', 'cough'])
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_predict_returns_condition_strings(self):
        result = predict_condition(['fever', 'cough', 'fatigue', 'sore_throat'])
        for condition, confidence in result:
            self.assertIsInstance(condition, str)
            self.assertIsInstance(confidence, (float, int))

    def test_confidence_between_0_and_100(self):
        result = predict_condition(['fever', 'cough', 'fatigue', 'body_ache', 'sore_throat'])
        for condition, confidence in result:
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 100.0)

    def test_predictions_ordered_by_confidence(self):
        result = predict_condition(['fever', 'cough'])
        confidences = [c for _, c in result]
        self.assertEqual(confidences, sorted(confidences, reverse=True))

    def test_different_symptoms_give_different_results(self):
        flu_symptoms = ['fever', 'cough', 'fatigue', 'body_ache', 'sore_throat']
        migraine_symptoms = ['headache', 'nausea', 'vision_blur', 'dizziness']
        flu_result = predict_condition(flu_symptoms)
        migraine_result = predict_condition(migraine_symptoms)
        top_flu = flu_result[0][0]
        top_migraine = migraine_result[0][0]
        self.assertNotEqual(top_flu, top_migraine)

    def test_all_symptoms_list_defined(self):
        self.assertIsInstance(SYMPTOMS, list)
        self.assertGreater(len(SYMPTOMS), 0)
        self.assertIn('fever', SYMPTOMS)
        self.assertIn('cough', SYMPTOMS)

    def test_empty_symptoms_returns_results(self):
        result = predict_condition([])
        self.assertIsInstance(result, list)
