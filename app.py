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
# 3. LOAD MOVIE DATA
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
# 5. FETCH MOVIE POSTER
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

            data = response.json()

            videos = data.get("results", [])

            # First search for official YouTube trailer
            for video in videos:

                if (
                    video.get("site") == "YouTube"
                    and video.get("type") == "Trailer"
                    and video.get("official") is True
                ):

                    return (
                        f"https://www.youtube.com/watch?v="
                        f"{video.get('key')}"
                    )

            # If official trailer is not available,
            # find any YouTube trailer
            for video in videos:

                if (
                    video.get("site") == "YouTube"
                    and video.get("type") == "Trailer"
                ):

                    return (
                        f"https://www.youtube.com/watch?v="
                        f"{video.get('key')}"
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

    # Get 20 similar movies
    for movie_index in similarity_indices[index][0:20]:

        movie_index = int(movie_index)

        movie_id = movies.iloc[movie_index]["movie_id"]

        movie_name = movies.iloc[movie_index]["title"]

        names.append(movie_name)

        posters.append(
            fetch_poster(movie_id)
        )

        ids.append(movie_id)

    return names, posters, ids


# ============================================================
# 9. MOVIE DETAILS PAGE
# ============================================================

def show_movie_details(movie_id):

    # Back button
    if st.button("⬅️ Back to Recommendations"):

        st.query_params.clear()

        st.rerun()

    st.divider()

    # Get movie details
    details = fetch_movie_details(movie_id)

    if not details:

        st.error("❌ Movie information could not be loaded.")

        return

    # --------------------------------------------------------
    # Movie information
    # --------------------------------------------------------

    title = details.get(
        "title",
        "Unknown Movie"
    )

    overview = details.get(
        "overview",
        "No description available."
    )

    rating = details.get(
        "vote_average",
        0
    )

    release_date = details.get(
        "release_date",
        "Unknown"
    )

    runtime = details.get(
        "runtime",
        0
    )

    genres = details.get(
        "genres",
        []
    )

    poster_path = details.get(
        "poster_path"
    )

    backdrop_path = details.get(
        "backdrop_path"
    )


    # ========================================================
    # BACKGROUND IMAGE
    # ========================================================

    if backdrop_path:

        backdrop_url = (
            "https://image.tmdb.org/t/p/original"
            + backdrop_path
        )

        st.markdown(
            f"""
            <style>

            .movie-banner {{
                width: 100%;
                height: 300px;

                background-image:
                linear-gradient(
                    rgba(0,0,0,0.45),
                    rgba(0,0,0,0.85)
                ),
                url("{backdrop_url}");

                background-size: cover;
                background-position: center;

                border-radius: 15px;

                margin-bottom: 30px;
            }}

            </style>

            <div class="movie-banner"></div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # TITLE
    # ========================================================

    st.title(f"🎬 {title}")


    # ========================================================
    # POSTER + DETAILS
    # ========================================================

    col1, col2 = st.columns(
        [1, 2],
        gap="large"
    )


    # --------------------------------------------------------
    # POSTER
    # --------------------------------------------------------

    with col1:

        if poster_path:

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

            st.image(
                poster_url,
                use_container_width=True
            )

        else:

            st.info(
                "Poster not available"
            )


    # --------------------------------------------------------
    # MOVIE INFORMATION
    # --------------------------------------------------------

    with col2:

        st.markdown(
            f"### ⭐ Rating: {rating:.1f}/10"
        )

        st.markdown(
            f"### 📅 Release Date: {release_date}"
        )

        if runtime:

            hours = runtime // 60
            minutes = runtime % 60

            if hours > 0:

                runtime_text = (
                    f"{hours}h {minutes}min"
                )

            else:

                runtime_text = (
                    f"{minutes}min"
                )

            st.markdown(
                f"### ⏱️ Runtime: {runtime_text}"
            )


        # ----------------------------------------------------
        # GENRES
        # ----------------------------------------------------

        if genres:

            genre_names = [
                genre["name"]
                for genre in genres
            ]

            st.markdown(
                "### 🎭 Genres"
            )

            st.write(
                " • ".join(genre_names)
            )


        # ----------------------------------------------------
        # OVERVIEW
        # ----------------------------------------------------

        st.markdown(
            "### 📝 Story"
        )

        st.write(
            overview
        )


        # ----------------------------------------------------
        # TRAILER
        # ----------------------------------------------------

        st.markdown(
            "### ▶️ Watch Trailer"
        )

        trailer_url = fetch_trailer(
            movie_id
        )

        if trailer_url:

            st.link_button(
                "▶️ Watch Trailer on YouTube",
                trailer_url,
                use_container_width=True
            )

        else:

            st.info(
                "Trailer is not available."
            )


# ============================================================
# 10. CHECK WHETHER DETAILS PAGE IS OPEN
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 11. DETAILS PAGE
# ============================================================

if movie_id_from_url:

    try:

        movie_id = int(
            movie_id_from_url
        )

        show_movie_details(
            movie_id
        )

    except ValueError:

        st.error(
            "Invalid movie ID."
        )


# ============================================================
# 12. MAIN RECOMMENDATION PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.title(
        "🎬 Movie Recommendation System MADE BY ANISH"
    )

    st.write(
        "Find movies similar to your favourite movie."
    )


    # --------------------------------------------------------
    # MOVIE LIST
    # --------------------------------------------------------

    movie_list = movies["title"].values


    # Avatar as default movie
    default_index = 0

    if "Avatar" in movie_list:

        default_index = int(
            list(movie_list).index(
                "Avatar"
            )
        )


    selected_movie = st.selectbox(
        "🎥 Select a movie",
        movie_list,
        index=default_index
    )


    # --------------------------------------------------------
    # GET RECOMMENDATIONS
    # --------------------------------------------------------

    names, posters, ids = recommend(
        selected_movie
    )


    st.subheader(
        f"✨ Recommended Movies for '{selected_movie}'"
    )


    # --------------------------------------------------------
    # NETFLIX STYLE GRID
    # --------------------------------------------------------

    COLS_PER_ROW = 5


    for i in range(
        0,
        len(names),
        COLS_PER_ROW
    ):

        cols = st.columns(
            COLS_PER_ROW
        )


        for j in range(
            COLS_PER_ROW
        ):

            if i + j < len(names):

                name = names[i + j]

                poster = posters[i + j]

                movie_id = ids[i + j]


                with cols[j]:

                    # Poster
                    if poster:

                        st.image(
                            poster,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "Poster not available"
                        )


                    # Movie name
                    st.markdown(
                        f"**{name}**"
                    )


                    # Movie ID
                    st.caption(
                        f"Movie ID: {movie_id}"
                    )


                    # Details button
                    if st.button(
                        "🎬 View Details",
                        key=f"details_{movie_id}_{i}_{j}",
                        use_container_width=True
                    ):

                        st.query_params[
                            "movie_id"
                        ] = str(movie_id)

                        st.rerun()


    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()


    dev_col1, dev_col2, dev_col3 = st.columns(
        [1, 2, 1]
    )


    with dev_col2:

        st.markdown(
            "### 👨‍💻 Developed By"
        )

        st.subheader(
            "Anish Kumar"
        )

        st.markdown(
            "**Project Lead & Developer**"
        )

        st.write(
            "Machine Learning & Web Application Project"
        )

"secrets.toml"

Tumhara existing API key wala setup same rahega:

TMDB_API_KEY = "YOUR_TMDB_API_KEY"

Ab flow: movie select karo → recommendations aayengi → 🎬 View Details dabao → details page khulega → ▶️ Watch Trailer on YouTube se trailer open hoga → ⬅️ Back to Recommendations se wapas aa jaoge.

Ek limitation: full movie ka Play button automatically nahi banega, kyunki TMDB movie information/trailer metadata deta hai; full movie playback ke liye authorized streaming source/API chahiye.