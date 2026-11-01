from app.ai.predict import predict_clothing
from PIL import Image

items = [
    ("Pantalon Noir", "app/uploads/demo_pantalon.jpg"),
    ("Jean Bleu", "app/uploads/demo_jean.jpg"),
    ("Chemise Blanche", "app/uploads/demo_chemise.jpg"),
    ("Baskets Blanches", "app/uploads/demo_baskets.jpg"),
    ("Veste Noire", "app/uploads/demo_veste.jpg"),
    ("Pull Beige", "app/uploads/demo_pull.jpg"),
]

for label, path in items:
    img = Image.open(path)
    res = predict_clothing(img)
    print(f"[{label}] -> Prédit: {res['category']} | Couleur: {res['color']} | Confiance: {res['confidence']}")
