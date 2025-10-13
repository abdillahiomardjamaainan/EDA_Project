import pandas as pd

def add_recipe_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les variables dérivées à la table recipes."""
    df = df.copy()

    # Longueur de la description (en mots)
    df["description_length"] = df["description_filled"].fillna("").apply(lambda x: len(str(x).split()))
    return df