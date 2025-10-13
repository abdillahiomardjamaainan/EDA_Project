# src/visualization.py
"""
Visualisations interactives pour EDA (recettes).
------------------------------------------------
Fonctions Plotly pour:
- Univarié: quantitatif, qualitatif
- Bivarié: quant-quant, quant-qual, qual-qual

Chaque fonction retourne une figure Plotly (fig).
Utilisation en notebook: fig.show()
Utilisation en Streamlit: st.plotly_chart(fig)
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def _ensure_cols(df: pd.DataFrame, cols: Iterable[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"Colonnes absentes: {missing}")

def _select_top_k_categories(
    df: pd.DataFrame, col: str, top_k: int
) -> pd.DataFrame:
    """
    Garde uniquement les top_k modalités les plus fréquentes (autres supprimées).
    """
    counts = df[col].value_counts(dropna=False)
    keep = counts.head(top_k).index
    return df[df[col].isin(keep)].copy()

def _numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    s = pd.to_numeric(df[col], errors="coerce")
    return s.dropna()


# ---------------------------------------------------------------------
# UNIVARIÉ — Quantitatif
# ---------------------------------------------------------------------
def plot_hist_interactive(
    df: pd.DataFrame,
    col: str,
    bins: int = 50,
    max_x: Optional[float] = None,
    log_x: bool = False,
    title: Optional[str] = None,
) -> go.Figure:
    """
    Histogramme interactif d'une variable quantitative.
    - max_x: tronque l'axe X pour limiter les extrêmes
    - log_x: échelle log sur X
    """
    _ensure_cols(df, [col])
    s = _numeric_series(df, col)
    if max_x is not None:
        s = s[s <= max_x]

    fig = px.histogram(
        s, x=s, nbins=bins,
        title=title or f"Distribution de {col}",
        labels={"x": col, "y": "Count"},
    )
    if log_x:
        fig.update_xaxes(type="log")
    fig.update_layout(template="plotly_white", bargap=0.05)
    return fig


def plot_box_interactive(
    df: pd.DataFrame,
    col: str,
    max_x: Optional[float] = None,
    showfliers: bool = True,
    title: Optional[str] = None,
) -> go.Figure:
    """
    Boxplot interactif d'une variable quantitative.
    - max_x: limite de l'axe X (utile pour couper les outliers visuellement)
    - showfliers: afficher/masquer les points extrêmes
    """
    _ensure_cols(df, [col])
    s = _numeric_series(df, col)
    fig = px.box(
        x=s, points="all" if showfliers else False,
        title=title or f"Boxplot de {col}",
        labels={"x": col},
    )
    if max_x is not None:
        fig.update_xaxes(range=[float(np.nanmin(s)), max_x])
    fig.update_layout(template="plotly_white")
    return fig


# ---------------------------------------------------------------------
# UNIVARIÉ — Qualitatif
# ---------------------------------------------------------------------
def plot_bar_categorical(
    df: pd.DataFrame,
    col: str,
    top_k: int = 20,
    normalize: bool = True,
    title: Optional[str] = None,
    rotate: int = 0,
) -> go.Figure:
    """
    Bar chart interactif des modalités les plus fréquentes d'une variable catégorielle.
    - top_k: nombre de modalités affichées
    - normalize: True -> proportions, False -> effectifs
    - rotate: angle des labels en X
    """
    _ensure_cols(df, [col])
    counts = df[col].value_counts(dropna=False).head(top_k)
    y_vals = counts / counts.sum() if normalize and counts.sum() > 0 else counts
    y_title = "Proportion" if normalize else "Effectif"

    fig = px.bar(
        x=counts.index.astype(str),
        y=y_vals.values,
        title=title or f"Top-{top_k} modalités de {col}",
        labels={"x": col, "y": y_title},
    )
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(tickangle=rotate)
    return fig


def plot_pie_categorical(
    df: pd.DataFrame,
    col: str,
    top_k: int = 10,
    title: Optional[str] = None,
) -> go.Figure:
    """
    Pie chart interactif (top-k) d'une variable catégorielle.
    Attention: privilégier bar chart pour comparer finement.
    """
    _ensure_cols(df, [col])
    counts = df[col].value_counts(dropna=False).head(top_k)
    fig = px.pie(
        names=counts.index.astype(str),
        values=counts.values,
        title=title or f"Répartition (Top-{top_k}) de {col}",
    )
    fig.update_layout(template="plotly_white")
    return fig


# ---------------------------------------------------------------------
# BIVARIÉ — Quantitatif ↔ Quantitatif
# ---------------------------------------------------------------------
def plot_scatter_num_num(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    sample: Optional[int] = 5000,
    trendline: Optional[str] = "lowess",  # "ols" | "lowess" | None
    title: Optional[str] = None,
    opacity: float = 0.5,
) -> go.Figure:
    """
    Scatter interactif entre deux variables quantitatives.
    - color: variable optionnelle pour colorer les points (ex. rating_class)
    - sample: sous-échantillonnage aléatoire si dataset très grand
    - trendline: 'ols' (linéaire) ou 'lowess' (lissage local), None pour désactiver
    """
    _ensure_cols(df, [x, y] + ([color] if color else []))
    d = df[[x, y] + ([color] if color else [])].copy()
    d[x] = pd.to_numeric(d[x], errors="coerce")
    d[y] = pd.to_numeric(d[y], errors="coerce")
    d = d.dropna(subset=[x, y])

    if sample and len(d) > sample:
        d = d.sample(sample, random_state=42)

    fig = px.scatter(
        d, x=x, y=y, color=color, opacity=opacity,
        title=title or f"{y} ~ {x}",
        trendline=trendline,
        labels={x: x, y: y},
    )
    fig.update_traces(marker=dict(size=6, line=dict(width=0)))
    fig.update_layout(template="plotly_white")
    return fig


# ---------------------------------------------------------------------
# BIVARIÉ — Quantitatif ↔ Qualitatif
# ---------------------------------------------------------------------
def plot_box_num_by_cat(
    df: pd.DataFrame,
    num_col: str,
    cat_col: str,
    top_k: int = 20,
    showfliers: bool = False,
    title: Optional[str] = None,
    rotate: int = 45,
) -> go.Figure:
    """
    Boxplots du numérique par catégories (limité aux top_k modalités).
    - showfliers=False: plus lisible quand les catégories sont nombreuses
    """
    _ensure_cols(df, [num_col, cat_col])
    d = df[[num_col, cat_col]].copy()
    d[num_col] = pd.to_numeric(d[num_col], errors="coerce")
    d = d.dropna(subset=[num_col, cat_col])
    d = _select_top_k_categories(d, cat_col, top_k)

    fig = px.box(
        d, x=cat_col, y=num_col, points="outliers" if showfliers else False,
        title=title or f"{num_col} par {cat_col} (Top-{top_k})",
        labels={cat_col: cat_col, num_col: num_col},
    )
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(tickangle=rotate)
    return fig


def plot_violin_num_by_cat(
    df: pd.DataFrame,
    num_col: str,
    cat_col: str,
    top_k: int = 20,
    title: Optional[str] = None,
    rotate: int = 45,
    box: bool = True,
) -> go.Figure:
    """
    Violin plots du numérique par catégories (Top-k).
    - box=True: superpose un boxplot à l'intérieur du violon.
    """
    _ensure_cols(df, [num_col, cat_col])
    d = df[[num_col, cat_col]].copy()
    d[num_col] = pd.to_numeric(d[num_col], errors="coerce")
    d = d.dropna(subset=[num_col, cat_col])
    d = _select_top_k_categories(d, cat_col, top_k)

    fig = px.violin(
        d, x=cat_col, y=num_col, box=box, points=False,
        title=title or f"{num_col} par {cat_col} (Top-{top_k})",
        labels={cat_col: cat_col, num_col: num_col},
    )
    fig.update_layout(template="plotly_white")
    fig.update_xaxes(tickangle=rotate)
    return fig


# ---------------------------------------------------------------------
# BIVARIÉ — Qualitatif ↔ Qualitatif
# ---------------------------------------------------------------------
def plot_heatmap_cat_cat(
    df: pd.DataFrame,
    a: str,
    b: str,
    top_k_a: int = 20,
    top_k_b: int = 20,
    normalize: Optional[str] = "index",  # "all" | "index" | "columns" | None
    title: Optional[str] = None,
) -> go.Figure:
    """
    Heatmap des fréquences (ou proportions) entre deux variables catégorielles.
    - normalize:
        None      -> effectifs
        "all"     -> proportions globales
        "index"   -> proportions par ligne
        "columns" -> proportions par colonne
    """
    _ensure_cols(df, [a, b])
    d = df[[a, b]].dropna().copy()
    # limiter aux top modalités
    a_top = d[a].value_counts().head(top_k_a).index
    b_top = d[b].value_counts().head(top_k_b).index
    d = d[d[a].isin(a_top) & d[b].isin(b_top)]

    ct = pd.crosstab(d[a], d[b], normalize=normalize)
    z = ct.values
    fig = go.Figure(
        data=go.Heatmap(
            z=z, x=ct.columns.astype(str), y=ct.index.astype(str),
            coloraxis="coloraxis"
        )
    )
    fig.update_layout(
        title=title or f"Contingence {a} × {b}",
        xaxis_title=b,
        yaxis_title=a,
        coloraxis_colorscale="Blues",
        template="plotly_white",
    )
    return fig
