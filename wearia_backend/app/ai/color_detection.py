import numpy as np
from PIL import Image

PALETTE_COULEURS = {
    "Noir": np.array([25, 25, 25]),
    "Blanc": np.array([245, 245, 245]),
    "Bleu": np.array([35, 90, 200]),
    "Bleu Marine": np.array([15, 30, 70]),
    "Gris": np.array([128, 128, 128]),
    "Beige": np.array([220, 200, 165]),
    "Rouge": np.array([195, 35, 35]),
    "Marron": np.array([105, 55, 30]),
    "Vert": np.array([45, 135, 55]),
    "Kaki": np.array([95, 105, 60]),
}

def detect_dominant_color(image_input) -> str:
    """
    Extrait précisément la couleur dominante du vêtement sur une vraie photo de smartphone :
    1. Analyse les bords de l'image pour détecter la couleur du fond (lit, sol, mur, table).
    2. Isole la zone centrale (où se situe le vêtement).
    3. Élimine les pixels correspondant au fond.
    4. Trouve la couleur la plus proche dans le référentiel Wearia.
    """
    try:
        if isinstance(image_input, str):
            img = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, Image.Image):
            img = image_input.convert("RGB")
        elif isinstance(image_input, np.ndarray):
            img = Image.fromarray(image_input).convert("RGB")
        else:
            return "Noir"

        # Redimensionner pour vitesse et lissage du bruit
        img = img.resize((100, 100))
        arr = np.array(img, dtype=np.float32)

        # Échantillonner les bords pour estimer la couleur d'arrière-plan
        top_edge = arr[0:5, :, :].reshape(-1, 3)
        bottom_edge = arr[95:100, :, :].reshape(-1, 3)
        left_edge = arr[:, 0:5, :].reshape(-1, 3)
        right_edge = arr[:, 95:100, :].reshape(-1, 3)
        border_pixels = np.vstack([top_edge, bottom_edge, left_edge, right_edge])
        bg_color = np.median(border_pixels, axis=0)

        # Zone centrale (25% à 75% en hauteur et largeur)
        center_crop = arr[20:80, 20:80, :].reshape(-1, 3)

        # Calcul de la distance de chaque pixel central par rapport au fond
        diff = np.linalg.norm(center_crop - bg_color, axis=1)

        # On garde les pixels distincts du fond (distance > 30)
        foreground_pixels = center_crop[diff > 30]

        if len(foreground_pixels) > 50:
            dominant_rgb = np.median(foreground_pixels, axis=0)
        else:
            # Si le vêtement prend toute l'image ou pas de fond distinct
            dominant_rgb = np.median(center_crop, axis=0)

        # Correspondance avec la palette la plus proche
        best_color = "Noir"
        min_dist = float("inf")
        for nom, rgb in PALETTE_COULEURS.items():
            dist = np.linalg.norm(dominant_rgb - rgb)
            if dist < min_dist:
                min_dist = dist
                best_color = nom

        return best_color
    except Exception as e:
        print("[COLOR DETECTION ERROR]", e)
        return "Noir"
