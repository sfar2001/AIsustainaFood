import joblib
import numpy as np
import pandas as pd
from django.conf import settings
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import NotFittedError


class StockPredictor:
    def __init__(self):
        # Define model paths
        model_path = os.path.join(settings.BASE_DIR, 'stockmgmt/ml_models/rf_model.pkl')
        scaler_path = os.path.join(settings.BASE_DIR, 'stockmgmt/ml_models/scaler.pkl')
        encoder_path = os.path.join(settings.BASE_DIR, 'stockmgmt/ml_models/label_encoder.pkl')

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        try:
            # Load models with version checking
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.encoder = joblib.load(encoder_path)

            # Verify model types
            if not isinstance(self.model, RandomForestClassifier):
                raise ValueError("Invalid model type - expected RandomForestClassifier")

            # Test model functionality
            test_input = np.random.rand(1, 4)
            _ = self.model.predict(self.scaler.transform(test_input))

        except (FileNotFoundError, ValueError, NotFittedError) as e:
            print(f"Model loading failed: {str(e)}. Initializing dummy models.")
            self._initialize_dummy_models()
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            if hasattr(self, 'encoder'):
                joblib.dump(self.encoder, encoder_path)

    def _initialize_dummy_models(self):
        """Initialize placeholder models for development"""
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.scaler = StandardScaler()

        # Create and fit with dummy data
        X_dummy = np.random.rand(100, 4) * 100  # Simulating realistic ranges
        y_dummy = (X_dummy.sum(axis=1) > 200).astype(int)  # Simple threshold rule

        self.scaler.fit(X_dummy)
        self.model.fit(self.scaler.transform(X_dummy), y_dummy)

    def preprocess_input(self, input_data):
        """Prepare input data for prediction"""
        df = pd.DataFrame([{
            'Quantity (liters/kg)': input_data['quantity'],
            'Quantity in Stock (liters/kg)': input_data['current_stock'],
            'Minimum Stock Threshold (liters/kg)': input_data['min_threshold'],
            'Reorder Quantity (liters/kg)': input_data['reorder_qty']
        }])
        return self.scaler.transform(df)

    def predict(self, input_data):
        """Make prediction with confidence scores"""
        processed_data = self.preprocess_input(input_data)
        prediction = self.model.predict(processed_data)
        proba = self.model.predict_proba(processed_data)

        return {
            'prediction': bool(prediction[0]),
            'confidence': float(np.max(proba)),
            'probabilities': {
                'Below Threshold': float(proba[0][0]),
                'Above Threshold': float(proba[0][1])
            }
        }