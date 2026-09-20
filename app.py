
import streamlit as st
import pickle
import requests
import gzip

with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception:
        return None

    return None


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []
    ids = []

    for i in distances[1:6]:
        movie_index = i[0]
        movie_id = movies.iloc[movie_index]["movie_id"]
        movie_name = movies.iloc[movie_index]["title"]

        names.append(movie_name)
        posters.append(fetch_poster(movie_id))
        ids.append(movie_id)

    return names, posters, ids


st.set_page_config(
    page_title="Movie Recommendation System MADE BY ANISH",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System MADE BY ANISH")
st.write("Find movies similar to your favourite movie.")

selected_movie = st.selectbox(
    "🎥 Type or select a movie",
    movies["title"].values
)

if st.button("🚀 Show Recommendation"):

    names, posters, ids = recommend(selected_movie)

    st.subheader("✨ Recommended Movies")

    cols = st.columns(5)

    for col, name, poster, movie_id in zip(
        cols, names, posters, ids
    ):
        with col:
            st.markdown(f"**{name}**")

            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.info("Poster not available")

            st.caption(f"Movie ID: {movie_id}")
