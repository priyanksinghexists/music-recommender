import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances

FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence", "tempo",
]


class Recommender:
    def __init__(self, path="data/spotify.csv"):
        df = pd.read_csv(path)
        df = df.drop(columns=["Unnamed: 0"], errors="ignore")
        df = df.dropna(subset=["track_name", "artists"])
        df = df.drop_duplicates(subset=["track_name", "artists"])
        self.df = df.reset_index(drop=True)
        self.scaled = StandardScaler().fit_transform(self.df[FEATURES])

    def search(self, query, limit=10):
        mask = self.df["track_name"].str.contains(
            query, case=False, na=False, regex=False
        )
        return self.df[mask].sort_values("popularity", ascending=False).head(limit)

    def recommend(self, idx, n=10, genre=None):
        dists = euclidean_distances(self.scaled[idx].reshape(1, -1), self.scaled)[0]

        order = dists.argsort()
        order = order[order != idx]

        if genre:
            order = order[self.df["track_genre"].values[order] == genre]

        top = order[:n]
        result = self.df.iloc[top][["track_name", "artists", "track_genre"]].copy()
        result["distance"] = dists[top].round(2)
        return result