# 👗 Wearia — Assistant Vestimentaire Intelligent
**Projet d'Intégration L3 DSI2 — ISET de Radès**  
*Binôme : Mohamed Omar Ben Hamda & Ameni Homri*

---

## 🎯 Livrables Réalisés : Sprint 1 & Sprint 2

Conformément au cahier des charges et au planning de cadrage, les **Sprint 1** et **Sprint 2** sont intégralement implémentés en respectant scrupuleusement les notions étudiées en cours :

| Périmètre | Réalisations Sprint 1 | Réalisations Sprint 2 |
| :--- | :--- | :--- |
| **Backend (FastAPI)** | • Architecture FastAPI + SQLAlchemy<br>• Support PostgreSQL (mot de passe `admin`) & fallback SQLite automatique<br>• Modèles relationnels et référentiels (Catégories, Types, Couleurs, Styles)<br>• Inscription, Connexion & JWT sécurisé (BR05, BR06) | • CRUD complet des vêtements (`/clothes`) avec upload d'images (`/uploads`)<br>• CRUD des routines hebdomadaires (`/routines`) pour BR09<br>• Endpoint IA `/ai/classify`<br>• Premier moteur de recommandation : BR01 (complétude), BR02 (météo), BR03 (harmonie teintes), BR08 (vêtements sales exclus), BR09 (occasion déduite) |
| **Intelligence Artificielle** | • Pipeline HOG (Histogram of Oriented Gradients)<br>• Entraînement du modèle KNN (`KNeighborsClassifier`) avec `scikit-learn`<br>• Découpage `train_test_split` et normalisation `StandardScaler`<br>• Évaluation chiffrée (Accuracy, Rapport de classification) | • Sauvegarde & chargement des artefacts `knn_model.joblib` et `scaler.joblib`<br>• Détection de la couleur dominante via OpenCV / RGB<br>• Pipeline intégré au backend FastAPI (`predict_clothing`) retournant catégorie, couleur et score de confiance |
| **Mobile Android (Kotlin)** | • Projet natif Android Studio en Kotlin avec ViewBinding<br>• Architecture MVVM stricte (View - ViewModel - Repository - Remote)<br>• Client Retrofit + OkHttp avec `AuthInterceptor` (Bearer token)<br>• Écrans d'authentification (Connexion & Inscription) avec gestion de session locale | • Écran Dressing Virtuel avec `RecyclerView` + `ViewHolder` + `Adapter`<br>• Filtres dynamiques par catégorie (Tous, Hauts, Bas, Chaussures, Vestes)<br>• Écran de numérisation avec sélection d'image (`ActivityResultLauncher`) et appel IA `/ai/classify`<br>• Validation et correction manuelle des étiquettes (US02)<br>• Changement de statut (Sale / Propre - BR08) et suppression avec boîte de dialogue `AlertDialog`<br>• Écran de configuration des routines hebdomadaires (BR09) |

---

## 📂 Structure du Projet

```text
wearia/
├── wearia_backend/                  # Backend Python (FastAPI + IA + SQLAlchemy)
│   ├── app/
│   │   ├── main.py                  # Point d'entrée FastAPI avec CORS et routes
│   │   ├── api/                     # Contrôleurs REST (auth, clothes, routines, ai, outfits...)
│   │   ├── models/                  # Modèles de données SQLAlchemy
│   │   ├── schemas/                 # Schémas de validation Pydantic
│   │   ├── services/                # Logique métier (règles BR01 à BR09, JWT)
│   │   ├── database/                # Connexion PostgreSQL/SQLite et script de seed
│   │   ├── ai/                      # Module IA (HOG, KNN, OpenCV, train_model.py, predict.py)
│   │   │   └── models/              # knn_model.joblib, scaler.joblib
│   │   └── uploads/                 # Stockage des photos numérisées
│   ├── run.py                       # Lanceur de serveur (uvicorn)
│   ├── init_db.py                   # Initialisation et insertion des données de démonstration
│   └── requirements.txt
│
└── WeariaMobile/                    # Application Mobile Android Native (Kotlin)
    ├── app/
    │   ├── build.gradle.kts         # Dépendances (Retrofit, Coil, Coroutines, ViewBinding)
    │   ├── src/main/
    │   │   ├── AndroidManifest.xml  # Déclaration des activités et permissions
    │   │   ├── java/com/wearia/app/
    │   │   │   ├── data/            # Models, ApiService, Repositories, SessionManager
    │   │   │   ├── ui/              # Activities, Adapters RecyclerView, Dialogs
    │   │   │   ├── viewmodel/       # MVVM ViewModels et ViewModelFactory
    │   │   │   └── utils/           # Constantes (BASE_URL = 10.0.2.2)
    │   │   └── res/                 # Layouts XML, Couleurs, Strings, Menus
    ├── settings.gradle.kts
    └── build.gradle.kts
```

---

## 🚀 Guide de Démarrage Rapide

### 1. Démarrer le Backend FastAPI
Ouvrez un terminal ou VS Code dans le dossier `wearia_backend` :
```powershell
cd C:\Users\ASUS\.gemini\antigravity\scratch\wearia\wearia_backend
python run.py
```
*Le serveur démarre sur `http://localhost:8000`. Vous pouvez tester la documentation interactive Swagger sur : `http://localhost:8000/docs`.*

> **Base de données :**
> Le backend est configuré pour se connecter à PostgreSQL avec l'utilisateur `postgres` et le mot de passe `admin` sur la base `wearia_db`. Si votre service PostgreSQL n'est pas actif lors du lancement, l'application bascule automatiquement sur une base locale SQLite (`wearia.db`), vous permettant de tester sans aucun blocage !

### 2. Comptes de Démonstration Pré-configurés
Des données de test sont déjà insérées automatiquement au démarrage :
- **E-mail :** `ameni@wearia.tn`
- **Mot de passe :** `password123`
*(Garde-robe comprenant déjà 4 pièces complètes et une routine active le lundi pour l'Université)*

### 3. Ouvrir l'Application dans Android Studio
1. Lancez **Android Studio**.
2. Cliquez sur **Open** et sélectionnez le dossier :
   `C:\Users\ASUS\.gemini\antigravity\scratch\wearia\WeariaMobile`
3. Laissez Gradle synchroniser les dépendances.
4. Lancez l'application sur un émulateur Android (AVD) ou sur votre smartphone réel (en adaptant l'IP dans `Constants.kt`).
