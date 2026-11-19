# 🎧 Music Recommender

A content-based music recommendation app. Search for a song and get tracks
that sound similar, based on Spotify audio features.

**Live demo:** https://priyank-music-recommender-uzpzrtzmsxkvdajrf7juic.streamlit.app/

## How it works

1. Cleaned a dataset of ~114k Spotify tracks down to ~81k unique songs
2. Standardized 9 audio features (danceability, energy, loudness, tempo, etc.)
   so no single feature dominates
3. Represented each song as a point in 9-dimensional space and used
   **Euclidean distance** to find the closest songs
4. Built a Streamlit interface with search, a genre filter, and a radar chart
   comparing the audio profiles of two songs

## Tech stack

Python, pandas, scikit-learn, Streamlit, Plotly

## Run it locally

```
pip install -r requirements.txt
streamlit run app.py
```

## Notes

I first tried cosine similarity, but it ignored how extreme a song's features
are and gave weak matches, so I switched to Euclidean distance.
