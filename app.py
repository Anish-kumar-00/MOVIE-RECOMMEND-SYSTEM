import gzip
import os
import pickle
import requests
import html
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
# 2. GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN PAGE
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(255, 0, 80, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(100, 50, 255, 0.10),
                transparent 30%
            ),
            #080808;
        color: white;
    }


    /* ======================================================
       REMOVE DEFAULT PADDING
       ====================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }


    /* ======================================================
       HERO SECTION
       ====================================================== */

    .hero {
        text-align: center;
        padding: 35px 20px 45px 20px;
        margin-bottom: 25px;

        background:
            linear-gradient(
                135deg,
                rgba(255, 0, 70, 0.16),
                rgba(70, 20, 120, 0.12)
            );

        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 25px;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.45);

        animation: heroFade 1s ease;
    }


    .hero-title {
        font-size: 55px;
        font-weight: 900;

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

        animation: gradientMove 5s infinite linear;

        margin-bottom: 10px;
    }


    .hero-subtitle {
        color: #bdbdbd;
        font-size: 19px;
    }


    @keyframes gradientMove {

        0% {
            background-position: 0%;
        }

        100% {
            background-position: 300%;
        }

    }


    @keyframes heroFade {

        from {
            opacity: 0;
            transform: translateY(-20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    /* ======================================================
       SEARCH / SELECTBOX
       ====================================================== */

    div[data-baseweb="select"] > div {

        background: rgba(25,25,25,0.85) !important;

        border: 1px solid
        rgba(255,255,255,0.12) !important;

        border-radius: 14px !important;

        min-height: 52px;

        transition: 0.3s;
    }


    div[data-baseweb="select"] > div:hover {

        border-color:
        rgba(255,65,108,0.8) !important;

        box-shadow:
        0 0 20px rgba(255,65,108,0.15);
    }


    /* ======================================================
       MOVIE CARD
       ====================================================== */

    .movie-card {

        background:
            linear-gradient(
                145deg,
                rgba(30,30,30,0.95),
                rgba(14,14,14,0.98)
            );

        border-radius: 18px;

        padding: 8px;

        margin-bottom: 15px;

        border: 1px solid
        rgba(255,255,255,0.08);

        box-shadow:
            0 8px 30px rgba(0,0,0,0.35);

        transition:
            transform 0.35s ease,
            box-shadow 0.35s ease,
            border-color 0.35s ease;

        animation: cardAppear 0.6s ease;
    }


    .movie-card:hover {

        transform:
            translateY(-12px)
            scale(1.025);

        border-color:
            rgba(255,65,108,0.65);

        box-shadow:
            0 18px 45px
            rgba(255,30,80,0.18);
    }


    @keyframes cardAppear {

        from {
            opacity: 0;
            transform: translateY(20px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    /* ======================================================
       CLICKABLE POSTER
       ====================================================== */

    .poster-link {

        display: block;

        position: relative;

        overflow: hidden;

        border-radius: 14px;

        text-decoration: none;
    }


    .poster-link img {

        width: 100%;

        aspect-ratio: 2 / 3;

        object-fit: cover;

        display: block;

        transition:
            transform 0.45s ease,
            filter 0.45s ease;
    }


    .poster-link:hover img {

        transform: scale(1.09);

        filter:
            brightness(0.55)
            saturate(1.15);
    }


    .poster-overlay {

        position: absolute;

        inset: 0;

        display: flex;

        justify-content: center;

        align-items: center;

        opacity: 0;

        transition: 0.35s;

        background:
            linear-gradient(
                rgba(0,0,0,0.05),
                rgba(0,0,0,0.65)
            );
    }


    .poster-link:hover .poster-overlay {

        opacity: 1;
    }


    .view-text {

        background:
            rgba(255,65,108,0.95);

        color: white;

        padding: 10px 18px;

        border-radius: 25px;

        font-weight: 700;

        box-shadow:
            0 8px 25px
            rgba(255,65,108,0.35);
    }


    /* ======================================================
       MOVIE NAME
       ====================================================== */

    .movie-name {

        font-size: 17px;

        font-weight: 700;

        margin-top: 12px;

        margin-bottom: 8px;

        white-space: nowrap;

        overflow: hidden;

        text-overflow: ellipsis;

        color: white;
    }


    /* ======================================================
       DETAILS BUTTON
       ====================================================== */

    .stButton > button {

        border-radius: 12px !important;

        border: 1px solid
        rgba(255,255,255,0.10) !important;

        background:
            linear-gradient(
                135deg,
                #ff416c,
                #ff4b2b
            ) !important;

        color: white !important;

        font-weight: 700 !important;

        transition: 0.3s !important;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 8px 25px
            rgba(255,65,108,0.30);
    }


    /* ======================================================
       DETAILS PAGE
       ====================================================== */

    .details-title {

        font-size: 50px;

        font-weight: 900;

        margin-bottom: 20px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #ff416c
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;
    }


    .info-box {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.08);

        border-radius: 18px;

        padding: 20px;

        margin-bottom: 15px;

        backdrop-filter: blur(10px);

        animation: fadeUp 0.7s ease;
    }


    .rating-box {

        display: inline-block;

        padding: 10px 18px;

        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                #ffb300,
                #ff6f00
            );

        color: white;

        font-weight: 800;

        font-size: 18px;

        box-shadow:
            0 8px 25px
            rgba(255,150,0,0.20);
    }


    @keyframes fadeUp {

        from {
            opacity: 0;
            transform: translateY(25px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    /* ======================================================
       BACKDROP
       ====================================================== */

    .movie-banner {

        width: 100%;

        height: 380px;

        background-size: cover;

        background-position: center;

        border-radius: 24px;

        margin-bottom: 30px;

        position: relative;

        overflow: hidden;

        box-shadow:
            0 20px 60px
            rgba(0,0,0,0.55);

        animation: bannerAppear 1s ease;
    }


    .movie-banner::after {

        content: "";

        position: absolute;

        inset: 0;

        background:
            linear-gradient(
                to top,
                #080808 0%,
                transparent 60%
            );
    }


    @keyframes bannerAppear {

        from {
            opacity: 0;
            transform: scale(0.97);
        }

        to {
            opacity: 1;
            transform: scale(1);
        }

    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {

        text-align: center;

        padding: 35px;

        margin-top: 50px;

        border-top:
            1px solid
            rgba(255,255,255,0.08);

        color: #999;
    }


    .developer {

        color: white;

        font-size: 20px;

        font-weight: 800;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 768px) {

        .hero-title {
            font-size: 36px;
        }

        .hero-subtitle {
            font-size: 15px;
        }

        .movie-banner {
            height: 220px;
        }

        .details-title {
            font-size: 35px;
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
# 4. LOAD DATA
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
# 6. FETCH POSTER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_poster(movie_id):

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
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()

            poster_path = data.get(
                "poster_path"
            )

            if poster_path:

                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

    except Exception:

        return None

    return None


# ============================================================
# 7. FETCH MOVIE DETAILS
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
            timeout=5
        )

        if response.status_code == 200:

            return response.json()

    except Exception:

        return None

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
            timeout=5
        )

        if response.status_code == 200:

            videos = response.json().get(
                "results",
                []
            )

            # ------------------------------------------
            # Official Trailer
            # ------------------------------------------

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

            # ------------------------------------------
            # Any Trailer
            # ------------------------------------------

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
# 9. RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie):

    index = movies[
        movies["title"] == movie
    ].index[0]

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

    # ------------------------------------------
    # Back Button
    # ------------------------------------------

    if st.button(
        "⬅️ Back to Recommendations"
    ):

        st.query_params.clear()

        st.rerun()


    st.divider()


    # ------------------------------------------
    # Fetch Details
    # ------------------------------------------

    details = fetch_movie_details(
        movie_id
    )


    if not details:

        st.error(
            "Movie information could not be loaded."
        )

        return


    # ------------------------------------------
    # Basic Information
    # ------------------------------------------

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

        st.markdown(
            f"""
            <div
                class="movie-banner"
                style="
                    background-image:
                    linear-gradient(
                        rgba(0,0,0,0.15),
                        rgba(0,0,0,0.88)
                    ),
                    url('{backdrop_url}');
                "
            >
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # TITLE
    # ========================================================

    safe_title = html.escape(title)

    st.markdown(
        f"""
        <div class="details-title">
            🎬 {safe_title}
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # POSTER + DETAILS
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
            <div class="info-box">

                <div class="rating-box">
                    ⭐ {rating:.1f}/10
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Release Date
        st.markdown(
            f"""
            <div class="info-box">

                <h3>📅 Release Date</h3>

                <p>{html.escape(str(release_date))}</p>

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
                <div class="info-box">

                    <h3>⏱️ Runtime</h3>

                    <p>{runtime_text}</p>

                </div>
                """,
                unsafe_allow_html=True
            )


        # Genres
        if genres:

            genre_names = [
                genre.get("name", "")
                for genre in genres
            ]

            genre_text = " • ".join(
                genre_names
            )


            st.markdown(
                f"""
                <div class="info-box">

                    <h3>🎭 Genres</h3>

                    <p>
                        {html.escape(genre_text)}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        # Story
        st.markdown(
            f"""
            <div class="info-box">

                <h3>📝 Story</h3>

                <p>
                    {html.escape(overview)}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Trailer
        st.markdown(
            """
            <div class="info-box">

                <h3>▶️ Trailer</h3>

            </div>
            """,
            unsafe_allow_html=True
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
                "Trailer not available for this movie."
            )


# ============================================================
# 11. GET MOVIE ID FROM URL
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 12. DETAILS PAGE
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
# 13. MAIN PAGE
# ============================================================

else:

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        """
        <div class="hero">

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
    # MOVIE SELECTOR
    # ========================================================

    st.markdown(
        "### 🎥 Choose Your Movie"
    )


    movie_list = movies[
        "title"
    ].values


    default_index = 0


    if "Avatar" in movie_list:

        default_index = int(
            list(movie_list).index(
                "Avatar"
            )
        )


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


    st.markdown(
        f"""
        ### ✨ Recommended Movies

        Showing movies similar to
        **{html.escape(selected_movie)}**
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MOVIE GRID
    # ========================================================

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

                safe_name = html.escape(
                    str(name)
                )


                # ==================================================
                # MOVIE CARD
                # ==================================================

                if poster:

                    # ----------------------------------------------
                    # CLICKABLE POSTER
                    # ----------------------------------------------

                    st.markdown(
                        f"""
                        <div class="movie-card">

                            <a
                                class="poster-link"
                                href="?movie_id={movie_id}"
                            >

                                <img
                                    src="{poster}"
                                    alt="{safe_name}"
                                >

                                <div class="poster-overlay">

                                    <div class="view-text">
                                        🎬 View Details
                                    </div>

                                </div>

                            </a>

                            <div class="movie-name">
                                {safe_name}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="movie-card">

                            <div
                                style="
                                height:350px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                background:#151515;
                                border-radius:14px;
                                "
                            >

                                🎬 Poster Not Available

                            </div>

                            <div class="movie-name">
                                {safe_name}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # ==================================================
                # DETAILS BUTTON
                # ==================================================

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

    st.markdown(
        """
        <div class="footer">

            <div class="developer">
                👨‍💻 Developed By
            </div>

            <br>

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