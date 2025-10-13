# 📊 Description des Données - Projet EDA

## 🎯 Vue d'Ensemble

Ce document décrit en détail les datasets utilisés dans notre projet d'Analyse Exploratoire de Données (EDA).

## 🍴 Dataset des Recettes (RAW_recipes.csv)

### Métadonnées

- **Nombre de lignes** : 231,637 recettes
- **Nombre de colonnes** : 12 variables
- **Taille approximative** : ~281 MB
- **Format** : CSV avec en-têtes

### Description des Variables

| Variable         | Type                       | Description                                 | Exemple                                                         |
| ---------------- | -------------------------- | ------------------------------------------- | --------------------------------------------------------------- |
| `name`           | Nominal (string)           | Nom de la recette                           | "Classic Chocolate Chip Cookies"                                |
| `id`             | Nominal (int)              | Identifiant unique de la recette            | 275022                                                          |
| `minutes`        | Quantitatif discret (int)  | Temps de préparation en minutes             | 45                                                              |
| `contributor_id` | Nominal (int)              | ID de l'utilisateur qui a ajouté la recette | 28540                                                           |
| `submitted`      | Temporel (date)            | Date de soumission                          | "2008-11-19"                                                    |
| `tags`           | Nominal (list)             | Liste de tags descriptifs                   | "['desserts', 'cookies', 'chocolate']"                          |
| `nutrition`      | Quantitatif continu (list) | Valeurs nutritionnelles                     | "[calories, fat, sugar, sodium, protein, saturated fat, carbs]" |
| `n_steps`        | Quantitatif discret (int)  | Nombre d'étapes de préparation              | 8                                                               |
| `steps`          | Nominal (list)             | Description détaillée des étapes            | "['Preheat oven', 'Mix ingredients', ...]"                      |
| `description`    | Nominal (string)           | Description courte de la recette            | "These are the best cookies ever!"                              |
| `ingredients`    | Nominal (list)             | Liste des ingrédients                       | "['flour', 'sugar', 'butter', 'eggs']"                          |
| `n_ingredients`  | Quantitatif discret (int)  | Nombre d'ingrédients                        | 6                                                               |

### Contraintes et Règles Business

- Chaque recette doit avoir un `id` unique
- `minutes` doit être > 0
- `n_steps` et `n_ingredients` doivent correspondre aux longueurs des listes `steps` et `ingredients`
- Les dates `submitted` sont comprises entre 1999 et 2018

## ⭐ Dataset des Interactions (RAW_interactions.csv)

### Métadonnées

- **Nombre de lignes** : 1,132,367 interactions
- **Nombre de colonnes** : 5 variables
- **Taille approximative** : ~333 MB
- **Format** : CSV avec en-têtes

### Description des Variables

| Variable    | Type             | Description                         | Exemple                       |
| ----------- | ---------------- | ----------------------------------- | ----------------------------- |
| `user_id`   | Nominal (int)    | Identifiant unique de l'utilisateur | 38094                         |
| `recipe_id` | Nominal (int)    | Référence vers `recipes.id`         | 275022                        |
| `date`      | Temporel (date)  | Date de l'interaction               | "2008-12-01"                  |
| `rating`    | Ordinal (int)    | Note de 1 à 5 étoiles               | 4                             |
| `review`    | Nominal (string) | Commentaire textuel (optionnel)     | "Delicious and easy to make!" |

### Contraintes et Règles Business

- `user_id` et `recipe_id` forment la clé primaire (un utilisateur ne peut noter qu'une fois chaque recette)
- `rating` doit être entre 1 et 5 (inclus)
- `recipe_id` doit exister dans le dataset des recettes (intégrité référentielle)
- `review` peut être vide (null/NaN)

## 🔗 Relations Entre les Datasets

### Schéma Relationnel

```
RECIPES (1) ←→ (N) INTERACTIONS
   ↓                    ↓
recipes.id ←→ interactions.recipe_id
```

### Types de Jointures Possibles

- **INNER JOIN** : Seulement les recettes qui ont des interactions
- **LEFT JOIN** : Toutes les recettes + leurs interactions (si elles existent)
- **RIGHT JOIN** : Toutes les interactions + informations des recettes

### Métriques de Couverture

- Recettes avec au moins une interaction : ~74,000 (32%)
- Recettes sans interaction : ~157,000 (68%)
- Utilisateurs uniques : ~25,000
- Interactions par recette (moyenne) : ~15

## 📋 Qualité des Données Attendue

### Valeurs Manquantes Prévisibles

- `description` dans recipes : ~15% manquant
- `review` dans interactions : ~20% manquant
- `tags` : Très peu de valeurs manquantes

### Problèmes Potentiels

- Doublons possibles dans les noms de recettes
- Formats de dates variables
- Listes stockées en format string (parsing nécessaire)
- Outliers dans `minutes` (recettes très longues/courtes)

## 🎯 Objectifs d'Analyse

### Questions Business

1. Quelles sont les recettes les plus populaires ?
2. Quels facteurs influencent les notes des recettes ?
3. Y a-t-il des tendances temporelles dans les soumissions ?
4. Peut-on prédire la popularité d'une recette ?

### Analyses Techniques Prévues

- Analyse des distributions de variables
- Corrélations entre temps de préparation et notes
- Clustering de recettes par similarité
- Analyse de sentiment des commentaires
- Recommandation de recettes

---

_Document généré le : 12 octobre 2025_  
_Version : 1.0_  
_Auteur : Équipe EDA_
