import os
import glob
import joblib
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from app.ai.feature_extraction import extract_clothing_features

CLASSES = ["Haut", "Bas", "Chaussures", "Veste"]
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "knn_model.joblib")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.joblib")
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

def generate_sample_clothing_image(category: str, seed: int) -> Image.Image:
    rng = np.random.RandomState(seed)

    if category == "Bas":
        # Les pantalons sont étroits et hauts avec 2 jambes et séparation centrale
        w = 400
        h = 450
        img = Image.new("RGB", (w, h), color=(rng.randint(235, 255), rng.randint(235, 255), rng.randint(235, 255)))
        draw = ImageDraw.Draw(img)
        waist_w = rng.randint(120, 150)
        x_c = w // 2
        col = (rng.randint(20, 60), rng.randint(20, 80), rng.randint(60, 160))
        # Ceinture
        draw.rectangle([x_c - waist_w//2, 70, x_c + waist_w//2, 110], fill=col)
        # Jambe gauche
        draw.polygon([(x_c - waist_w//2, 100), (x_c - 10, 100), (x_c - 15, 410), (x_c - waist_w//2 + 5, 410)], fill=col)
        # Jambe droite
        draw.polygon([(x_c + 10, 100), (x_c + waist_w//2, 100), (x_c + waist_w//2 - 5, 410), (x_c + 15, 410)], fill=col)

    elif category == "Haut":
        # T-shirts et chemises (carré, torse plein central)
        w = 400
        h = 450
        img = Image.new("RGB", (w, h), color=(rng.randint(235, 255), rng.randint(235, 255), rng.randint(235, 255)))
        draw = ImageDraw.Draw(img)
        col = (rng.randint(40, 220), rng.randint(40, 220), rng.randint(40, 220))
        draw.polygon([(130, 80), (270, 80), (330, 160), (300, 190), (260, 150), (260, 380), (140, 380), (140, 150), (100, 190), (70, 160)], fill=col)

    elif category == "Chaussures":
        # Horizontale basse
        w = 400
        h = 450
        img = Image.new("RGB", (w, h), color=(rng.randint(235, 255), rng.randint(235, 255), rng.randint(235, 255)))
        draw = ImageDraw.Draw(img)
        col = (rng.randint(20, 200), rng.randint(20, 200), rng.randint(20, 200))
        draw.ellipse([80, 220, 320, 340], fill=col)
        draw.rectangle([110, 290, 290, 330], fill=(240, 240, 240))

    elif category == "Veste":
        w = 400
        h = 450
        img = Image.new("RGB", (w, h), color=(rng.randint(235, 255), rng.randint(235, 255), rng.randint(235, 255)))
        draw = ImageDraw.Draw(img)
        col = (rng.randint(20, 50), rng.randint(20, 50), rng.randint(20, 50))
        draw.polygon([(120, 70), (280, 70), (350, 160), (320, 200), (280, 160), (280, 370), (120, 370), (120, 160), (80, 200), (50, 160)], fill=col)
        draw.line([(200, 160), (200, 370)], fill=(200, 200, 200), width=4)

    return img

def train_and_save_knn(num_samples_per_class: int = 60):
    os.makedirs(MODEL_DIR, exist_ok=True)
    X = []
    y = []

    print("[IA] Entraînement KNN sur le jeu d'images enrichies...")

    # 1. Échantillons générés
    for cat in CLASSES:
        for i in range(num_samples_per_class):
            img = generate_sample_clothing_image(cat, i * 11 + 7)
            feat = extract_clothing_features(img)
            X.append(feat)
            y.append(cat)

    # 2. Ajout des images de référence avec poids fort
    anchors = [
        ("app/uploads/demo_pantalon.jpg", "Bas"),
        ("app/uploads/demo_jean.jpg", "Bas"),
        ("app/uploads/demo_chemise.jpg", "Haut"),
        ("app/uploads/demo_tshirt.jpg", "Haut"),
        ("app/uploads/demo_pull.jpg", "Haut"),
        ("app/uploads/demo_baskets.jpg", "Chaussures"),
        ("app/uploads/demo_chaussures.jpg", "Chaussures"),
        ("app/uploads/demo_veste.jpg", "Veste"),
    ]

    for path, cat in anchors:
        if os.path.exists(path):
            img = Image.open(path)
            feat = extract_clothing_features(img)
            # Répéter l'ancre 10 fois pour donner un poids fort aux exemples réels
            for _ in range(10):
                X.append(feat)
                y.append(cat)

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=3, metric="euclidean", weights="distance")
    knn.fit(X_train_scaled, y_train)

    y_pred = knn.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"[IA] Modèle KNN ré-entraîné ! Accuracy: {acc * 100:.2f}%")

    joblib.dump(knn, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    return knn, scaler

if __name__ == "__main__":
    train_and_save_knn()
