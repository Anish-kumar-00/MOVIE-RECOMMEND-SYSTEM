import gzip
import os
import pickle
import requests
import streamlit as st


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# 2. FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MOVIES_FILE = os.path.join(BASE_DIR, "movies.pkl")
SIMILARITY_FILE = os.path.join(BASE_DIR, "similarity.pkl.gz")


# ============================================================
# 3. LOAD DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_data():

    with open(MOVIES_FILE, "rb") as f:
        movies_data = pickle.load(f)

    with gzip.open(SIMILARITY_FILE, "rb") as f:
        similarity_data = pickle.load(f)

    return movies_data, similarity_data["indices"]


movies, similarity_indices = load_data()


# ============================================================
# 4. TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# 5. FETCH POSTER
# ============================================================

@st.cache_data(show_spinner=False, ttl=86400)
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
            timeout=5
        )

        if response.status_code == 200:

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


# ============================================================
# 6. FETCH MOVIE DETAILS
# ============================================================

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        if response.status_code == 200:

            return response.json()

    except Exception:
        return None

    return None


# ============================================================
# 7. FETCH TRAILER
# ============================================================

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_trailer(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        if response.status_code == 200:

            videos = response.json().get("results", [])

            # Official trailer
            for video in videos:

                if (
                    video.get("site") == "YouTube"
                    and video.get("type") == "Trailer"
                    and video.get("official") is True
                ):

                    return (
                        "https://www.youtube.com/watch?v="
                        + video.get("key")
                    )

            # Any YouTube trailer
            for video in videos:

                if (
                    video.get("site") == "YouTube"
                    and video.get("type") == "Trailer"
                ):

                    return (
                        "https://www.youtube.com/watch?v="
                        + video.get("key")
                    )

    except Exception:
        return None

    return None


# ============================================================
# 8. RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    names = []
    posters = []
    ids = []

    for movie_index in similarity_indices[index][0:20]:

        movie_index = int(movie_index)

        movie_id = movies.iloc[movie_index]["movie_id"]
        movie_name = movies.iloc[movie_index]["title"]

        names.append(movie_name)
        posters.append(fetch_poster(movie_id))
        ids.append(movie_id)

    return names, posters, ids


# ============================================================
# 9. MOVIE DETAILS PAGE
# ============================================================

def movie_details_page(movie_id):

    if st.button(
        "⬅️ Back to Recommendations",
        use_container_width=False
    ):

        st.query_params.clear()
        st.rerun()

    st.divider