import plotly.graph_objects as go
import streamlit as st

from recommender import Recommender

RADAR_FEATURES = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence",
]

st.set_page_config(page_title="Music Recommender", page_icon="🎧")
st.title("🎧 Music Recommender")
st.caption("Pick a song, get tracks with a similar sound.")


@st.cache_resource
def load_recommender():
    return Recommender()

COLORS = [
    ("#1DB954", "rgba(29, 185, 84, 0.35)"),   # green: the song you picked
    ("#E63946", "rgba(230, 57, 70, 0.35)"),   # red: the recommendation
]



def radar_chart(song_a, song_b):
    categories = RADAR_FEATURES + [RADAR_FEATURES[0]]
    fig = go.Figure()
    for song, (line_color, fill_color) in zip((song_a, song_b), COLORS):
        values = [song[f] for f in RADAR_FEATURES]
        values.append(values[0])
        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                name=f"{song['track_name']} - {song['artists']}",
                line=dict(color=line_color),
                fillcolor=fill_color,
            )
        )
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 1])),
        legend=dict(orientation="h", y=-0.15),
        height=480,
    )
    return fig


rec = load_recommender()
genres = ["Any genre"] + sorted(rec.df["track_genre"].unique())

query = st.text_input("Search for a song", placeholder="e.g. Blinding Lights")

if query:
    matches = rec.search(query)

    if matches.empty:
        st.warning("No songs found. Try another name.")
    else:
        options = {
            f"{row.track_name} - {row.artists} (popularity {row.popularity})": i
            for i, row in matches.iterrows()
        }
        choice = st.selectbox("Pick the exact track", list(options.keys()))

        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox("Genre filter", genres)
        with col2:
            n = st.slider("How many results?", 5, 20, 10)

        if st.button("Recommend"):
            genre_filter = None if genre == "Any genre" else genre
            source_idx = options[choice]
            st.session_state["source_idx"] = source_idx
            st.session_state["result"] = rec.recommend(source_idx, n=n, genre=genre_filter)

if "result" in st.session_state:
    result = st.session_state["result"]
    source_idx = st.session_state["source_idx"]

    st.subheader("You might also like")
    st.dataframe(result, hide_index=True)
    st.caption("Distance: smaller means a closer sound.")

    st.subheader("Compare the sound")
    compare_options = {
        f"{row.track_name} - {row.artists}": i for i, row in result.iterrows()
    }
    compare_choice = st.selectbox("Compare with", list(compare_options.keys()))

    song_a = rec.df.loc[source_idx]
    song_b = rec.df.loc[compare_options[compare_choice]]
    st.plotly_chart(radar_chart(song_a, song_b))