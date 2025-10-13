# src/utils/descriptives.py
"""
Indicateurs descriptifs univariés et bivariés.
- Numérique ↔ Numérique
- Numérique ↔ Catégoriel
- Catégoriel ↔ Catégoriel
"""

from __future__ import annotations
from typing import Dict, Sequence, Optional
import numpy as np
import pandas as pd


# ---------- helpers ----------
def _ensure_col(df: pd.DataFrame, col: str) -> None:
    if col not in df.columns:
        raise KeyError(f"Colonne absente: {col}")

def _is_numeric(s: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(s)

def _is_categorical(s: pd.Series) -> bool:
    return pd.api.types.is_categorical_dtype(s) or pd.api.types.is_object_dtype(s) or pd.api.types.is_string_dtype(s)


# ---------- univarié ----------
def summarize_numeric(
    df: pd.DataFrame,
    column: str,
    percentiles: Sequence[float] = (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99),
) -> pd.DataFrame:
    """Résumé complet pour une variable quantitative."""
    _ensure_col(df, column)
    s = pd.to_numeric(df[column], errors="coerce").dropna()
    out = {
        "count": s.size,
        "missing": df[column].isna().sum(),
        "min": s.min() if not s.empty else np.nan,
        "q1": s.quantile(0.25) if not s.empty else np.nan,
        "median": s.median() if not s.empty else np.nan,
        "mean": s.mean() if not s.empty else np.nan,
        "q3": s.quantile(0.75) if not s.empty else np.nan,
        "max": s.max() if not s.empty else np.nan,
        "std": s.std(ddof=1) if s.size > 1 else np.nan,
        "skew": s.skew() if s.size > 2 else np.nan,
        "kurtosis": s.kurt() if s.size > 3 else np.nan,
        "unique": s.nunique(),
    }
    for p in percentiles:
        out[f"p{int(p*100):02d}"] = s.quantile(p) if not s.empty else np.nan
    return pd.DataFrame([out], index=[column])


def summarize_categorical(
    df: pd.DataFrame,
    column: str,
    top_k: int = 20,
    normalize: bool = True,
    dropna: bool = False,
) -> pd.DataFrame:
    """Résumé pour une variable qualitative : total, NA, uniques + top-k modalités."""
    _ensure_col(df, column)
    s = df[column]
    counts = s.value_counts(dropna=dropna)
    top = counts.head(top_k).rename("count").to_frame()
    if normalize and counts.sum() > 0:
        top["prop"] = (top["count"] / counts.sum()).round(4)
    header = pd.DataFrame({"total":[len(s)], "missing":[s.isna().sum()], "unique":[s.nunique(dropna=True)]}, index=["__summary__"])
    return pd.concat([header, top])


# ---------- bivarié ----------
def summarize_num_num(df: pd.DataFrame, x: str, y: str) -> pd.DataFrame:
    """Numérique↔Numérique : corrélations / covariance."""
    _ensure_col(df, x); _ensure_col(df, y)
    sx = pd.to_numeric(df[x], errors="coerce")
    sy = pd.to_numeric(df[y], errors="coerce")
    mask = sx.notna() & sy.notna()
    sx, sy = sx[mask], sy[mask]
    if sx.empty:
        return pd.DataFrame([{"n":0, "pearson":np.nan, "spearman":np.nan, "cov":np.nan}], index=[f"{x}~{y}"])
    return pd.DataFrame([{
        "n": len(sx),
        "pearson": sx.corr(sy, method="pearson"),
        "spearman": sx.corr(sy, method="spearman"),
        "cov": np.cov(sx, sy, ddof=1)[0,1]
    }], index=[f"{x}~{y}"])


def summarize_num_cat(
    df: pd.DataFrame, num_col: str, cat_col: str, top_k: int = 20
) -> pd.DataFrame:
    """Numérique↔Catégoriel : stats par catégorie (count, mean, median, std)."""
    _ensure_col(df, num_col); _ensure_col(df, cat_col)
    g = df[[num_col, cat_col]].copy()
    g[num_col] = pd.to_numeric(g[num_col], errors="coerce")
    g = g.dropna(subset=[num_col, cat_col])
    top_cats = g[cat_col].value_counts().head(top_k).index
    g = g[g[cat_col].isin(top_cats)]
    stats = g.groupby(cat_col)[num_col].agg(["count","mean","median","std"]).sort_values("count", ascending=False)
    return stats


def summarize_cat_cat(df: pd.DataFrame, a: str, b: str, top_k: int = 20, normalize: Optional[str] = None) -> pd.DataFrame:
    """Catégoriel↔Catégoriel : table de contingence (option : proportions par ligne/colonne)."""
    _ensure_col(df, a); _ensure_col(df, b)
    tmp = df[[a,b]].dropna()
    # limiter aux top modalités pour lisibilité
    a_top = tmp[a].value_counts().head(top_k).index
    b_top = tmp[b].value_counts().head(top_k).index
    tmp = tmp[tmp[a].isin(a_top) & tmp[b].isin(b_top)]
    ct = pd.crosstab(tmp[a], tmp[b], normalize=normalize)
    return ct.round(4) if normalize else ct


# --- Analyse de colonnes LISTE (tags, ingredients, steps) ---
from collections import Counter
import pandas as pd

def analyze_list_column(df: pd.DataFrame, col_name: str, top_k: int = 10) -> pd.DataFrame:
    """
    Compte les occurrences des éléments dans une colonne de listes (ex: 'ingredients', 'tags').
    Retourne un DataFrame: élément | fréquence (trié décroissant).
    suppose que df[col_name] contient déjà des listes Python (pas des str).
    """
    if col_name not in df.columns:
        raise KeyError(f"Colonne absente: {col_name}")
    all_items = [
        item
        for sub in df[col_name].dropna()
        if isinstance(sub, list)
        for item in sub
    ]
    counter = Counter(all_items)
    top = counter.most_common(top_k)
    out = pd.DataFrame(top, columns=["element", "frequency"])
    out.index = range(1, len(out) + 1)
    print(f"📊 '{col_name}': total={len(all_items):,} | uniques={len(counter):,}")
    return out

