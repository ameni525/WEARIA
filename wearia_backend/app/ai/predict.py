import os
import joblib
import numpy as np
from PIL import Image
from app.ai.feature_extraction import extract_clothing_features
from app.ai.color_detection import detect_dominant_color
from app.ai.train_model import MODEL_PATH, SCALER_PATH, train_and_save_knn

_model = None
_scaler = None

def get_classifier():
    global _model, _scaler
    if _model is None or _scaler is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
            print("[IA] Entraînement initial automatique...")
            _model, _scaler = train_and_save_knn()
        else:
            _model = joblib.load(MODEL_PATH)
            _scaler = joblib.load(SCALER_PATH)
    return _model, _scaler

def predict_clothing(image_input) -> dict:
    model, scaler = get_classifier()

    features = extract_clothing_features(image_input)
    features_scaled = scaler.transform([features])

    category = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    confidence = float(np.max(probabilities))

    dominant_color = detect_dominant_color(image_input)

    return {
        "category": category,
        "color": dominant_color,
        "confidence": round(confidence, 2)
    }
