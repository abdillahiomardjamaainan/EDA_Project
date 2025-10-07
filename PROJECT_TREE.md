# Structure Complète du Projet EDA

```
eda_project/
│
├── � .git/                        # Dossier de versioning Git (contrôle de version)
├── 📄 .gitignore                   # Fichiers/dossiers à ignorer par Git
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 ci.yml               # CI/CD (tests automatisés, lint, build)
│
├── � .venv/                       # Environnement virtuel Python
│
├── �📄 README.md                    # Présentation du projet
├── 📄 requirements.txt             # Dépendances Python
├── 📄 setup.py                     # Packaging et installation du projet
├── � Dockerfile                   # Conteneurisation du projet
├── � PROJECT_TREE.md              # Structure du projet (ce fichier)
│
├── 📁 data/                        # Données utilisées dans l'analyse
│   ├── 📁 raw/                     # Données brutes non traitées
│   ├── 📁 processed/               # Données nettoyées et transformées
│   └── � external/                # Données externes ou provenant d'APIs
│
├── 📁 notebooks/                   # Notebooks Jupyter pour l'exploration
│   ├── 📄 cleaning.ipynb           # 01 - Nettoyage des données
│   ├── 📄 modeling.ipynb           # 02 - Modélisation et analyse
│   └── 📄 visualisation.ipynb      # 03 - Visualisations et graphiques
│
├── 📁 src/                         # Code source principal du projet
│   ├── 📄 __init__.py
│   ├── 📄 data_loader.py           # Chargement et nettoyage des données
│   ├── 📄 preprocessing.py         # Feature engineering et préparation
│   ├── 📄 visualization.py         # Graphiques et dashboards
│   ├── 📄 modeling.py              # Modèles statistiques et Machine Learning
│   │
│   └── 📁 utils/
│       ├── 📄 __init__.py
│       ├── 📄 logger.py            # Gestion des logs
│       └── 📄 helpers.py           # Fonctions utilitaires communes
│
├── 📁 tests/                       # Tests unitaires et d'intégration
│   ├── 📄 __init__.py
│   ├── 📄 conftest.py              # Configuration des tests pytest
│   ├── 📄 test_data_loader.py      # Tests du module data_loader
│   └── 📄 test_visualization.py    # Tests du module visualization
│
├── 📁 scripts/                     # Scripts exécutables autonomes
│   ├── � run_eda.py               # Point d'entrée principal de l'EDA
│   ├── 📄 export_charts.py         # Export des graphiques générés
│   └── 📄 generate_report.py       # Génération de rapports automatisés
│
├── 📁 docs/                        # Documentation du projet
│   ├── 📄 index.md                 # Page d'accueil de la documentation
│   └── 📄 conf.py                  # Configuration Sphinx (si utilisé)
│
```

## � Description Détaillée des Dossiers

### 🔧 **Configuration et Versioning**

- **`.git/`**: Dossier de contrôle de version Git
- **`.gitignore`**: Spécifie les fichiers à ignorer par Git
- **`.github/workflows/`**: Actions GitHub pour CI/CD automatisé
- **`.venv/`**: Environnement virtuel Python isolé

### 📦 **Fichiers de Configuration**

- **`README.md`**: Documentation principale du projet
- **`requirements.txt`**: Liste des dépendances Python
- **`setup.py`**: Configuration pour l'installation du package
- **`Dockerfile`**: Instructions pour la conteneurisation

### 🗂️ **Données (`data/`)**

- **`raw/`**: Données brutes non modifiées provenant des sources originales
- **`processed/`**: Données nettoyées, transformées et prêtes pour l'analyse
- **`external/`**: Données provenant d'APIs externes ou sources tierces

### 📓 **Notebooks (`notebooks/`)**

- **`cleaning.ipynb`**: Exploration et nettoyage des données
- **`modeling.ipynb`**: Développement et évaluation des modèles
- **`visualisation.ipynb`**: Création de graphiques et visualisations

### 🧩 **Code Source (`src/`)**

- **`data_loader.py`**: Fonctions de chargement et validation des données
- **`preprocessing.py`**: Feature engineering et transformation des données
- **`visualization.py`**: Génération de graphiques et tableaux de bord
- **`modeling.py`**: Modèles statistiques et algorithmes de Machine Learning
- **`utils/`**: Modules utilitaires (logging, helpers, configurations)

### 🧪 **Tests (`tests/`)**

- **`conftest.py`**: Configuration globale des tests pytest
- **`test_*.py`**: Tests unitaires pour chaque module principal
- Assure la qualité et la fiabilité du code

### ⚙️ **Scripts (`scripts/`)**

- **`run_eda.py`**: Point d'entrée principal pour exécuter l'EDA complète
- **`export_charts.py`**: Export automatisé des visualisations
- **`generate_report.py`**: Génération de rapports PDF/HTML

### 📚 **Documentation (`docs/`)**

- **`index.md`**: Page d'accueil de la documentation
- **`conf.py`**: Configuration Sphinx pour la génération automatique

### 🌐 **Application Web (`streamlit_app/`)**

- **`app.py`**: Interface utilisateur principale Streamlit
- **`pages/`**: Pages modulaires de l'application web
  - Vue d'ensemble, visualisations interactives, modélisation

## 🏗️ Architecture et Bonnes Pratiques

### ✅ **Principes Appliqués**

1. **Séparation des préoccupations**: Code, données, tests, documentation séparés
2. **Modularité**: Code organisé en modules réutilisables
3. **Reproductibilité**: Environnement virtuel et dépendances figées
4. **Qualité**: Tests automatisés et CI/CD
5. **Documentation**: README, docstrings et documentation technique
6. **Interactivité**: Interface web pour les utilisateurs finaux

### 📊 **Flux de Travail EDA**

```
Données brutes → Nettoyage → Transformation → Visualisation → Modélisation → Rapport
     ↓              ↓            ↓              ↓             ↓           ↓
  data/raw/   →  notebooks/  →  src/      →  streamlit/  →  scripts/  → docs/
```

### 🚀 **Déploiement et Production**

- **Docker**: Conteneurisation pour un déploiement cohérent
- **CI/CD**: Tests automatisés à chaque modification
- **Streamlit**: Interface web déployable sur cloud
- **Documentation**: Auto-générée et maintenue à jour
