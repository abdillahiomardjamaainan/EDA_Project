# 📚 Guide Détaillé - Structure du Projet EDA et Poetry

## 🎯 Vue d'Ensemble

Ce guide explique en détail chaque élément de l'arborescence du projet EDA et particulièrement **Poetry**, l'outil moderne de gestion des dépendances Python.

---

## 🌳 Description Détaillée de l'Arborescence

### 🔧 **Configuration et Versioning**

#### `.git/` (Dossier automatique)

- **Rôle** : Contrôle de version Git
- **Contenu** : Historique des modifications, branches, configurations
- **Action** : Créé automatiquement avec `git init`
- **Ne pas toucher** : Géré automatiquement par Git

#### `.github/workflows/` - CI/CD Automation

- **Rôle** : Actions GitHub pour l'intégration et déploiement continus
- **Contenu** : Fichiers YAML définissant les pipelines automatisés
- **Exemple** : `ci.yml` pour tests automatiques à chaque push

#### `.gitignore`

- **Rôle** : Liste des fichiers/dossiers à ignorer par Git
- **Exemple de contenu** :
  ```
  __pycache__/
  *.pyc
  .env
  .venv/
  data/raw/*
  .DS_Store
  ```
- **Pourquoi** : Évite de versionner les fichiers temporaires, sensibles ou volumineux

---

## ⚙️ **CI/CD - Intégration Continue et Déploiement**

### 🤔 **Qu'est-ce que le CI/CD ?**

**CI/CD** signifie **Continuous Integration / Continuous Deployment** :

- **CI (Intégration Continue)** : Tests automatiques à chaque modification du code
- **CD (Déploiement Continu)** : Déploiement automatique si tous les tests passent

### 📁 **Structure du Workflow**

```
.github/
└── workflows/
    └── ci.yml                    # Pipeline principal CI/CD
```

### 🎯 **À Quelle Étape Utiliser le CI/CD ?**

#### **🟢 Étape 1 : Setup Initial (Recommandé)**

- **Moment** : Dès la création du projet
- **Pourquoi** : Établit les bonnes pratiques dès le début
- **Action** : Créer le fichier `.github/workflows/ci.yml`

#### **🟡 Étape 2 : Pendant le Développement**

- **Moment** : Dès que vous avez du code à tester
- **Pourquoi** : Détecte les problèmes rapidement
- **Déclenchement** : À chaque `git push` et Pull Request

#### **🔴 Étape 3 : Avant la Production**

- **Moment** : Obligatoire avant le déploiement
- **Pourquoi** : Garantit la qualité du code
- **Validation** : Tous les tests doivent passer

### 🔄 **Pipeline CI/CD Détaillé**

Notre pipeline comprend **3 jobs principaux** :

#### **1. 🧪 Job Test**

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11] # Test sur plusieurs versions Python
```

**Étapes du job Test :**

1. **Checkout du code** : Récupère le code depuis GitHub
2. **Setup Python** : Installe la version Python spécifiée
3. **Installation Poetry** : Configure l'outil de gestion des dépendances
4. **Cache des dépendances** : Accélère les builds suivants
5. **Installation des dépendances** : `poetry install`
6. **Tests unitaires** : `pytest` avec couverture de code
7. **Formatage du code** : Vérification avec `black`
8. **Linting** : Analyse statique avec `flake8`
9. **Type checking** : Vérification des types avec `mypy`
10. **Upload de la couverture** : Envoi vers Codecov

#### **2. 🔒 Job Security**

```yaml
security:
  runs-on: ubuntu-latest
```

**Vérifications de sécurité :**

1. **Analyse du code** : Détection de vulnérabilités avec `bandit`
2. **Vérification des dépendances** : Scan des packages avec `safety`

#### **3. 📦 Job Build**

```yaml
build:
  needs: [test, security] # Ne s'exécute que si test et security passent
  if: github.ref == 'refs/heads/main' # Uniquement sur la branche main
```

**Construction du package :**

1. **Build du package** : `poetry build`
2. **Upload des artefacts** : Sauvegarde du package construit

### 🚨 **Déclencheurs du Pipeline**

```yaml
on:
  push:
    branches: [main, develop] # Push sur main ou develop
  pull_request:
    branches: [main] # Pull Request vers main
```

### 🛠️ **Configuration des Dépendances CI/CD**

Ajoutez ces dépendances dans votre `pyproject.toml` :

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.7.0"
flake8 = "^6.0.0"
mypy = "^1.5.0"
bandit = "^1.7.5"
safety = "^2.3.0"
```

````

### 🎯 **Workflow de Développement avec CI/CD**

#### **Développement Local**

```bash
# 1. Créer une branche feature
git checkout -b feature/nouvelle-fonctionnalite

# 2. Développer et tester localement
poetry run pytest
poetry run black .
poetry run flake8

# 3. Commit et push
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
````

#### **Intégration Continue**

```bash
# 4. Créer une Pull Request sur GitHub
# ✅ Le CI/CD se déclenche automatiquement
# ✅ Tests sur Python 3.9, 3.10, 3.11
# ✅ Vérification du code (black, flake8, mypy)
# ✅ Tests de sécurité (bandit, safety)

# 5. Si tout passe ✅ → Merge possible
# 6. Si échec ❌ → Corriger et repousser
```

#### **Déploiement Continu**

```bash
# 7. Merge vers main
# ✅ Pipeline complet se relance
# ✅ Build du package
# ✅ Déploiement automatique (si configuré)
```

### 🔧 **Configuration Avancée**

#### **Variables d'Environnement**

```yaml
env:
  PYTHONPATH: ${{ github.workspace }}
  ENVIRONMENT: test
```

#### **Secrets GitHub**

Pour les clés API, tokens, etc. :

1. Aller dans **Settings** → **Secrets and variables** → **Actions**
2. Ajouter des secrets (ex: `CODECOV_TOKEN`)
3. Les utiliser dans le workflow :

```yaml
env:
  CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

### ✅ **Avantages du CI/CD**

1. **🚀 Détection précoce** : Problèmes détectés immédiatement
2. **🔒 Qualité garantie** : Code toujours testé avant merge
3. **⚡ Automatisation** : Plus de tests manuels oubliés
4. **🤝 Collaboration** : Standards de qualité partagés
5. **📈 Confiance** : Déploiements sûrs et répétables

### 🚨 **Que Faire en Cas d'Échec du CI/CD ?**

#### **Échec des Tests**

```bash
# Voir les logs sur GitHub Actions
# Reproduire localement :
poetry run pytest -v
# Corriger et repousser
```

#### **Échec du Formatage**

```bash
# Corriger automatiquement :
poetry run black .
git add .
git commit -m "fix: formatting"
git push
```

#### **Échec du Linting**

```bash
# Voir les erreurs :
poetry run flake8 src tests
# Corriger et repousher
```

### 🎪 **Tests Smoke - Le Test qui Passe Toujours**

Le fichier `test_smoke.py` contient un test simple qui valide que l'environnement fonctionne :

```python
# tests/test_smoke.py
def test_smoke():
    """Test smoke - vérifie que l'environnement fonctionne."""
    assert True

def test_imports():
    """Test que les imports principaux fonctionnent."""
    import src
    import pytest
    assert True
```

**Pourquoi un test smoke ?**

- ✅ **Validation rapide** de l'environnement
- ✅ **Détection des problèmes** d'installation
- ✅ **Confiance** que les bases fonctionnent
- ✅ **Feedback immédiat** sur le setup

---

## 🐍 **POETRY - Guide Complet pour Débutants**

### 🤔 **Qu'est-ce que Poetry ?**

Poetry est un **outil moderne** qui remplace l'ancienne méthode `pip + requirements.txt + setup.py`. Il simplifie :

- ✅ Gestion des dépendances
- ✅ Création d'environnements virtuels
- ✅ Packaging du projet
- ✅ Publication sur PyPI

### 📋 **Fichiers Poetry**

#### `pyproject.toml` - Le Cerveau du Projet

C'est le **fichier principal** qui remplace plusieurs anciens fichiers :

```toml
[tool.poetry]
name = "eda-project"
version = "0.1.0"
description = "Projet d'Analyse Exploratoire de Données"
authors = ["Votre Nom <email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
pandas = "^2.0.0"
matplotlib = "^3.7.0"
seaborn = "^0.12.0"
plotly = "^5.15.0"
streamlit = "^1.25.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
flake8 = "^6.0.0"
jupyter = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Sections expliquées :**

- `[tool.poetry]` : Métadonnées du projet
- `[tool.poetry.dependencies]` : Dépendances de production
- `[tool.poetry.group.dev.dependencies]` : Dépendances de développement uniquement
- `^2.0.0` : Version minimum 2.0.0, compatible jusqu'à 3.0.0 (exclu)

#### `poetry.lock` - Le Verrou de Sécurité

- **Rôle** : Fige les versions exactes de TOUTES les dépendances
- **Exemple** : Si vous installez `pandas = "^2.0.0"`, le lock file note `pandas = "2.1.3"`
- **Avantage** : Garantit que tous les développeurs ont exactement les mêmes versions
- **Ne pas modifier** : Généré automatiquement par Poetry

### 🚀 **Commandes Poetry Essentielles**

#### Installation et Configuration

```bash
# Installation de Poetry (une seule fois)
curl -sSL https://install.python-poetry.org | python3 -

# Vérification de l'installation
poetry --version

# Initialiser un nouveau projet
poetry new mon-projet
# OU dans un dossier existant
poetry init
```

#### Gestion des Dépendances

```bash
# Installer toutes les dépendances du projet
poetry install

# Ajouter une nouvelle dépendance
poetry add pandas
poetry add matplotlib seaborn plotly

# Ajouter une dépendance de développement
poetry add --group dev pytest black

# Supprimer une dépendance
poetry remove pandas

# Mettre à jour les dépendances
poetry update
```

#### Environnement Virtuel

```bash
# Activer l'environnement virtuel
poetry shell

# Exécuter une commande dans l'environnement
poetry run python script.py
poetry run jupyter notebook
poetry run pytest

# Sortir de l'environnement
exit
```

### 🆚 **Poetry vs Ancienne Méthode**

| Ancienne Méthode                  | Poetry                                   |
| --------------------------------- | ---------------------------------------- |
| `pip install pandas`              | `poetry add pandas`                      |
| `pip freeze > requirements.txt`   | Automatique dans pyproject.toml          |
| `python -m venv venv`             | `poetry shell`                           |
| `pip install -r requirements.txt` | `poetry install`                         |
| `setup.py` complexe               | Configuration simple dans pyproject.toml |

---

## 📁 **Structure des Dossiers**

### 🗂️ **data/** - Organisation des Données

#### `data/raw/` - Données Brutes

- **Principe** : JAMAIS modifiées
- **Contenu** : Fichiers CSV, JSON, Excel originaux
- **Exemple** :
  ```
  data/raw/
  ├── sales_2023.csv
  ├── customers.xlsx
  └── api_data.json
  ```

#### `data/processed/` - Données Transformées

- **Contenu** : Données nettoyées, agrégées, transformées
- **Exemple** :
  ```
  data/processed/
  ├── clean_sales.csv
  ├── customer_segments.csv
  └── features_engineered.pkl
  ```

#### `data/external/` - Sources Externes

- **Contenu** : Données téléchargées d'APIs, web scraping
- **Exemple** :
  ```
  data/external/
  ├── weather_api.json
  ├── scraped_prices.csv
  └── demographic_data.csv
  ```

#### `.gitkeep` - Maintien des Dossiers Vides

- **Problème** : Git n'indexe pas les dossiers vides
- **Solution** : Fichier `.gitkeep` pour maintenir la structure
- **Contenu** : Fichier vide ou commentaire

### 📓 **notebooks/** - Exploration Interactive

```
notebooks/
├── 01_cleaning.ipynb      # Nettoyage et exploration initiale
├── 02_visualization.ipynb # Graphiques et visualisations
└── 03_modeling.ipynb      # Modélisation et analyse avancée
```

**Bonnes pratiques :**

- **Numérotation** : Pour indiquer l'ordre logique
- **Noms explicites** : Fonction claire de chaque notebook
- **Séparation** : Un objectif par notebook

### 💻 **src/** - Code Source Principal

#### Structure Modulaire

```
src/
├── __init__.py              # Fait de src un package Python
├── data_loader.py           # Chargement et validation des données
├── preprocessing.py         # Nettoyage et feature engineering
├── visualization.py         # Fonctions de graphiques
├── modeling.py              # Modèlesisation et algorithmes
└── utils/                   # Utilitaires partagés
    ├── __init__.py
    ├── logger.py            # Configuration des logs
    └── helpers.py           # Fonctions diverses
```

#### Exemple de `data_loader.py`

```python
import pandas as pd
from pathlib import Path

def load_raw_data(filename: str) -> pd.DataFrame:
    """Charge un fichier de données brutes."""
    file_path = Path("data/raw") / filename
    return pd.read_csv(file_path)

def save_processed_data(df: pd.DataFrame, filename: str) -> None:
    """Sauvegarde des données traitées."""
    file_path = Path("data/processed") / filename
    df.to_csv(file_path, index=False)
```

### 🧪 **tests/** - Tests Unitaires

```
tests/
├── __init__.py              # Package de tests
├── conftest.py              # Configuration pytest
├── test_data_loader.py      # Tests du module data_loader
└── test_visualization.py    # Tests des graphiques
```

#### Exemple de test

```python
# test_data_loader.py
import pytest
from src.data_loader import load_raw_data

def test_load_raw_data():
    """Test du chargement de données."""
    df = load_raw_data("sample.csv")
    assert not df.empty
    assert "column1" in df.columns
```

### 🚀 **scripts/** - Scripts d'Exécution

#### `run_eda.py` - Point d'Entrée Principal

```python
#!/usr/bin/env python3
"""Script principal pour lancer l'EDA complète."""

from src.data_loader import load_raw_data
from src.preprocessing import clean_data
from src.visualization import create_dashboard

def main():
    # 1. Charger les données
    data = load_raw_data("raw_data.csv")

    # 2. Nettoyer
    clean_data = clean_data(data)

    # 3. Visualiser
    create_dashboard(clean_data)

if __name__ == "__main__":
    main()
```

### 📚 **docs/** - Documentation

```
docs/
├── index.md                 # Documentation principale
├── conf.py                  # Configuration Sphinx
├── api.md                   # Documentation de l'API
└── tutorials.md             # Tutoriels d'utilisation
```

### 🌐 **streamlit_app/** - Interface Web

```
streamlit_app/
├── app.py                   # Application principale
└── pages/
    ├── 1_Overview.py        # Page d'accueil
    ├── 2_Visualizations.py  # Graphiques interactifs
    └── 3_Modeling.py        # Modélisation
```

---

## 🎯 **Workflow de Développement**

### 1. **Setup Initial**

```bash
# Cloner le projet
git clone <repo-url>
cd eda-project

# Installer les dépendances
poetry install

# Activer l'environnement
poetry shell
```

### 2. **Développement**

```bash
# Ajouter une nouvelle dépendance
poetry add scikit-learn

# Lancer les notebooks
poetry run jupyter notebook

# Exécuter le script principal
poetry run python scripts/run_eda.py

# Lancer l'app Streamlit
poetry run streamlit run streamlit_app/app.py
```

### 3. **Tests et Qualité**

```bash
# Lancer les tests
poetry run pytest

# Formatage du code
poetry run black .

# Vérification du style
poetry run flake8
```

---

## ✅ **Avantages de cette Structure**

### 🎯 **Organisation Claire**

- **Séparation** : Chaque type de fichier à sa place
- **Évolutivité** : Facile d'ajouter de nouveaux modules
- **Collaboration** : Structure standardisée

### 🛠️ **Poetry pour la Gestion**

- **Simplicité** : Une commande pour tout installer
- **Reproductibilité** : Même environnement partout
- **Modernité** : Standard actuel de l'écosystème Python

### 🚀 **Productivité**

- **Automation** : Scripts prêts à l'emploi
- **Tests** : Qualité du code garantie
- **Documentation** : Facilite la maintenance

---

## 🆘 **Aide-Mémoire des Commandes**

```bash
# Setup
poetry install                    # Installer le projet
poetry shell                      # Activer l'environnement

# Dépendances
poetry add <package>              # Ajouter une dépendance
poetry add --group dev <package>  # Dépendance de développement
poetry remove <package>           # Supprimer
poetry update                     # Mettre à jour

# Exécution
poetry run python <script>        # Lancer un script
poetry run jupyter notebook       # Lancer Jupyter
poetry run streamlit run app.py   # Lancer Streamlit
poetry run pytest                 # Lancer les tests

# Informations
poetry show                       # Voir les dépendances
poetry env info                   # Info sur l'environnement
```

Ce guide couvre tous les aspects essentiels pour comprendre et utiliser efficacement cette structure de projet moderne avec Poetry ! 🚀
