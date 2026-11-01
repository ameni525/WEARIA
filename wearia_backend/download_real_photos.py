import urllib.request
import os

images = {
    "demo_chemise.jpg": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&auto=format&fit=crop&q=80",
    "demo_jean.jpg": "https://images.unsplash.com/photo-1542272604-780c96856592?w=600&auto=format&fit=crop&q=80",
    "demo_pantalon.jpg": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&auto=format&fit=crop&q=80",
    "demo_baskets.jpg": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&auto=format&fit=crop&q=80",
    "demo_veste.jpg": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=600&auto=format&fit=crop&q=80",
    "demo_pull.jpg": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=600&auto=format&fit=crop&q=80",
    "demo_tshirt.jpg": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80",
    "demo_chaussures.jpg": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=600&auto=format&fit=crop&q=80"
}

out_dir = r"C:\Users\ASUS\.gemini\antigravity\scratch\wearia\wearia_backend\app\uploads"
os.makedirs(out_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

for name, url in images.items():
    dest = os.path.join(out_dir, name)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response, open(dest, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Downloaded {name} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {name}: {e}")
