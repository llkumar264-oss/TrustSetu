import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DATA_PATH = "data/scam_samples.csv"
MODEL_PATH = "scam_model.joblib"

def train():
    df = pd.read_csv(DATA_PATH)

    # ? Clean bad rows (missing text/label)
    df = df.dropna(subset=["text", "label"])
    df["text"] = df["text"].astype(str).fillna("").str.strip()

    # ? Convert label safely
    df["label"] = pd.to_numeric(df["label"], errors="coerce")
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    # ? Remove empty text rows
    df = df[df["text"] != ""]

    X = df["text"]
    y = df["label"]

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("clf", LogisticRegression(max_iter=1500))
    ])

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

    print("? Model trained successfully!")
    print("? Saved as:", MODEL_PATH)
    print("? Rows used:", len(df))

if __name__ == "__main__":
    train()
