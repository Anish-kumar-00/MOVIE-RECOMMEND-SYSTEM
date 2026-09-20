import gzip
import os
import pickle
import requests
import streamlit as st

# -----------------------------
# 1. Page settings
# -----------------------------
st.set_page_config(
    page_title="Movie Recommendation System", page_icon="🎬", layout="wide"
)

# -----------------------------
# 2. File paths & Caching
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(BASE_DIR, "movies.pkl")
SIMILARITY_FILE = os.path.join(BASE_DIR, "similarity.pkl.gz")


# Fast data loading using Streamlit cache
@st.cache_data(show_spinner=False)
def load_data():
    with open(MOVIES_FILE, "rb") as f:
        movies_data = pickle.load(f)

    with gzip.open(SIMILARITY_FILE, "rb") as f:
        similarity_data = pickle.load(f)

    return movies_data, similarity_data["indices"]


movies, similarity_indices = load_data()

# -----------------------------
# 3. Fast TMDB API Poster Fetcher
# -----------------------------
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


@st.cache_data(show_spinner=False, ttl=86400)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        return None
    return None


# -----------------------------
# 4. Recommendation Function
# -----------------------------
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    names = []
    posters = []
    ids = []

    # 20 movies fetch ho rahi hain
    for movie_index in similarity_indices[index][0:20]:
        movie_index = int(movie_index)
        movie_id = movies.iloc[movie_index]["movie_id"]
        movie_name = movies.iloc[movie_index]["title"]

        names.append(movie_name)
        posters.append(fetch_poster(movie_id))
        ids.append(movie_id)

    return names, posters, ids


# -----------------------------
# 5. App User Interface (UI)
# -----------------------------
st.title("🎬 Movie Recommendation System MADE BY ANISH")
st.write("Find movies similar to your favourite movie.")

# Finding index of 'Avatar' to make it default
movie_list = movies["title"].values
default_index = 0
if "Avatar" in movie_list:
    default_index = int(list(movie_list).index("Avatar"))

selected_movie = st.selectbox(
    "🎥 Select a movie", movie_list, index=default_index
)

# Display recommendations by default
names, posters, ids = recommend(selected_movie)

st.subheader(f"✨ Recommended Movies for '{selected_movie}'")

# NETFLIX STYLE GRID (5 columns per row, auto-wrapping for 20 movies)
COLS_PER_ROW = 5

for i in range(0, len(names), COLS_PER_ROW):
    cols = st.columns(COLS_PER_ROW)
    for j in range(COLS_PER_ROW):
        if i + j < len(names):
            name = names[i + j]
            poster = posters[i + j]
            movie_id = ids[i + j]

            with cols[j]:
                if poster:
                    st.image(poster, use_container_width=True)
                else:
                    st.info("Poster not available")
                st.markdown(f"**{name}**")
                st.caption(f"Movie ID: {movie_id}")

# -----------------------------
# 6. Developer Info Section (Footer)
# -----------------------------
st.divider()

dev_col1, dev_col2, dev_col3 = st.columns([1, 2, 1])

with dev_col2:
    st.markdown("### 👨‍💻 Developed By")
    st.subheader("Anish Kumar")
    st.markdown("**Project Lead & Developer**")
    st.write("Machine Learning & Web Application Project")
