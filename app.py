import streamlit as st
import pickle
import requests
import gzip
import os

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOVIES_FILE = os.path.join(BASE_DIR, "movies.pkl")
SIMILARITY_FILE = os.path.join(BASE_DIR, "similarity.pkl.gz")

# -----------------------------
# Load movies
# -----------------------------
with open(MOVIES_FILE, "rb") as f:
    movies = pickle.load(f)

# -----------------------------
# Load similarity
# -----------------------------
with gzip.open(SIMILARITY_FILE, "rb") as f:
    similarity_data = pickle.load(f)

similarity_indices = similarity_data["indices"]

# -----------------------------
# TMDB API
# -----------------------------
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

    except Exception:
        return None

    return None


def recommend(movie):

    index = movies[
        movies["title"] == movie
    ].index[0]

    names = []
    posters = []
    ids = []

    for movie_index in similarity_indices[index][0:10]:

        movie_index = int(movie_index)

        movie_id = movies.iloc[
            movie_index
        ]["movie_id"]

        movie_name = movies.iloc[
            movie_index
        ]["title"]

        names.append(movie_name)

        posters.append(
            fetch_poster(movie_id)
        )

        ids.append(movie_id)

    return names, posters, ids


# -----------------------------
# App UI
# -----------------------------

st.title("🎬 Movie Recommendation System")

st.write(
    "Find movies similar to your favourite movie."
)

selected_movie = st.selectbox(
    "🎥 Select a movie",
    movies["title"].values
)

if st.button("🚀 Show Recommendation"):

    names, posters, ids = recommend(
        selected_movie
    )

    st.subheader(
        "✨ Recommended Movies"
    )

    cols = st.columns(5)

    for col, name, poster, movie_id in zip(
        cols,
        names,
        posters,
        ids
    ):

        with col:

            st.markdown(
                f"**{name}**"
            )

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.info(
                    "Poster not available"
                )

            st.caption(
                f"Movie ID: {movie_id}"
            )


# -----------------------------
# Developer Info Section (Footer)
# -----------------------------
st.divider()

dev_col1, dev_col2, dev_col3 = st.columns([1, 2, 1])

with dev_col2:
    st.markdown("### 👨‍💻 Developed By")
    
    img_col, info_col = st.columns([1, 2])
    
    with img_col:
        # GitHub se raw image URL
        IMAGE_URL = "https://raw.githubusercontent.com/Anish-kumar-00/MOVIE-RECOMMENDATION-SYSTEM/main/anish.jpg"
        
        try:
            st.image(IMAGE_URL, width=140)
        except Exception:
            st.warning("Developer image not available")
            
    with info_col:
        st.subheader("Anish Kumar")
        st.markdown("**Project Lead & Developer**")
        st.write("Machine Learning & Web Application Project")
