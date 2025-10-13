# 📊 Guide Étape par Étape - Projet EDA Complet

## 🎯 Vue d'Ensemble du Processus EDA

Ce guide détaille toutes les étapes d'un projet d'Analyse Exploratoire de Données (EDA) en utilisant la structure moderne avec Poetry et CI/CD.

---

## 📋 PHASE 1: SETUP & CONFIGURATION DU PROJET

### 🔧 Étape 1.1: Initialisation du Projet

- [ ] Créer le dossier projet
- [ ] Initialiser Git: `git init`
- [ ] Configurer Poetry: `poetry init`
- [ ] Créer l'arborescence des dossiers
- [ ] Ajouter `.gitignore` approprié
- [ ] Setup CI/CD (`github/workflows/ci.yml`)

### 🐍 Étape 1.2: Configuration Poetry

- [ ] Définir les dépendances principales dans `pyproject.toml`:
  - pandas, numpy (manipulation de données)
  - matplotlib, seaborn, plotly (visualisation)
  - jupyter (notebooks)
  - streamlit (interface web)
- [ ] Ajouter les dépendances de développement:
  - pytest, black, flake8 (qualité du code)
  - mypy (type checking)
- [ ] Installer: `poetry install`
- [ ] Tester l'environnement: `poetry shell`

### 📁 Étape 1.3: Structure des Modules

- [ ] Créer `src/__init__.py`
- [ ] Créer `src/data_loader.py` (fonctions de chargement)
- [ ] Créer `src/utils/helpers.py` (fonctions utilitaires)
- [ ] Créer `src/utils/logger.py` (configuration des logs)
- [ ] Créer `tests/test_smoke.py` (test basique)

---

## 📥 PHASE 2: COLLECTE & CHARGEMENT DES DONNÉES

### 🎯 **Répartition des Responsabilités par Fichier**

#### 📁 **data/raw/** - Stockage des Données Brutes

- [ ] **Fichiers CSV/JSON/Excel** : Données originales NON MODIFIÉES
- [ ] **README.md** : Documentation des sources de données
- [ ] **.gitkeep** : Maintenir le dossier dans Git

#### 💻 **src/data_loader.py** - Module de Chargement Central

**RESPONSABILITÉ** : Centraliser TOUT le chargement des données

**🔧 Ce qu'on doit y mettre :**

- [ ] **Fonctions de chargement spécialisées** pour chaque dataset

```python
def load_recipes(file_name: str = "RAW_recipes.csv") -> pd.DataFrame:
def load_interactions(file_name: str = "RAW_interactions.csv") -> pd.DataFrame:
def load_all_datasets() -> dict:  # Charge tout en une fois
```

- [ ] **Gestion des chemins absolus** (éviter les problèmes de répertoire)

```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW_PATH = PROJECT_ROOT / "data" / "raw"
```

- [ ] **Validation basique des données chargées**

```python
def validate_dataframe(df: pd.DataFrame, expected_columns: list) -> bool:
    # Vérifier que les colonnes attendues existent
    # Vérifier que le DataFrame n'est pas vide
```

- [ ] **Gestion d'erreurs robuste**

```python
if not file_path.exists():
    raise FileNotFoundError(f"Fichier non trouvé : {file_path}")
```

- [ ] **Logs informatifs** pour le debugging

```python
print(f"✅ {file_name} chargé: {df.shape[0]} lignes, {df.shape[1]} colonnes")
```

- [ ] **Fonction de sanité check**

```python
def sanity_check():
    """Vérifie que tous les fichiers sont accessibles"""
    # Lister les fichiers disponibles
    # Tester le chargement de chaque dataset
```

**❌ Ce qu'on NE doit PAS mettre dans data_loader.py :**

- Nettoyage des données (c'est pour preprocessing.py)
- Analyses ou visualisations
- Transformations des données

#### 📓 **notebooks/01_cleaning.ipynb** - Exploration Initiale

**RESPONSABILITÉ** : Première découverte et nettoyage interactif

**🔧 Ce qu'on doit y faire :**

- [ ] **Configuration des imports**

```python
# Cellule 1: Configuration des chemins
import sys, os
from pathlib import Path
sys.path.append(str(Path().absolute().parent))

# Cellule 2: Imports des modules
from src.data_loader import load_recipes, load_interactions, sanity_check
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns
```

- [ ] **Test du chargement des données**

```python
# Cellule 3: Sanity check
sanity_check()

# Cellule 4: Chargement des datasets
recipes = load_recipes()
interactions = load_interactions()
```

**❌ Ce qu'on NE fait PAS dans 01_cleaning.ipynb :**

- Créer des fonctions complexes (c'est pour les modules .py)
- Analyses poussées (c'est pour 02_visualization.ipynb)

---

## 🔍 PHASE 3: EXPLORATION INITIALE (notebooks/01_cleaning.ipynb)

### 🎯 **Structure Détaillée du Notebook 01_cleaning.ipynb**

#### 📝 **Cellule 1-2 : Setup et Imports**

- [ ] Configuration des chemins et imports des modules
- [ ] Test de connectivité avec les données

#### 📊 **Cellules 3-5 : Vue d'Ensemble**

```python
# Cellule 3: Chargement et première inspection
recipes = load_recipes()
interactions = load_interactions()

print("📊 RÉSUMÉ DES DATASETS")
print(f"Recettes: {recipes.shape}")
print(f"Interactions: {interactions.shape}")

# Cellule 4: Structure des données
recipes.info()
interactions.info()

# Cellule 5: Aperçu des données
display(recipes.head())
display(interactions.head())
```

#### 🔍 **Cellules 6-10 : Qualité des Données**

```python
# Cellule 6: Valeurs manquantes
print("❓ VALEURS MANQUANTES")
print(recipes.isnull().sum())
print(interactions.isnull().sum())

# Cellule 7: Doublons
print("🔁 DOUBLONS")
print(f"Recettes dupliquées: {recipes.duplicated().sum()}")
print(f"Interactions dupliquées: {interactions.duplicated().sum()}")

# Cellule 8: Types de données
print("📋 TYPES DE DONNÉES")
display(recipes.dtypes)
display(interactions.dtypes)

# Cellule 9: Statistiques descriptives
recipes.describe()

# Cellule 10: Valeurs uniques pour variables catégorielles
for col in recipes.select_dtypes(include=['object']).columns:
    print(f"{col}: {recipes[col].nunique()} valeurs uniques")
```

#### � **Cellules 11-15 : Relations Entre Datasets**

```python
# Cellule 11: Clés de jointure
print("🔑 CLÉS DE JOINTURE")
recipes_ids = set(recipes['id']) if 'id' in recipes.columns else set()
interaction_recipe_ids = set(interactions['recipe_id']) if 'recipe_id' in interactions.columns else set()

# Cellule 12: Intégrité référentielle
common_ids = recipes_ids.intersection(interaction_recipe_ids)
print(f"Recettes avec interactions: {len(common_ids)}")
print(f"Recettes sans interactions: {len(recipes_ids - interaction_recipe_ids)}")

# Cellule 13: Test de jointure
if len(common_ids) > 0:
    test_join = recipes.merge(interactions, left_on='id', right_on='recipe_id', how='inner')
    print(f"Jointure réussie: {test_join.shape}")
```

---

## 🧹 PHASE 4: NETTOYAGE DES DONNÉES

### 🎯 **Répartition entre Notebook et Module**

#### � **notebooks/01_cleaning.ipynb (Suite)** - Nettoyage Interactif

**RESPONSABILITÉ** : Expérimenter et décider des stratégies de nettoyage

**🔧 Cellules 16-25 : Traitement des Valeurs Manquantes**

```python
# Cellule 16: Analyse des patterns de valeurs manquantes
import missingno as msno
msno.matrix(recipes)

# Cellule 17: Décisions de nettoyage par colonne
missing_analysis = recipes.isnull().sum()
for col, missing_count in missing_analysis.items():
    if missing_count > 0:
        missing_pct = (missing_count / len(recipes)) * 100
        print(f"{col}: {missing_count} manquants ({missing_pct:.1f}%)")

        # Décision stratégique
        if missing_pct > 50:
            print(f"  → RECOMMANDATION: Supprimer la colonne {col}")
        elif missing_pct > 20:
            print(f"  → RECOMMANDATION: Imputer {col}")
        else:
            print(f"  → RECOMMANDATION: Supprimer les lignes pour {col}")

# Cellule 18: Test des stratégies de nettoyage
recipes_cleaned = recipes.copy()

# Exemple: Supprimer les colonnes avec trop de valeurs manquantes
high_missing_cols = missing_analysis[missing_analysis > len(recipes) * 0.5].index
recipes_cleaned = recipes_cleaned.drop(columns=high_missing_cols)

# Cellule 19: Validation du nettoyage
print("AVANT NETTOYAGE:", recipes.shape)
print("APRÈS NETTOYAGE:", recipes_cleaned.shape)
```

#### 💻 **src/preprocessing.py** - Fonctions de Nettoyage Réutilisables

**RESPONSABILITÉ** : Implémenter les décisions prises dans le notebook

**🔧 Ce qu'on doit y mettre :**

```python
# src/preprocessing.py
import pandas as pd
from typing import List, Optional

def clean_recipes(df: pd.DataFrame) -> pd.DataFrame:
    """Applique toutes les transformations de nettoyage aux recettes"""
    df_clean = df.copy()

    # Appliquer toutes les fonctions de nettoyage
    df_clean = remove_high_missing_columns(df_clean)
    df_clean = standardize_date_formats(df_clean)
    df_clean = clean_text_columns(df_clean)

    return df_clean

def remove_high_missing_columns(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Supprime les colonnes avec trop de valeurs manquantes"""
    # ... implémentation

def standardize_date_formats(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise les formats de dates"""
    # ... implémentation

def impute_missing_values(df: pd.DataFrame, strategy: dict) -> pd.DataFrame:
    """Impute les valeurs manquantes selon la stratégie donnée"""
    # ... implémentation
```

#### 📊 **data/processed/** - Données Nettoyées

**RESPONSABILITÉ** : Stocker les résultats du nettoyage

**🔧 Ce qu'on doit y sauvegarder :**

- [ ] **clean_recipes.csv** : Recettes nettoyées
- [ ] **clean_interactions.csv** : Interactions nettoyées
- [ ] **cleaning_report.txt** : Rapport des transformations appliquées

---

## 📊 PHASE 5: ANALYSE EXPLORATOIRE (notebooks/02_visualization.ipynb)

### 🎯 **Structure du Notebook de Visualisation**

#### 📓 **notebooks/02_visualization.ipynb** - Analyses Visuelles

**RESPONSABILITÉ** : Explorer visuellement les données nettoyées

**🔧 Cellules 1-5 : Setup et Chargement**

```python
# Cellule 1: Setup
import sys
from pathlib import Path
sys.path.append(str(Path().absolute().parent))

# Cellule 2: Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from src.data_loader import load_recipes, load_interactions
from src.preprocessing import clean_recipes, clean_interactions

# Cellule 3: Chargement des données nettoyées
recipes = clean_recipes(load_recipes())
interactions = clean_interactions(load_interactions())

# Cellule 4: Configuration des graphiques
plt.style.use('default')
sns.set_palette("husl")
```

#### 📈 **Cellules 6-15 : Analyse Univariée**

```python
# Cellule 6: Distribution des variables numériques
numeric_cols = recipes.select_dtypes(include=['int64', 'float64']).columns
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
for i, col in enumerate(numeric_cols[:4]):
    recipes[col].hist(ax=axes[i//2, i%2], bins=30)
    axes[i//2, i%2].set_title(f'Distribution de {col}')

# Cellule 7: Box plots pour détecter les outliers
for col in numeric_cols:
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=recipes[col])
    plt.title(f'Box plot - {col}')
    plt.show()
```

#### 💻 **src/visualization.py** - Fonctions de Visualisation

**RESPONSABILITÉ** : Créer des fonctions de graphiques réutilisables

**🔧 Ce qu'on doit y mettre :**

```python
# src/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def create_distribution_plots(df: pd.DataFrame, columns: List[str]) -> None:
    """Crée des histogrammes pour les colonnes spécifiées"""
    # ... implémentation

def create_correlation_heatmap(df: pd.DataFrame) -> plt.Figure:
    """Crée une heatmap de corrélation"""
    # ... implémentation

def create_interactive_scatter(df: pd.DataFrame, x: str, y: str) -> None:
    """Crée un scatter plot interactif avec Plotly"""
    # ... implémentation
```

---

## 🤖 PHASE 6: MODÉLISATION (notebooks/03_modeling.ipynb)

### 🎯 **Structure du Notebook de Modélisation**

#### 📓 **notebooks/03_modeling.ipynb** - Modélisation Exploratoire

**RESPONSABILITÉ** : Créer des modèles exploratoires pour comprendre les données

#### 💻 **src/modeling.py** - Fonctions de Modélisation

**RESPONSABILITÉ** : Implémenter les modèles réutilisables

**🔧 Ce qu'on doit y mettre :**

```python
# src/modeling.py
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

def prepare_features(df: pd.DataFrame, target_col: str) -> tuple:
    """Prépare les features pour la modélisation"""
    # ... implémentation

def train_baseline_model(X_train, y_train) -> object:
    """Entraîne un modèle de base"""
    # ... implémentation

def evaluate_model(model, X_test, y_test) -> dict:
    """Évalue les performances du modèle"""
    # ... implémentation
```

---

## 🚀 PHASE 7: AUTOMATISATION ET SCRIPTS

### 🎯 **Répartition des Scripts**

#### ⚙️ **scripts/run_eda.py** - Pipeline Principal

**RESPONSABILITÉ** : Orchestrer tout le pipeline EDA

```python
#!/usr/bin/env python3
"""Script principal pour exécuter l'EDA complète"""

from src.data_loader import load_all_datasets, sanity_check
from src.preprocessing import clean_recipes, clean_interactions
from src.visualization import generate_all_plots
from src.modeling import run_baseline_models

def main():
    print("🚀 DÉMARRAGE DU PIPELINE EDA")

    # 1. Vérification
    sanity_check()

    # 2. Chargement
    datasets = load_all_datasets()

    # 3. Nettoyage
    clean_data = clean_all_datasets(datasets)

    # 4. Visualisations
    generate_all_plots(clean_data)

    # 5. Modélisation
    models = run_baseline_models(clean_data)

    print("✅ PIPELINE TERMINÉ")

if __name__ == "__main__":
    main()
```

#### � **scripts/export_charts.py** - Export des Graphiques

**RESPONSABILITÉ** : Sauvegarder tous les graphiques

#### 📋 **scripts/generate_report.py** - Génération de Rapport

**RESPONSABILITÉ** : Créer un rapport HTML/PDF automatique

---

## 🌐 PHASE 8: INTERFACE STREAMLIT

### 🎯 **Structure de l'Application**

#### 🎯 **streamlit_app/app.py** - Application Principale

**RESPONSABILITÉ** : Point d'entrée de l'interface web

#### 📄 **streamlit_app/pages/** - Pages de l'Application

- **1_Overview.py** : Vue d'ensemble et métriques clés
- **2_Visualizations.py** : Graphiques interactifs
- **3_Modeling.py** : Résultats des modèles

---

## ✅ **RÈGLES DE QUALITÉ DU CODE À SUIVRE**

### 🏗️ **Architecture Modulaire**

- [ ] **Un fichier = Une responsabilité** claire
- [ ] **Fonctions courtes** (< 50 lignes)
- [ ] **Noms explicites** pour variables et fonctions
- [ ] **Documentation** de chaque fonction

### 🔧 **Bonnes Pratiques Python**

- [ ] **Type hints** sur les fonctions importantes
- [ ] **Gestion d'erreurs** avec try/except
- [ ] **Logs informatifs** plutôt que print()
- [ ] **Validation des entrées** de fonctions

### 📝 **Documentation**

- [ ] **Docstrings** pour chaque fonction
- [ ] **Commentaires** pour la logique complexe
- [ ] **README** à jour avec instructions d'usage
- [ ] **Changelog** des modifications importantes

### 🧪 **Tests**

- [ ] **Test smoke** pour chaque module
- [ ] **Tests unitaires** pour fonctions critiques
- [ ] **Tests d'intégration** pour le pipeline
- [ ] **CI/CD** qui valide automatiquement

---

## 📊 PHASE 5: ANALYSE EXPLORATOIRE (Notebook 02_visualization)

### 🔢 Étape 5.1: Analyse Univariée

- [ ] **Variables numériques:**
  - Histogrammes et courbes de densité
  - Box plots pour détecter les outliers
  - Statistiques descriptives détaillées
- [ ] **Variables catégorielles:**
  - Graphiques en barres des fréquences
  - Diagrammes en secteurs si approprié
  - Analyse des modalités rares

### 🔗 Étape 5.2: Analyse Bivariée

- [ ] **Numérique vs Numérique:**
  - Matrices de corrélation et heatmaps
  - Scatter plots avec tendances
  - Identification des relations non-linéaires
- [ ] **Catégorielle vs Numérique:**
  - Box plots par catégorie
  - Violin plots pour les distributions
  - Tests statistiques (ANOVA, t-test)
- [ ] **Catégorielle vs Catégorielle:**
  - Tables de contingence
  - Heatmaps de fréquences croisées
  - Tests du chi-carré

### 🕸️ Étape 5.3: Analyse Multivariée

- [ ] Matrices de scatter plots (pairplot)
- [ ] Analyse en composantes principales (PCA) exploratoire
- [ ] Clustering exploratoire (K-means)
- [ ] Analyse des interactions entre variables

### 📈 Étape 5.4: Analyses Spécialisées

- [ ] **Séries temporelles** (si applicable):
  - Évolution dans le temps
  - Saisonnalité et tendances
  - Autocorrélations
- [ ] **Données géographiques** (si applicable):
  - Cartes choroplèthes
  - Analyses spatiales
- [ ] **Données textuelles** (si applicable):
  - Nuages de mots
  - Analyse de sentiment

---

## 🤖 PHASE 6: MODÉLISATION EXPLORATOIRE (Notebook 03_modeling)

### 🎯 Étape 6.1: Définition des Objectifs

- [ ] Identifier le type de problème:
  - Classification (binaire/multiclasse)
  - Régression
  - Clustering
  - Association
- [ ] Définir les variables cibles
- [ ] Choisir les métriques d'évaluation

### 🔧 Étape 6.2: Préparation des Données pour ML

- [ ] Encodage des variables catégorielles
- [ ] Normalisation/standardisation des variables numériques
- [ ] Création de variables d'interaction
- [ ] Division train/validation/test

### 🧠 Étape 6.3: Modèles de Base (Baseline)

- [ ] Modèles simples (régression linéaire, arbres de décision)
- [ ] Modèles naïfs (prédiction par moyenne/mode)
- [ ] Évaluation des performances de base

### 📊 Étape 6.4: Modèles Avancés

- [ ] Ensemble methods (Random Forest, Gradient Boosting)
- [ ] Modèles de clustering (K-means, DBSCAN)
- [ ] Validation croisée
- [ ] Tuning des hyperparamètres

### 🔍 Étape 6.5: Interprétation des Modèles

- [ ] Importance des features
- [ ] Analyse des résidus
- [ ] Courbes d'apprentissage
- [ ] Matrices de confusion (classification)

---

## 🚀 PHASE 7: PRODUCTION DES LIVRABLES

### 📋 Étape 7.1: Scripts d'Automatisation

- [ ] **`scripts/run_eda.py`**: Pipeline complet automatisé
- [ ] **`scripts/export_charts.py`**: Export de tous les graphiques
- [ ] **`scripts/generate_report.py`**: Génération de rapport HTML/PDF

### 🌐 Étape 7.2: Interface Streamlit

- [ ] **Page 1 - Overview**: Métriques clés et résumé
- [ ] **Page 2 - Visualizations**: Graphiques interactifs
- [ ] **Page 3 - Modeling**: Résultats des modèles
- [ ] Tests et optimisation de l'interface

### 📚 Étape 7.3: Documentation

- [ ] Finaliser le README.md
- [ ] Documenter l'API dans `docs/`
- [ ] Créer un guide utilisateur
- [ ] Documenter les décisions prises et insights

---

## ✅ PHASE 8: VALIDATION & DÉPLOIEMENT

### 🧪 Étape 8.1: Tests et Qualité

- [ ] Tests unitaires pour tous les modules
- [ ] Tests d'intégration du pipeline
- [ ] Validation du CI/CD
- [ ] Code review et refactoring

### 📦 Étape 8.2: Packaging

- [ ] Finaliser la configuration Poetry
- [ ] Construire le package: `poetry build`
- [ ] Tester l'installation en environnement propre
- [ ] Documenter les instructions d'installation

### 🚀 Étape 8.3: Déploiement

- [ ] Déployer Streamlit (Streamlit Cloud, Heroku, etc.)
- [ ] Configurer les variables d'environnement
- [ ] Mettre en place la surveillance (logs, métriques)
- [ ] Documentation de déploiement

---

## 🔄 BONNES PRATIQUES TOUT AU LONG DU PROJET

### 💾 Gestion de Version

- [ ] Commits fréquents avec messages descriptifs
- [ ] Branches pour les features importantes
- [ ] Tags pour les versions importantes
- [ ] Synchronisation régulière avec le remote

### 📝 Documentation Continue

- [ ] Commenter le code complexe
- [ ] Maintenir un journal de bord
- [ ] Documenter les décisions importantes
- [ ] Mettre à jour le README régulièrement

### 🔍 Monitoring de la Qualité

- [ ] Lancer les tests régulièrement: `poetry run pytest`
- [ ] Vérifier le formatage: `poetry run black .`
- [ ] Contrôler la qualité: `poetry run flake8`
- [ ] Surveiller les métriques CI/CD

### 🤝 Collaboration

- [ ] Code reviews avant merge
- [ ] Issues GitHub pour tracker les tâches
- [ ] Documentation des APIs pour les collaborateurs
- [ ] Partage des insights et découvertes

---

## 🎯 MÉTRIQUES DE SUCCÈS D'UN PROJET EDA

### 📊 Métriques Techniques

- [ ] **Couverture de code** > 80%
- [ ] **Temps d'exécution** du pipeline < X minutes
- [ ] **Qualité des données** après nettoyage
- [ ] **Performance des modèles** selon les métriques choisies

### 🎨 Métriques de Présentation

- [ ] **Nombre de visualisations** pertinentes créées
- [ ] **Interface Streamlit** fonctionnelle et intuitive
- [ ] **Rapport final** complet et actionnable
- [ ] **Documentation** claire et utilisable

### 🚀 Métriques Business

- [ ] **Insights actionnables** identifiés
- [ ] **Recommandations** concrètes formulées
- [ ] **Hypothèses** validées ou invalidées
- [ ] **Valeur ajoutée** démontrée pour l'organisation

---

## 🛠️ OUTILS ET COMMANDES ESSENTIELS

### Poetry

```bash
poetry install          # Installation des dépendances
poetry add <package>     # Ajouter une dépendance
poetry shell            # Activer l'environnement virtuel
poetry run <command>     # Exécuter une commande
```

### Tests et Qualité

```bash
poetry run pytest       # Lancer les tests
poetry run black .      # Formater le code
poetry run flake8       # Vérifier la qualité
poetry run mypy src     # Type checking
```

### Git

```bash
git add .               # Ajouter les changements
git commit -m "msg"     # Commiter
git push                # Pousser vers remote
git pull                # Récupérer les changements
```

### Streamlit

```bash
poetry run streamlit run streamlit_app/app.py
```

---

Ce guide vous donne une roadmap complète pour mener un projet EDA de A à Z avec une structure professionnelle moderne ! 🚀
