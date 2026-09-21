import gzip
import os
import pickle
import requests
import streamlit as st


# ============================================================
# 1. PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN BACKGROUND
       ================================ */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(255, 0, 80, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at bottom right,
                rgba(90, 40, 200, 0.12),
                transparent 30%
            ),
            #08090d;
    }


    /* ================================
       PAGE WIDTH
       ================================ */

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ================================
       HERO
       ================================ */

    .hero-box {
        padding: 35px 20px;
        text-align: center;

        border-radius: 25px;

        background:
            linear-gradient(
                135deg,
                rgba(255, 20, 70, 0.16),
                rgba(100, 30, 180, 0.14)
            );

        border: 1px solid rgba(255,255,255,0.08);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.40);

        margin-bottom: 30px;
    }


    .hero-title {
        font-size: 48px;
        font-weight: 900;
        margin-bottom: 10px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #ff416c,
                #ff4b2b,
                #ffffff
            );

        background-size: 300%;

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        animation: gradientAnimation 5s linear infinite;
    }


    .hero-subtitle {
        font-size: 18px;
        color: #bdbdbd;
    }


    @keyframes gradientAnimation {

        0% {
            background-position: 0%;
        }

        100% {
            background-position: 300%;
        }

    }


    /* ================================
       SELECT BOX
       ================================ */

    div[data-baseweb="select"] > div {

        background: #171920 !important;

        border:
            1px solid
            rgba(255,255,255,0.10) !important;

        border-radius: 12px !important;
    }


    /* ================================
       MOVIE IMAGE
       ================================ */

    [data-testid="stImage"] img {

        border-radius: 14px;

        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.45);
    }


    [data-testid="stImage"] img:hover {

        transform: scale(1.03);

        box-shadow:
            0 15px 35px
            rgba(255,50,90,0.25);
    }


    /* ================================
       BUTTON
       ================================ */

    .stButton > button {

        width: 100%;

        border-radius: 10px;

        border: none;

        background:
            linear-gradient(
                135deg,
                #ff416c,
                #ff4b2b
            );

        color: white;

        font-weight: 700;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .stButton > button:hover {

        transform: translateY(-3px);

        box-shadow:
            0 8px 25px
            rgba(255,65,108,0.35);
    }


    /* ================================
       MOVIE TITLE
       ================================ */

    .movie-title-text {

        font-size: 16px;

        font-weight: 700;

        text-align: center;

        color: white;

        margin-top: 8px;

        min-height: 45px;
    }


    /* ================================
       DETAILS PAGE
       ================================ */

    .details-title {

        font-size: 45px;

        font-weight: 900;

        margin-bottom: 20px;

        background:
            linear-gradient(
                90deg,
                white,
                #ff416c
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }


    .detail-box {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid
            rgba(255,255,255,0.08);

        border-radius: 16px;

        padding: 18px;

        margin-bottom: 15px;
    }


    .rating {

        display: inline-block;

        padding: 8px 18px;

        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                #ffb300,
                #ff6f00
            );

        color: white;

        font-weight: 800;
    }


    /* ================================
       FOOTER
       ================================ */

    .footer-line {

        margin-top: 50px;

        border-top:
            1px solid
            rgba(255,255,255,0.08);

        padding-top: 25px;

        text-align: center;

        color: #999;
    }


    /* ================================
       MOBILE
       ================================ */

    @media (max-width: 700px) {

        .hero-title {
            font-size: 34px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

        .details-title {
            font-size: 32px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MOVIES_FILE = os.path.join(
    BASE_DIR,
    "movies.pkl"
)

SIMILARITY_FILE = os.path.join(
    BASE_DIR,
    "similarity.pkl.gz"
)


# ============================================================
# 4. LOAD MOVIE DATA
# ============================================================

@st.cache_data(show_spinner=False)
def load_data():

    with open(MOVIES_FILE, "rb") as f:

        movies_data = pickle.load(f)

    with gzip.open(SIMILARITY_FILE, "rb") as f:

        similarity_data = pickle.load(f)

    return (
        movies_data,
        similarity_data["indices"]
    )


movies, similarity_indices = load_data()


# ============================================================
# 5. TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# 6. FETCH MOVIE DETAILS
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_movie_details(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
    )

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=8
        )

        if response.status_code == 200:

            return response.json()

    except Exception:

        return None

    return None


# ============================================================
# 7. FETCH POSTER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_poster(movie_id):

    details = fetch_movie_details(movie_id)

    if not details:
        return None

    poster_path = details.get(
        "poster_path"
    )

    if poster_path:

        return (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

    return None


# ============================================================
# 8. FETCH TRAILER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_trailer(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}/videos"
    )

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=8
        )

        if response.status_code == 200:

            videos = response.json().get(
                "results",
                []
            )

            # ----------------------------------------
            # Official trailer first
            # ----------------------------------------

            for video in videos:

                if (
                    video.get("site") == "YouTube"
                    and
                    video.get("type") == "Trailer"
                    and
                    video.get("official") is True
                ):

                    key = video.get("key")

                    if key:

                        return (
                            "https://www.youtube.com/watch?v="
                            + key
                        )

            # ----------------------------------------
            # Any YouTube trailer
            # ----------------------------------------

            for video in videos:

                if (
                    video.get("site") == "YouTube"
                    and
                    video.get("type") == "Trailer"
                ):

                    key = video.get("key")

                    if key:

                        return (
                            "https://www.youtube.com/watch?v="
                            + key
                        )

    except Exception:

        return None

    return None


# ============================================================
# 9. RECOMMEND MOVIES
# ============================================================

def recommend(movie):

    index_list = movies[
        movies["title"] == movie
    ].index

    if len(index_list) == 0:

        return [], [], []

    index = index_list[0]

    names = []
    posters = []
    ids = []

    for movie_index in similarity_indices[index][0:20]:

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

    return (
        names,
        posters,
        ids
    )


# ============================================================
# 10. DETAILS PAGE
# ============================================================

def movie_details_page(movie_id):

    # ----------------------------------------
    # Back button
    # ----------------------------------------

    if st.button(
        "⬅️ Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


    st.divider()


    # ----------------------------------------
    # Get movie details
    # ----------------------------------------

    details = fetch_movie_details(
        movie_id
    )


    if not details:

        st.error(
            "Movie information could not be loaded."
        )

        return


    # ----------------------------------------
    # Information
    # ----------------------------------------

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
    # BACKDROP
    # ========================================================

    if backdrop_path:

        backdrop_url = (
            "https://image.tmdb.org/t/p/original"
            + backdrop_path
        )

        st.image(
            backdrop_url,
            use_container_width=True
        )


    # ========================================================
    # TITLE
    # ========================================================

    st.markdown(
        f"## 🎬 {title}"
    )


    # ========================================================
    # POSTER + INFORMATION
    # ========================================================

    col1, col2 = st.columns(
        [1, 2],
        gap="large"
    )


    # ========================================================
    # POSTER
    # ========================================================

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
                "Poster not available."
            )


    # ========================================================
    # INFORMATION
    # ========================================================

    with col2:

        # Rating
        st.markdown(
            f"""
            <div class="detail-box">

                <div class="rating">
                    ⭐ {rating:.1f}/10
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Release date
        st.markdown(
            f"""
            <div class="detail-box">

                <h3>📅 Release Date</h3>

                <p>{release_date}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Runtime
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
                f"""
                <div class="detail-box">

                    <h3>⏱️ Runtime</h3>

                    <p>{runtime_text}</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        # Genres
        if genres:

            genre_names = []

            for genre in genres:

                genre_names.append(
                    genre.get("name", "")
                )

            genre_text = " • ".join(
                genre_names
            )


            st.markdown(
                f"""
                <div class="detail-box">

                    <h3>🎭 Genres</h3>

                    <p>{genre_text}</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        # Story
        st.markdown(
            f"""
            <div class="detail-box">

                <h3>📝 Story</h3>

                <p>{overview}</p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Trailer
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
                "Trailer not available."
            )


# ============================================================
# 11. CHECK URL
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 12. SHOW DETAILS PAGE
# ============================================================

if movie_id_from_url:

    try:

        movie_id = int(
            movie_id_from_url
        )

        movie_details_page(
            movie_id
        )

    except ValueError:

        st.error(
            "Invalid movie ID."
        )


# ============================================================
# 13. MAIN RECOMMENDATION PAGE
# ============================================================

else:

    # ========================================================
    # HERO SECTION
    # ========================================================

    st.markdown(
        """
        <div class="hero-box">

            <div class="hero-title">
                🎬 CineMatch AI
            </div>

            <div class="hero-subtitle">
                Discover movies you'll love
                with AI-powered recommendations.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SELECT MOVIE
    # ========================================================

    st.subheader(
        "🎥 Choose Your Movie"
    )


    movie_list = movies[
        "title"
    ].values


    default_index = 0


    if "Avatar" in movie_list:

        default_index = list(
            movie_list
        ).index("Avatar")


    selected_movie = st.selectbox(
        "Select a movie",
        movie_list,
        index=default_index,
        label_visibility="collapsed"
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    names, posters, ids = recommend(
        selected_movie
    )


    st.subheader(
        f"✨ Movies Similar to {selected_movie}"
    )


    st.write(
        "Click **View Details** to explore the movie."
    )


    # ========================================================
    # RESPONSIVE GRID
    # ========================================================

    # Desktop: 5 columns
    # Mobile: Streamlit automatically stacks
    # columns more naturally

    COLS_PER_ROW = 5


    for i in range(
        0,
        len(names),
        COLS_PER_ROW
    ):

        cols = st.columns(
            COLS_PER_ROW,
            gap="medium"
        )


        for j in range(
            COLS_PER_ROW
        ):

            if i + j >= len(names):

                continue


            name = names[i + j]

            poster = posters[i + j]

            movie_id = ids[i + j]


            with cols[j]:

                # ------------------------------------
                # POSTER
                # ------------------------------------

                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )


                # ------------------------------------
                # MOVIE NAME
                # ------------------------------------

                st.markdown(
                    f"""
                    <div class="movie-title-text">
                        {name}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # ------------------------------------
                # DETAILS BUTTON
                # ------------------------------------

                if st.button(
                    "🎬 View Details",
                    key=f"movie_{movie_id}_{i}_{j}",
                    use_container_width=True
                ):

                    st.query_params[
                        "movie_id"
                    ] = str(movie_id)

                    st.rerun()


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="footer-line">

            <h3>👨‍💻 Developed By</h3>

            <strong>
                Anish Kumar • Abhishek • Vishal
            </strong>

            <br><br>

            Machine Learning & Web Application Project

            <br><br>

            🎬 CineMatch AI

        </div>
        """,
        unsafe_allow_html=True
    )