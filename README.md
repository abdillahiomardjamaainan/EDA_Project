# Structure du Projet EDA

```
eda_project/
│
├── .git/                                   # (auto) dépôt Git
├── .gitignore
│
├── pyproject.toml                          # Poetry (dépendances & config)
├── poetry.lock                             # (auto) versions exactes
│
├── README.md                               # description, installation, usage
├── Dockerfile                              #  conteneur
│
├── .github/
│   └── workflows/
│       └── ci.yml                          # CI (lint + tests + smoke checks)
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── external/
│       └── .gitkeep
│
├── notebooks/
│   ├── 01_cleaning.ipynb
│   ├── 02_visualization.ipynb
│   └── 03_modeling.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── modeling.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_visualization.py
│   └── test_smoke.py                      # petit test qui passe toujours
│
├── scripts/
│   ├── run_eda.py                         # point d'entrée CLI
│   ├── export_charts.py
│   └── generate_report.py
│
├── docs/
│   ├── index.md
│   └── conf.py                            # ( Sphinx)
│
└── streamlit_app/                         #  Streamlit ("Extreme Light")
    ├── app.py
    └── pages/
        ├── 1_Overview.py
        ├── 2_Visualizations.py
        └── 3_Modeling.py
```
