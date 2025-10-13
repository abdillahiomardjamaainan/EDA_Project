"""
src/data_loader.py
Module de CHARGEMENT centralisé (EDA).

Objectifs :
- Centraliser toutes les lectures de données brutes.
- Ne PAS transformer les types ici (ni imputation, ni parsing complexe).
- Offrir une validation basique et des logs clairs.
- Rester indépendant du répertoire courant (fonctionne depuis notebooks/).

"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Sequence

import os
import pandas as pd


# ---------------------------------------------------------------------
# Chemins : racine projet et dossiers data
# ---------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_RAW_PATH: Path = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_PATH: Path = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------------------
# Helpers internes
# ---------------------------------------------------------------------

def _ensure_exists(path: Path) -> None:
    """Lève une erreur explicite si le fichier demandé n'existe pas."""
    if not path.exists():
        available = ", ".join(p.name for p in DATA_RAW_PATH.glob("*")) if DATA_RAW_PATH.exists() else "n/a"
        raise FileNotFoundError(
            f"Fichier non trouvé : {path}\n"
            f"Dossier RAW : {DATA_RAW_PATH}\n"
            f"Fichiers disponibles : {available}"
        )


def _read_csv_no_cast(path: Path, **read_csv_kwargs) -> pd.DataFrame:
    """
    Lecture CSV SANS forcer les types.
    - Tente d'abord utf-8, puis latin-1 si besoin.
    - Laisse pandas inférer dtypes (on transformera plus tard en preprocessing).
    """
    try:
        df = pd.read_csv(path, **read_csv_kwargs)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1", **read_csv_kwargs)
    return df


def _log_loaded(name: str, df: pd.DataFrame) -> None:
    """Affiche un petit résumé lisible du chargement."""
    print(f" {name} chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")


# ---------------------------------------------------------------------
# API publique : fonctions de chargement spécialisées
# ---------------------------------------------------------------------

def load_recipes(file_name: str = "RAW_recipes.csv", **read_csv_kwargs) -> pd.DataFrame:
    """
    Charge le dataset des recettes depuis data/raw/.
    Ne modifie PAS les types : objectif = lecture simple et fiable.
    """
    file_path = DATA_RAW_PATH / file_name
    _ensure_exists(file_path)
    df = _read_csv_no_cast(file_path, **read_csv_kwargs)
    _log_loaded(file_name, df)
    return df


def load_interactions(file_name: str = "RAW_interactions.csv", **read_csv_kwargs) -> pd.DataFrame:
    """
    Charge le dataset des interactions (notes/commentaires) depuis data/raw/.
    Ne modifie PAS les types.
    """
    file_path = DATA_RAW_PATH / file_name
    _ensure_exists(file_path)
    df = _read_csv_no_cast(file_path, **read_csv_kwargs)
    _log_loaded(file_name, df)
    return df


# ---------------------------------------------------------------------
# Validation basique (structure + non-vide)
# ---------------------------------------------------------------------

def validate_dataframe(df: pd.DataFrame, expected_columns: Sequence[str]) -> bool:
    """
    Vérifie une structure minimale :
      - DataFrame non vide
      - Colonnes attendues présentes
    Retourne True si OK ; sinon lève une ValueError explicite.
    """
    if df.empty:
        raise ValueError("Le DataFrame est vide après chargement.")

    missing = [c for c in expected_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}.\nColonnes présentes : {list(df.columns)}")

    return True


# ---------------------------------------------------------------------
# Sanity check et utilitaires
# ---------------------------------------------------------------------

def sanity_check() -> None:
    """
    Vérifie que le dossier RAW est accessible et liste son contenu.
    À lancer en premier dans un notebook.
    """
    print(f"ROOT: {PROJECT_ROOT}")
    print(f"RAW : {DATA_RAW_PATH}  exists: {DATA_RAW_PATH.exists()}")
    print("CONTENU RAW:")
    if DATA_RAW_PATH.exists():
        for p in sorted(DATA_RAW_PATH.glob("*")):
            print("  •", p.name)
    print()


def save_parquet(df: pd.DataFrame, name: str) -> Path:
    """
    Sauvegarde un DataFrame en Parquet dans data/processed/.
    (Aucune transformation ici, simple I/O.)
    """
    DATA_PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    out = DATA_PROCESSED_PATH / name
    df.to_parquet(out, index=False)
    print(f"💾 Sauvegardé : {out.relative_to(PROJECT_ROOT)}  shape={df.shape}")
    return out


def load_parquet(name: str, **read_parquet_kwargs) -> pd.DataFrame:
    """
    Charge un fichier Parquet depuis data/processed/.
    - Gère automatiquement les chemins relatifs.
    - Lève une erreur si le fichier n'existe pas.
    - Affiche la taille du DataFrame chargé.

    Exemple :
        df = load_parquet("recipes_enriched.parquet")
    """
    DATA_PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    file_path = DATA_PROCESSED_PATH / name

    # Vérification d’existence
    if not file_path.exists():
        available = ", ".join(p.name for p in DATA_PROCESSED_PATH.glob("*.parquet")) or "aucun"
        raise FileNotFoundError(
            f"❌ Fichier introuvable : {file_path}\n"
            f"Fichiers disponibles dans processed/ : {available}"
        )

    # Lecture
    df = pd.read_parquet(file_path, **read_parquet_kwargs)
    print(f"✅ {file_path.name} chargé ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
    return df

# --- Normalisation post-lecture pour colonnes liste ---
import ast
import numpy as np
import pandas as pd
from typing import Iterable

def _to_list_or_none(x):
    """Convertit str/ndarray -> list ; garde list ; NaN/None -> None ; sinon -> None."""
    if x is None:
        return None
    if isinstance(x, list):
        return x
    if isinstance(x, np.ndarray):
        return list(x)
    # gérer NaN après ndarray
    try:
        if pd.isna(x):
            return None
    except Exception:
        pass
    if isinstance(x, str):
        try:
            v = ast.literal_eval(x)
            return v if isinstance(v, list) else None
        except (ValueError, SyntaxError):
            return None
    return None


def _normalize_list_columns(df: pd.DataFrame, list_cols: Iterable[str]) -> pd.DataFrame:
    """Force les colonnes spécifiées à être des listes Python ou None (idempotent)."""
    out = df.copy()
    for c in list_cols:
        if c in out.columns:
            out[c] = out[c].apply(_to_list_or_none)
    return out

def load_parquet_safe(name: str, list_cols: Iterable[str] = ("tags","ingredients","steps"), **kwargs) -> pd.DataFrame:
    """
    Charge un .parquet depuis data/processed/ puis normalise les colonnes liste.
    N’exige AUCUNE modif de preprocessing.
    """
    df = load_parquet(name, **kwargs)  # ta fonction existante
    df = _normalize_list_columns(df, list_cols)
    print(f"✅ {name} chargé & normalisé (colonnes liste: {list(list_cols)})")
    return df
