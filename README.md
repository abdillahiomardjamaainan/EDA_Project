eda_project/
│
├── � .git/ # Dossier de versioning Git (contrôle de version)
├── 📄 .gitignore # Fichiers/dossiers à ignorer par Git
├── 📁 .github/
│ └── 📁 workflows/
│ └── 📄 ci.yml # CI/CD (tests automatisés, lint, build)
│
├── � .venv/ # Environnement virtuel Python
│
├── �📄 README.md # Présentation du projet
├── 📄 requirements.txt # Dépendances Python
├── 📄 setup.py # Packaging et installation du projet
├── � Dockerfile # Conteneurisation du projet
├── � PROJECT_TREE.md # Structure du projet (ce fichier)
│
├── 📁 data/ # Données utilisées dans l'analyse
│ ├── 📁 raw/ # Données brutes non traitées
│ ├── 📁 processed/ # Données nettoyées et transformées
│ └── � external/ # Données externes ou provenant d'APIs
│
├── 📁 notebooks/ # Notebooks Jupyter pour l'exploration
│ ├── 📄 cleaning.ipynb # 01 - Nettoyage des données
│ ├── 📄 modeling.ipynb # 02 - Modélisation et analyse
│ └── 📄 visualisation.ipynb # 03 - Visualisations et graphiques
│
├── 📁 src/ # Code source principal du projet
│ ├── 📄 **init**.py
│ ├── 📄 data_loader.py # Chargement et nettoyage des données
│ ├── 📄 preprocessing.py # Feature engineering et préparation
│ ├── 📄 visualization.py # Graphiques et dashboards
│ ├── 📄 modeling.py # Modèles statistiques et Machine Learning
│ │
│ └── 📁 utils/
│ ├── 📄 **init**.py
│ ├── 📄 logger.py # Gestion des logs
│ └── 📄 helpers.py # Fonctions utilitaires communes
│
├── 📁 tests/ # Tests unitaires et d'intégration
│ ├── 📄 **init**.py
│ ├── 📄 conftest.py # Configuration des tests pytest
│ ├── 📄 test_data_loader.py # Tests du module data_loader
│ └── 📄 test_visualization.py # Tests du module visualization
│
├── 📁 scripts/ # Scripts exécutables autonomes
│ ├── � run_eda.py # Point d'entrée principal de l'EDA
│ ├── 📄 export_charts.py # Export des graphiques générés
│ └── 📄 generate_report.py # Génération de rapports automatisés
│
├── 📁 docs/ # Documentation du projet
│ ├── 📄 index.md # Page d'accueil de la documentation
│ └── 📄 conf.py # Configuration Sphinx (si utilisé)
│
