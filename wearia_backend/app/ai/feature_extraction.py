import numpy as np
from PIL import Image

try:
    from skimage.feature import hog
    HAS_SKIMAGE = True
except ImportError:
    HAS_SKIMAGE = False

IMAGE_SIZE = (64, 64)

def extract_clothing_features(image_input) -> np.ndarray:
    """
    Extrait les caractéristiques physiques et d'apparence du vêtement :
    1. Détection du fond et calcul de la bounding-box du vêtement (rapport largeur/hauteur réel).
    2. Détection de la séparation des deux jambes (signature distinctive des pantalons/bas).
    3. Descripteur HOG sur le vêtement recadré.
    """
    if isinstance(image_input, str):
        img_original = Image.open(image_input).convert("RGB")
    elif isinstance(image_input, Image.Image):
        img_original = image_input.convert("RGB")
    elif isinstance(image_input, np.ndarray):
        img_original = Image.fromarray(image_input).convert("RGB")
    else:
        raise ValueError("Format d'image non supporté")

    # Image en niveaux de gris pour l'analyse morphologique
    img_gray = img_original.convert("L").resize((120, 120))
    arr = np.array(img_gray, dtype=np.float32) / 255.0

    # Détection du niveau de fond (médiane des 4 bordures extérieures)
    bg_val = float(np.median(np.concatenate([
        arr[0:5, :].flatten(),
        arr[-5:, :].flatten(),
        arr[:, 0:5].flatten(),
        arr[:, -5:].flatten()
    ])))

    diff = np.abs(arr - bg_val)
    mask = diff > 0.08
    y_idx, x_idx = np.where(mask)

    if len(y_idx) > 100:
        ymin, ymax = int(np.min(y_idx)), int(np.max(y_idx))
        xmin, xmax = int(np.min(x_idx)), int(np.max(x_idx))
        gw = max(xmax - xmin, 10)
        gh = max(ymax - ymin, 10)
        garment_ratio = float(gw) / float(gh)

        # Mesure de la séparation des jambes dans la moitié inférieure
        bot = arr[int(ymin + gh * 0.45):ymax, xmin:xmax]
        bw, bh = bot.shape[1], bot.shape[0]
        if bw > 10 and bh > 5:
            mid_col = bot[:, int(bw * 0.38):int(bw * 0.62)]
            left_col = bot[:, int(bw * 0.05):int(bw * 0.35)]
            right_col = bot[:, int(bw * 0.65):int(bw * 0.95)]
            leg_gap_score = float(np.mean(np.abs(mid_col - bg_val)) - 0.5 * (np.mean(np.abs(left_col - bg_val)) + np.mean(np.abs(right_col - bg_val))))
        else:
            leg_gap_score = 0.0
    else:
        garment_ratio = float(arr.shape[1]) / float(arr.shape[0])
        leg_gap_score = 0.0

    # Recadrage et redimensionnement pour HOG (64x64)
    img_cropped = img_original.convert("L").resize(IMAGE_SIZE)
    arr_hog = np.array(img_cropped, dtype=np.float32) / 255.0

    if HAS_SKIMAGE:
        hog_feat = hog(
            arr_hog,
            orientations=9,
            pixels_per_cell=(8, 8),
            cells_per_block=(2, 2),
            block_norm="L2-Hys",
            visualize=False
        )
    else:
        gx = np.gradient(arr_hog, axis=1)
        gy = np.gradient(arr_hog, axis=0)
        mag = np.hypot(gx, gy)
        hog_feat = mag.flatten()[:1764]

    # Caractéristiques géométriques fortes
    geom_features = np.array([
        garment_ratio * 10.0,    # Ratio réel du vêtement (ex: 0.4 pour pantalon, 1.0 pour haut, 1.5 pour chaussures)
        leg_gap_score * 20.0,    # Négatif ou nul si gap entre deux jambes de pantalon
    ], dtype=np.float32)

    return np.concatenate([hog_feat, geom_features])
