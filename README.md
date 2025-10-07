# 📊 Projet EDA - Structure Complète# Structure du Projet EDAeda_project/

## 🌳 Arborescence du Projet│

# Structure du Projet EDA

```
eda_project/
│
├── .git/                         # (auto) suivi de versions Git
├── .gitignore                    # fichiers/dossiers à ignorer (voir plus bas)
│
├── pyproject.toml                # fichier principal Poetry (équiv. à setup.py + requirements.txt)
├── poetry.lock                   # versions exactes des dépendances
│
├── README.md                     # description du projet (objectif, installation, usage)
├── Dockerfile                    # (optionnel) pour conteneuriser l'app
│
├── data/                         # dossiers pour tes datasets
│   ├── raw/                      # données brutes (jamais modifiées)
│   │   └── .gitkeep
│   ├── processed/                # données nettoyées / transformées
│   │   └── .gitkeep
│   └── external/                 # données externes ou téléchargées
│       └── .gitkeep
│
├── notebooks/                    # explorations Jupyter
│   ├── 01_cleaning.ipynb
│   ├── 02_visualization.ipynb
│   └── 03_modeling.ipynb
│
├── src/                          # code source du projet
│   ├── __init__.py
│   ├── data_loader.py            # chargement / nettoyage des données
│   ├── preprocessing.py          # feature engineering
│   ├── visualization.py          # visualisation et graphiques
│   ├── modeling.py               # (optionnel) modèles statistiques / ML
│   └── utils/
│       ├── __init__.py
│       ├── logger.py             # gestion des logs
│       └── helpers.py            # fonctions utilitaires
│
├── tests/                        # tests unitaires
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_visualization.py
│   └── conftest.py
│
├── scripts/                      # scripts exécutables
│   ├── run_eda.py                # point d'entrée principal du projet
│   ├── export_charts.py          # exporter des figures
│   └── generate_report.py        # générer un rapport automatique
│
├── docs/                         # documentation technique
│   ├── index.md
│   └── conf.py                   # config ( Sphinx utilisé)
│
└── streamlit_app/ (optionnel)    # interface web Streamlit
    ├── app.py
    └── pages/
        ├── 1_Overview.py
        ├── 2_Visualizations.py
        └── 3_Modeling.py
```
