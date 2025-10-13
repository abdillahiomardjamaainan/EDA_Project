# src/preprocessing.py
"""
Préprocessing (CONVERSIONS UNIQUEMENT) pour EDA recettes.

Objectifs (stricts) :
- Convertir proprement les colonnes list-like (tags, ingredients, steps, nutrition).
- Découper la colonne 'nutrition' en 7 colonnes dédiées.
- Convertir les colonnes temporelles (submitted -> datetime + parties utiles).
- Caster contributor_id en catégoriel.
- Fournir un pipeline "convert_recipes_for_univariate" idempotent.

Exclusions :
- Pas d'imputation, pas de filtrage d'outliers, pas de feature engineering métier.
- Pas de modification de 'description' (sauf helper optionnel génératif si manquant).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Sequence, Tuple, List

import ast
import pandas as pd


# ---------------------------------------------------------------------
# Constantes & schémas
# ---------------------------------------------------------------------

#: Ordre conventionnel des 7 valeurs présentes dans la colonne 'nutrition'
NUTRITION_COLS: Tuple[str, ...] = (
    "calories",
    "total_fat",
    "sugar",
    "sodium",
    "protein",
    "saturated_fat",
    "carbohydrates",
)

#: Colonnes list-like attendues dans recipes
DEFAULT_LIST_LIKE_COLS: Tuple[str, ...] = ("tags", "ingredients", "steps", "nutrition")


# ---------------------------------------------------------------------
# Helpers internes (purs, idempotents)
# ---------------------------------------------------------------------

def _safe_literal_eval(x: Any) -> Any:
    """
    Convertit une chaîne représentant une structure Python (liste/dict)
    en objet Python. Si la conversion échoue, renvoie la valeur d'origine.
    - Idempotent : si x est déjà list/dict -> renvoie x.
    - Ne modifie pas NaN/None.
    """
    if isinstance(x, (list, dict)) or pd.isna(x):
        return x
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except (ValueError, SyntaxError):
            return x
    return x


def _ensure_list_or_none(x: Any) -> Optional[list]:
    """
    Force la sortie à être une liste Python ou None.
    - str convertible -> list
    - list -> list
    - NaN/None -> None
    - sinon -> None (on ne force pas des types improbables)
    """
    if pd.isna(x):
        return None
    if isinstance(x, list):
        return x
    parsed = _safe_literal_eval(x)
    return parsed if isinstance(parsed, list) else None


def _copy(df: pd.DataFrame) -> pd.DataFrame:
    """Raccourci lisible pour travailler en pure function."""
    return df.copy()


def _pad_or_none(lst: Optional[List[Any]], n: int) -> List[Optional[Any]]:
    """
    Prend une liste (ou None) et renvoie une liste de longueur n :
    - si lst est None ou pas une liste -> [None]*n
    - si len(lst) == n -> lst
    - si len(lst) < n -> lst + [None]*(n-len(lst))
    - si len(lst) > n -> lst[:n]
    """
    if not isinstance(lst, list):
        return [None] * n
    if len(lst) == n:
        return lst
    if len(lst) < n:
        return lst + [None] * (n - len(lst))
    return lst[:n]


# ---------------------------------------------------------------------
# Conversions unitaires
# ---------------------------------------------------------------------

def convert_list_like_columns(
    df: pd.DataFrame,
    list_like_cols: Iterable[str] = DEFAULT_LIST_LIKE_COLS,
) -> pd.DataFrame:
    """
    Convertit les colonnes list-like (stockées en str) en vraies listes Python.
    - Aucune imputation ni correction sémantique.
    - Les valeurs non convertibles deviennent None.
    """
    df = _copy(df)
    for col in list_like_cols:
        if col in df.columns:
            df[col] = df[col].apply(_ensure_list_or_none)
    return df


def split_nutrition_columns(
    df: pd.DataFrame,
    nutrition_col: str = "nutrition",
    output_cols: Sequence[str] = NUTRITION_COLS,
    drop_original: bool = False,
) -> pd.DataFrame:
    """
    Découpe 'nutrition' (list[float] de longueur 7) en 7 colonnes nommées.

    - Si la ligne ne contient pas une liste -> NaN dans les colonnes créées.
    - Si la liste n'est pas de longueur 7 -> pad/truncate à 7 avec None.
    - drop_original=True supprime la colonne 'nutrition' d'origine.

    Raises
    ------
    ValueError si une des colonnes cibles existe déjà pour éviter l'écrasement.
    """
    df = _copy(df)
    if nutrition_col not in df.columns:
        return df

    # Sécurité : convertir au bon format list/None AVANT de splitter
    lists = df[nutrition_col].apply(_ensure_list_or_none)
    padded = lists.apply(lambda x: _pad_or_none(x, len(output_cols)))
    nutri_df = pd.DataFrame(padded.to_list(), columns=list(output_cols), index=df.index)

    # Vérifier collisions de noms
    dupes = [c for c in output_cols if c in df.columns]
    if dupes:
        raise ValueError(
            f"Colonnes déjà présentes dans le DataFrame : {dupes}. "
            "Renomme-les/supprime-les avant split_nutrition_columns()."
        )

    out = pd.concat([df, nutri_df], axis=1)
    if drop_original and nutrition_col in out.columns:
        out = out.drop(columns=[nutrition_col])
    return out


def convert_temporal_columns(
    df: pd.DataFrame,
    submitted_col: str = "submitted",
    add_parts: bool = True,
    parts: Sequence[str] = ("year", "month"),
) -> pd.DataFrame:
    """
    Convertit 'submitted' en datetime (errors='coerce').
    Optionnel : ajoute des parties temporelles ('year', 'month', 'day', 'dayofweek', ...).
    """
    df = _copy(df)
    if submitted_col in df.columns:
        df[submitted_col] = pd.to_datetime(df[submitted_col], errors="coerce")
        if add_parts:
            if "year" in parts:
                df["year"] = df[submitted_col].dt.year
            if "month" in parts:
                df["month"] = df[submitted_col].dt.month
            if "day" in parts:
                df["day"] = df[submitted_col].dt.day
            if "dayofweek" in parts:
                df["dayofweek"] = df[submitted_col].dt.dayofweek
    return df


def convert_contributor_to_category(
    df: pd.DataFrame,
    contributor_col: str = "contributor_id",
) -> pd.DataFrame:
    """
    Convertit l'identifiant contributeur en catégoriel pour éviter des stats numériques absurdes.
    """
    df = _copy(df)
    if contributor_col in df.columns:
        df[contributor_col] = df[contributor_col].astype("category")
    return df


# ---------------------------------------------------------------------
# Pipeline de conversion (recettes, univariée)
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RecipeConversionConfig:
    """Configuration déclarative du pipeline de conversion."""
    list_like_cols: Tuple[str, ...] = DEFAULT_LIST_LIKE_COLS
    nutrition_col: str = "nutrition"
    temporal_col: str = "submitted"
    add_temporal_parts: bool = True
    temporal_parts: Tuple[str, ...] = ("year", "month")
    contributor_col: str = "contributor_id"
    drop_original_nutrition: bool = False


def convert_recipes_for_univariate(
    df_recipes: pd.DataFrame,
    config: RecipeConversionConfig | None = None,
) -> pd.DataFrame:
    """
    Pipeline minimal des CONVERSIONS techniques pour la table 'recipes'.

    Inclus :
      - list-like -> listes (tags, ingredients, steps, nutrition)
      - découpe des 7 colonnes nutritionnelles (ajoutées à droite)
      - submitted -> datetime (+ colonnes temporelles choisies)
      - contributor_id -> category

    Exclus :
      - Pas d'imputation, pas de filtrage d'outliers, pas de features dérivées métier.
      - 'description' non modifiée (traitée à part selon ton process).
    """
    cfg = config or RecipeConversionConfig()

    df = _copy(df_recipes)
    # 1) Colonnes list-like en vraies listes
    df = convert_list_like_columns(df, list_like_cols=cfg.list_like_cols)
    # 2) Nutrition -> colonnes dédiées
    if cfg.nutrition_col in df.columns:
        df = split_nutrition_columns(
            df,
            nutrition_col=cfg.nutrition_col,
            output_cols=NUTRITION_COLS,
            drop_original=cfg.drop_original_nutrition,
        )
    # 3) Temps -> datetime (+ parts)
    df = convert_temporal_columns(
        df,
        submitted_col=cfg.temporal_col,
        add_parts=cfg.add_temporal_parts,
        parts=cfg.temporal_parts,
    )
    # 4) Contributor -> category
    df = convert_contributor_to_category(df, contributor_col=cfg.contributor_col)

    return df


# ---------------------------------------------------------------------
# Helper optionnel : description auto (utilisée seulement si manquante)
# ---------------------------------------------------------------------

def generate_auto_description(row: pd.Series) -> str:
    """
    Génère une description "simple" d'une recette à partir de ses caractéristiques.
    Utilisée uniquement quand la description d'origine est manquante.

    Notes :
    - Purement indicative (anglais simple), ne remplace pas un vrai texte marketing.
    - N'altère aucune autre colonne, à appeler via df.apply(generate_auto_description, axis=1).
    """
    # 1) Si la description existe déjà, on la garde telle quelle
    desc = row.get("description", None)
    if isinstance(desc, str) and desc.strip():
        return desc

    # 2) Extraire les champs utiles (sans imputer)
    time = row.get("minutes", None)
    n_ing = row.get("n_ingredients", None)
    n_steps = row.get("n_steps", None)
    tags = row.get("tags", None)

    # 3) Catégorie "naïve" depuis le 1er tag si possible
    category = None
    if isinstance(tags, list) and len(tags) > 0 and isinstance(tags[0], str):
        category = tags[0].replace("-", " ").strip() or None

    # 4) Construire la phrase
    parts = ["This is a"]
    if category:
        parts.append(category)
    parts.append("recipe")

    # Temps
    if pd.notna(time):
        try:
            t = float(time)
            if t < 30:
                parts.append("that is quick to prepare")
            elif t < 90:
                parts.append("of moderate duration")
            else:
                parts.append("that takes longer to cook")
        except Exception:
            pass  # si non convertible, on ignore

    # Complexité
    if pd.notna(n_steps) and pd.notna(n_ing):
        try:
            s = float(n_steps)
            i = float(n_ing)
            if s <= 5 and i <= 5:
                parts.append("and very simple to make")
            elif s > 10 or i > 10:
                parts.append("and rather elaborate")
            else:
                parts.append("with average complexity")
        except Exception:
            pass

    sentence = " ".join(parts).strip().capitalize()
    return (sentence + ".") if not sentence.endswith(".") else sentence

# (← ligne vide à la fin du fichier)

