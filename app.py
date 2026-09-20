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
# 2. File paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(BASE_DIR, "movies.pkl")
SIMILARITY_FILE = os.path.join(BASE_DIR, "similarity.pkl.gz")

# -----------------------------
# 3. Load movies & similarity data
# -----------------------------
with open(MOVIES_FILE, "rb") as f:
    movies = pickle.load(f)

with gzip.open(SIMILARITY_FILE, "rb") as f:
    similarity_data = pickle.load(f)

similarity_indices = similarity_data["indices"]

# -----------------------------
# 4. TMDB API Function
# -----------------------------
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


# -----------------------------
# 5. Recommendation Function
# -----------------------------
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    names = []
    posters = []
    ids = []

    for movie_index in similarity_indices[index][0:10]:
        movie_index = int(movie_index)
        movie_id = movies.iloc[movie_index]["movie_id"]
        movie_name = movies.iloc[movie_index]["title"]

        names.append(movie_name)
        posters.append(fetch_poster(movie_id))
        ids.append(movie_id)

    return names, posters, ids


# -----------------------------
# 6. App User Interface (UI)
# -----------------------------
st.title("🎬 Movie Recommendation System")
st.write("Find movies similar to your favourite movie.")

selected_movie = st.selectbox("🎥 Select a movie", movies["title"].values)

if st.button("🚀 Show Recommendation"):
    names, posters, ids = recommend(selected_movie)

    st.subheader("✨ Recommended Movies")
    cols = st.columns(5)

    for col, name, poster, movie_id in zip(cols, names, posters, ids):
        with col:
            st.markdown(f"**{name}**")
            if poster:
                st.image(poster, use_container_width=True)
            else:
                st.info("Poster not available")
            st.caption(f"Movie ID: {movie_id}")


# -----------------------------
# 7. Developer Info Section (Footer)
# -----------------------------
st.divider()

dev_col1, dev_col2, dev_col3 = st.columns([1, 2, 1])

with dev_col2:
    st.markdown("### 👨‍💻 Developed By")

    img_col, info_col = st.columns([1, 2])

    # KANAN DURA: Linkii suuraa direct ta'e (.jpg/.png) bakka kana galchaa:
    IMAGE_URL = "https://i.postimg.cc/xyz/your-image.jpg"

    with img_col:
        # Streamlit PIL dogoggora malee HTML'n render godha
        st.markdown(
            f'<img src="{IMAGE_URL}" width="130" style="border-radius: 10px; object-fit: cover;">',
            unsafe_allow_html=True,
        )

    with info_col:
        st.subheader("Anish Kumar")
        st.markdown("**Project Lead & Developer**")
        st.write("Machine Learning & Web Application Project")
