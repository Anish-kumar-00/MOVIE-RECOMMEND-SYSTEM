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
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. GLOBAL CSS
# ============================================================

st.html(
    """
    <style>

    /* =====================================================
       GLOBAL APP
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 10%,
                rgba(0, 100, 255, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 20%,
                rgba(255, 0, 70, 0.14),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(120, 0, 255, 0.10),
                transparent 35%
            ),
            #030308;

        color: white;
    }


    .block-container {
        max-width: 1500px;
        padding-top: 25px;
        padding-bottom: 60px;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {

        background:
            linear-gradient(
                90deg,
                rgba(0, 100, 255, 0.10),
                rgba(255, 0, 90, 0.10)
            ) !important;

        border:
            1px solid #2477ff !important;

        border-radius:
            9px !important;

        color:
            white !important;

        box-shadow:
            0 0 12px rgba(0, 100, 255, 0.25),
            0 0 18px rgba(255, 0, 90, 0.15) !important;
    }


    /* =====================================================
       NORMAL BUTTON
       ===================================================== */

    .stButton > button {

        background:
            linear-gradient(
                90deg,
                #006eff,
                #7b00ff,
                #ff0055
            ) !important;

        color:
            white !important;

        border:
            1px solid #00aaff !important;

        border-radius:
            9px !important;

        font-weight:
            800 !important;

        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.35),
            0 0 20px rgba(255, 0, 80, 0.25) !important;

        transition:
            all 0.25s ease !important;
    }


    .stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 0 25px rgba(0, 110, 255, 0.60),
            0 0 35px rgba(255, 0, 80, 0.45) !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {

        border:
            none !important;

        height:
            1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                #006eff,
                #ff0066,
                transparent
            ) !important;

        opacity:
            0.65;
    }


    /* =====================================================
       HERO
       ===================================================== */

    @keyframes heroGlow {

        0% {
            box-shadow:
                0 0 20px rgba(0, 110, 255, 0.25),
                0 0 20px rgba(255, 0, 80, 0.15);
        }

        50% {
            box-shadow:
                0 0 45px rgba(0, 110, 255, 0.55),
                0 0 55px rgba(255, 0, 80, 0.35);
        }

        100% {
            box-shadow:
                0 0 20px rgba(0, 110, 255, 0.25),
                0 0 20px rgba(255, 0, 80, 0.15);
        }
    }


    .hero-box {

        animation:
            heroGlow 4s ease-in-out infinite;

        border:
            1px solid rgba(0, 110, 255, 0.55);

        position:
            relative;

        overflow:
            hidden;
    }


    /* =====================================================
       TITLE ANIMATION
       ===================================================== */

    @keyframes titleFade {

        0% {
            opacity: 0;
            transform: translateY(20px);
        }

        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }


    .hero-content {

        animation:
            titleFade 1s ease-out;
    }


    /* =====================================================
       GRADIENT TEXT
       ===================================================== */

    .gradient-text {

        background:
            linear-gradient(
                90deg,
                #00aaff,
                #0077ff,
                #9d00ff,
                #ff0077
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;

        background-clip:
            text;
    }


    /* =====================================================
       MOVIE CARD
       ===================================================== */

    .movie-wrapper {

        position:
            relative;

        background:
            linear-gradient(
                145deg,
                #111827,
                #08090d
            );

        border:
            2px solid transparent;

        border-radius:
            13px;

        padding:
            6px;

        margin-bottom:
            22px;

        overflow:
            hidden;

        transition:
            transform 0.35s ease,
            box-shadow 0.35s ease;

        box-shadow:
            0 0 12px rgba(0, 100, 255, 0.22),
            0 0 15px rgba(255, 0, 80, 0.12);

        background-clip:
            padding-box;
    }


    .movie-wrapper::before {

        content:
            "";

        position:
            absolute;

        inset:
            -2px;

        border-radius:
            14px;

        background:
            linear-gradient(
                120deg,
                #006eff,
                #00d4ff,
                #7b00ff,
                #ff0066,
                #006eff
            );

        background-size:
            300% 300%;

        animation:
            neonBorder 4s linear infinite;

        z-index:
            -1;
    }


    @keyframes neonBorder {

        0% {
            background-position:
                0% 50%;
        }

        50% {
            background-position:
                100% 50%;
        }

        100% {
            background-position:
                0% 50%;
        }
    }


    .movie-wrapper:hover {

        transform:
            translateY(-8px)
            scale(1.025);

        box-shadow:
            0 0 20px rgba(0, 110, 255, 0.65),
            0 0 35px rgba(255, 0, 80, 0.45);
    }


    /* =====================================================
       POSTER
       ===================================================== */

    .movie-poster-container {

        position:
            relative;

        overflow:
            hidden;

        border-radius:
            8px;

        z-index:
            1;
    }


    .movie-poster {

        width:
            100%;

        aspect-ratio:
            2 / 3;

        object-fit:
            cover;

        display:
            block;

        transition:
            transform 0.5s ease,
            filter 0.5s ease;
    }


    .movie-wrapper:hover
    .movie-poster {

        transform:
            scale(1.08);

        filter:
            brightness(0.55);
    }


    /* =====================================================
       PLAY OVERLAY
       ===================================================== */

    .movie-overlay {

        position:
            absolute;

        inset:
            0;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;

        opacity:
            0;

        background:
            linear-gradient(
                to bottom,
                rgba(0,0,0,0.05),
                rgba(0,0,0,0.88)
            );

        transition:
            opacity 0.35s ease;
    }


    .movie-wrapper:hover
    .movie-overlay {

        opacity:
            1;
    }


    .play-circle {

        width:
            58px;

        height:
            58px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;

        border-radius:
            50%;

        background:
            linear-gradient(
                135deg,
                #006eff,
                #ff0055
            );

        color:
            white;

        font-size:
            23px;

        box-shadow:
            0 0 25px rgba(0, 110, 255, 0.65),
            0 0 30px rgba(255, 0, 80, 0.45);
    }


    /* =====================================================
       MOVIE TITLE
       ===================================================== */

    .movie-title {

        position:
            relative;

        z-index:
            2;

        color:
            white;

        font-size:
            13px;

        font-weight:
            700;

        text-align:
            center;

        padding:
            10px 5px 7px;

        min-height:
            42px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;
    }


    /* =====================================================
       SECTION TITLE
       ===================================================== */

    .section-title {

        font-size:
            32px;

        font-weight:
            900;

        margin-top:
            25px;

        margin-bottom:
            5px;
    }


    .section-subtitle {

        color:
            #999;

        margin-bottom:
            25px;
    }


    /* =====================================================
       DETAIL PAGE
       ===================================================== */

    .detail-title {

        font-size:
            38px;

        font-weight:
            900;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #00aaff,
                #ff0066
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;
    }


    /* =====================================================
       WIDE TRAILER
       ===================================================== */

    .trailer-section {

        width:
            100%;

        margin:
            0 auto 30px auto;
    }


    .trailer-heading {

        font-size:
            28px;

        font-weight:
            900;

        margin-bottom:
            14px;

        background:
            linear-gradient(
                90deg,
                #00aaff,
                #ffffff,
                #ff0066
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;
    }


    .trailer-box {

        width:
            100%;

        aspect-ratio:
            16 / 9;

        border-radius:
            15px;

        overflow:
            hidden;

        border:
            2px solid transparent;

        background:
            linear-gradient(#050509, #050509) padding-box,
            linear-gradient(
                90deg,
                #006eff,
                #00d9ff,
                #8b00ff,
                #ff0055
            ) border-box;

        box-shadow:
            0 0 20px rgba(0, 110, 255, 0.45),
            0 0 35px rgba(255, 0, 80, 0.30);

        position:
            relative;
    }


    .trailer-box iframe {

        width:
            100% !important;

        height:
            100% !important;

        border:
            0 !important;

        display:
            block;
    }


    /* =====================================================
       CENTER POSTER
       ===================================================== */

    .poster-center {

        display:
            flex;

        justify-content:
            center;

        align-items:
            center;

        width:
            100%;

        margin:
            15px auto 35px auto;
    }


    .poster-center img {

        width:
            260px;

        max-width:
            75vw;

        aspect-ratio:
            2 / 3;

        object-fit:
            cover;

        border-radius:
            12px;

        border:
            2px solid transparent;

        background:
            linear-gradient(#050509, #050509) padding-box,
            linear-gradient(
                135deg,
                #006eff,
                #7b00ff,
                #ff0055
            ) border-box;

        box-shadow:
            0 0 20px rgba(0, 110, 255, 0.50),
            0 0 35px rgba(255, 0, 80, 0.30);
    }


    /* =====================================================
       INFORMATION PANEL
       ===================================================== */

    .info-panel {

        width:
            100%;

        padding:
            25px;

        border-radius:
            16px;

        background:
            linear-gradient(
                135deg,
                rgba(5, 12, 30, 0.95),
                rgba(20, 5, 20, 0.95)
            );

        border:
            1px solid transparent;

        background:
            linear-gradient(
                rgba(5, 10, 25, 0.96),
                rgba(15, 5, 20, 0.96)
            ) padding-box,

            linear-gradient(
                90deg,
                #006eff,
                #7b00ff,
                #ff0055
            ) border-box;

        box-shadow:
            0 0 25px rgba(0, 110, 255, 0.20),
            0 0 30px rgba(255, 0, 80, 0.16);

        margin-bottom:
            30px;
    }


    .info-main-title {

        font-size:
            32px;

        font-weight:
            900;

        margin-bottom:
            20px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #00b7ff,
                #ff0066
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;
    }


    .info-grid {

        display:
            grid;

        grid-template-columns:
            repeat(3, 1fr);

        gap:
            15px;

        margin-bottom:
            20px;
    }


    .info-item {

        padding:
            18px;

        border-radius:
            12px;

        background:
            linear-gradient(
                135deg,
                rgba(0, 110, 255, 0.10),
                rgba(255, 0, 80, 0.08)
            );

        border:
            1px solid rgba(0, 150, 255, 0.30);

        box-shadow:
            inset 0 0 15px rgba(0, 110, 255, 0.06);
    }


    .info-label {

        font-size:
            13px;

        color:
            #8e8e9a;

        margin-bottom:
            7px;
    }


    .info-value {

        font-size:
            19px;

        font-weight:
            800;

        color:
            #ffffff;
    }


    .info-value.rating {

        color:
            #ffd43b;

        text-shadow:
            0 0 12px rgba(255, 210, 0, 0.35);
    }


    .info-block {

        padding:
            18px 0;

        border-top:
            1px solid rgba(0, 120, 255, 0.22);
    }


    .info-block-title {

        font-size:
            20px;

        font-weight:
            800;

        margin-bottom:
            9px;

        color:
            #ffffff;
    }


    .info-block-text {

        color:
            #c5c5cc;

        font-size:
            15px;

        line-height:
            1.7;
    }


    .genre-tag {

        display:
            inline-block;

        padding:
            7px 13px;

        margin:
            4px 5px 4px 0;

        border-radius:
            20px;

        background:
            linear-gradient(
                90deg,
                rgba(0, 110, 255, 0.20),
                rgba(255, 0, 80, 0.20)
            );

        border:
            1px solid rgba(0, 160, 255, 0.55);

        color:
            #ffffff;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer-title {

        color:
            #ffffff;

        font-size:
            22px;

        font-weight:
            800;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding-left:
                12px;

            padding-right:
                12px;
        }


        .hero-box {

            min-height:
                300px !important;

            padding:
                28px !important;
        }


        .section-title {

            font-size:
                25px;
        }


        .movie-wrapper {

            border-radius:
                10px;

            padding:
                5px;

            margin-bottom:
                16px;
        }


        .movie-wrapper:hover {

            transform:
                translateY(-3px)
                scale(1.01);
        }


        .movie-title {

            font-size:
                11px;

            min-height:
                38px;
        }


        .detail-title {

            font-size:
                30px;
        }


        .trailer-heading {

            font-size:
                23px;
        }


        .trailer-box {

            border-radius:
                10px;

            aspect-ratio:
                16 / 9;
        }


        .poster-center img {

            width:
                220px;
        }


        .info-panel {

            padding:
                18px;
        }


        .info-grid {

            grid-template-columns:
                1fr;

            gap:
                10px;
        }


        .info-main-title {

            font-size:
                27px;
        }

    }

    </style>
    """
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

    with open(
        MOVIES_FILE,
        "rb"
    ) as file:

        movies_data = pickle.load(file)


    with gzip.open(
        SIMILARITY_FILE,
        "rb"
    ) as file:

        similarity_data = pickle.load(file)


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
# 6. TMDB REQUEST
# ============================================================

def tmdb_request(
    endpoint,
    params=None
):

    url = (
        "https://api.themoviedb.org/3/"
        + endpoint
    )


    if params is None:

        params = {}


    params = params.copy()

    params["api_key"] = TMDB_API_KEY


    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )


        if response.status_code == 200:

            return response.json()


    except Exception:

        return None


    return None


# ============================================================
# 7. MOVIE DETAILS
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_movie_details(
    movie_id
):

    return tmdb_request(
        f"movie/{movie_id}",
        {
            "language": "en-US"
        }
    )


# ============================================================
# 8. POSTER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_poster(
    movie_id
):

    details = fetch_movie_details(
        movie_id
    )


    if not details:

        return None


    poster_path = details.get(
        "poster_path"
    )


    if not poster_path:

        return None


    return (
        "https://image.tmdb.org/t/p/w500"
        + poster_path
    )


# ============================================================
# 9. TRAILER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_trailer(
    movie_id
):

    data = tmdb_request(
        f"movie/{movie_id}/videos",
        {
            "language": "en-US"
        }
    )


    if not data:

        return None


    videos = data.get(
        "results",
        []
    )


    # Official YouTube Trailer
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

                return key


    # Any YouTube Trailer
    for video in videos:

        if (
            video.get("site") == "YouTube"
            and
            video.get("type") == "Trailer"
        ):

            key = video.get("key")

            if key:

                return key


    # YouTube Teaser
    for video in videos:

        if (
            video.get("site") == "YouTube"
            and
            video.get("type") == "Teaser"
        ):

            key = video.get("key")

            if key:

                return key


    return None


# ============================================================
# 10. RECOMMENDATION
# ============================================================

def recommend(movie):

    indexes = movies[
        movies["title"] == movie
    ].index


    if len(indexes) == 0:

        return [], [], []


    index = indexes[0]


    names = []
    posters = []
    ids = []


    similar_movies = similarity_indices[
        index
    ][0:20]


    for movie_index in similar_movies:

        movie_index = int(
            movie_index
        )


        movie_id = movies.iloc[
            movie_index
        ]["movie_id"]


        movie_name = movies.iloc[
            movie_index
        ]["title"]


        names.append(
            movie_name
        )


        posters.append(
            fetch_poster(
                movie_id
            )
        )


        ids.append(
            movie_id
        )


    return (
        names,
        posters,
        ids
    )


# ============================================================
# 11. MOVIE CARD
# ============================================================

def movie_card_html(
    movie_name,
    poster_url,
    movie_id
):

    if not poster_url:

        poster_url = (
            "https://via.placeholder.com/"
            "500x750?text=No+Poster"
        )


    return f"""
    <a
        href="?movie_id={movie_id}"
        target="_self"
        style="
            display:block;
            text-decoration:none;
            color:white;
        "
    >

        <div class="movie-wrapper">

            <div class="movie-poster-container">

                <img
                    class="movie-poster"
                    src="{poster_url}"
                    alt="{movie_name}"
                >

                <div class="movie-overlay">

                    <div class="play-circle">
                        ▶
                    </div>

                </div>

            </div>

            <div class="movie-title">
                {movie_name}
            </div>

        </div>

    </a>
    """


# ============================================================
# 12. DETAILS PAGE
# ============================================================

def show_movie_details(
    movie_id
):

    # ========================================================
    # BACK BUTTON
    # ========================================================

    if st.button(
        "← Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


    # ========================================================
    # GET DETAILS
    # ========================================================

    details = fetch_movie_details(
        movie_id
    )


    if not details:

        st.error(
            "Movie information could not be loaded."
        )

        return


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
    # 1. TRAILER FIRST
    # ========================================================

    trailer_key = fetch_trailer(
        movie_id
    )


    if trailer_key:

        st.html(
            f"""
            <div class="trailer-section">

                <div class="trailer-heading">
                    ▶️ Trailer
                </div>

                <div class="trailer-box">

                    <iframe
                        src="https://www.youtube.com/embed/{trailer_key}"
                        title="{title} Trailer"
                        allow="
                            accelerometer;
                            autoplay;
                            clipboard-write;
                            encrypted-media;
                            gyroscope;
                            picture-in-picture;
                            web-share
                        "
                        allowfullscreen>
                    </iframe>

                </div>

            </div>
            """
        )

    else:

        st.info(
            "Trailer not available."
        )


    # ========================================================
    # 2. CENTER POSTER
    # ========================================================

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )


        st.html(
            f"""
            <div class="poster-center">

                <img
                    src="{poster_url}"
                    alt="{title}"
                >

            </div>
            """
        )


    # ========================================================
    # 3. MOVIE INFORMATION BELOW POSTER
    # ========================================================

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

    else:

        runtime_text = "N/A"


    genre_html = ""


    for genre in genres:

        genre_name = genre.get(
            "name"
        )

        if genre_name:

            genre_html += (
                f'<span class="genre-tag">'
                f'{genre_name}'
                f'</span>'
            )


    st.html(
        f"""
        <div class="info-panel">

            <div class="info-main-title">
                🎬 {title}
            </div>


            <div class="info-grid">

                <div class="info-item">

                    <div class="info-label">
                        ⭐ Rating
                    </div>

                    <div class="info-value rating">
                        ⭐ {rating:.1f}/10
                    </div>

                    <div class="info-label">
                        TMDB Rating
                    </div>

                </div>


                <div class="info-item">

                    <div class="info-label">
                        📅 Release Date
                    </div>

                    <div class="info-value">
                        {release_date}
                    </div>

                </div>


                <div class="info-item">

                    <div class="info-label">
                        ⏱️ Runtime
                    </div>

                    <div class="info-value">
                        {runtime_text}
                    </div>

                </div>

            </div>


            <div class="info-block">

                <div class="info-block-title">
                    🎭 Genres
                </div>

                <div>
                    {genre_html if genre_html else "N/A"}
                </div>

            </div>


            <div class="info-block">

                <div class="info-block-title">
                    📝 Story
                </div>

                <div class="info-block-text">
                    {overview}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# 13. CHECK MOVIE ID
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 14. DETAILS PAGE
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
# 15. MAIN PAGE
# ============================================================

else:

    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div
            class="hero-box"
            style="
                min-height:390px;

                display:flex;

                align-items:flex-end;

                padding:50px;

                border-radius:16px;

                background:
                    radial-gradient(
                        circle at 75% 30%,
                        rgba(0,110,255,0.20),
                        transparent 30%
                    ),
                    radial-gradient(
                        circle at 90% 70%,
                        rgba(255,0,80,0.18),
                        transparent 30%
                    ),
                    linear-gradient(
                        90deg,
                        #050505 0%,
                        #080912 50%,
                        #09050a 100%
                    );

                margin-bottom:40px;
            "
        >

            <div class="hero-content">

                <div
                    style="
                        color:#ff174f;
                        font-size:14px;
                        font-weight:900;
                        letter-spacing:4px;
                        margin-bottom:12px;
                    "
                >
                    DEVELOPED BY ANISH-ABRAR-ABHISHEK-VISHAL
                </div>


                <div
                    style="
                        font-size:clamp(36px,6vw,68px);
                        font-weight:900;
                        line-height:1.05;
                        margin-bottom:18px;
                    "
                >
                    <span style="color:white;">
                        Movie
                    </span>

                    <br>

                    <span class="gradient-text">
                        Recommendation
                    </span>

                    <br>

                    <span style="color:white;">
                        System
                    </span>
                </div>


                <div
                    style="
                        color:#bdbdbd;
                        font-size:17px;
                        line-height:1.6;
                        max-width:650px;
                    "
                >
                    Discover movies similar to
                    your favourite movies using
                    AI-powered recommendations.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # SELECT MOVIE
    # ========================================================

    st.html(
        """
        <div
            style="
                font-size:30px;
                font-weight:900;
                margin-bottom:10px;
            "
        >
            🎬
            <span style="color:white;">
                Choose
            </span>

            <span
                style="
                    background:
                    linear-gradient(
                        90deg,
                        #00aaff,
                        #ff0066
                    );
                    -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent;
                "
            >
                Your Movie
            </span>
        </div>
        """
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
        "Choose movie",
        movie_list,
        index=default_index
    )


    # ========================================================
    # SELECTED MOVIE PREVIEW
    # ========================================================

    selected_indexes = movies[
        movies["title"] == selected_movie
    ].index


    if len(selected_indexes) > 0:

        selected_index = selected_indexes[0]

        selected_id = movies.iloc[
            selected_index
        ]["movie_id"]

        selected_details = fetch_movie_details(
            selected_id
        )


        if selected_details:

            selected_poster = selected_details.get(
                "poster_path"
            )

            selected_overview = selected_details.get(
                "overview",
                "No description available."
            )


            if selected_poster:

                selected_poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + selected_poster
                )


                st.html(
                    f"""
                    <div
                        style="
                            margin-top:20px;
                            margin-bottom:25px;
                            padding:16px;
                            border-radius:14px;

                            background:
                                linear-gradient(
                                    135deg,
                                    rgba(0,110,255,0.10),
                                    rgba(255,0,80,0.10)
                                );

                            border:1px solid transparent;

                            background:
                                linear-gradient(
                                    #080b14,
                                    #080b14
                                ) padding-box,

                                linear-gradient(
                                    90deg,
                                    #006eff,
                                    #7b00ff,
                                    #ff0055
                                ) border-box;

                            box-shadow:
                                0 0 20px
                                rgba(0,110,255,0.18),
                                0 0 25px
                                rgba(255,0,80,0.15);
                        "
                    >

                        <div
                            style="
                                display:flex;
                                align-items:center;
                                gap:18px;
                            "
                        >

                            <img
                                src="{selected_poster_url}"
                                style="
                                    width:120px;
                                    height:175px;
                                    object-fit:cover;
                                    border-radius:9px;
                                    border:1px solid #2477ff;
                                    box-shadow:
                                        0 0 15px
                                        rgba(0,110,255,0.40);
                                "
                            >

                            <div>

                                <div
                                    style="
                                        color:#00aaff;
                                        font-size:13px;
                                        font-weight:800;
                                        margin-bottom:7px;
                                    "
                                >
                                    ⭐ SELECTED MOVIE
                                </div>


                                <div
                                    style="
                                        color:white;
                                        font-size:27px;
                                        font-weight:900;
                                        margin-bottom:8px;
                                    "
                                >
                                    {selected_movie}
                                </div>


                                <div
                                    style="
                                        color:#c0c0c0;
                                        font-size:14px;
                                        line-height:1.55;
                                    "
                                >
                                    {selected_overview}
                                </div>

                            </div>

                        </div>

                    </div>
                    """
                )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    names, posters, ids = recommend(
        selected_movie
    )


    st.divider()


    st.html(
        f"""
        <div class="section-title">

            🔥
            <span
                class="gradient-text"
            >
                Recommended Movies
            </span>

        </div>


        <div class="section-subtitle">

            Because you selected

            <b
                style="
                    color:#00aaff;
                "
            >
                {selected_movie}
            </b>

            <br>

            👆 Tap any poster to open movie details

        </div>
        """
    )


    # ========================================================
    # MOVIE GRID
    # ========================================================

    COLS_PER_ROW = 5


    for row_start in range(
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

            position = (
                row_start + j
            )


            if position >= len(names):

                continue


            with cols[j]:

                movie_html = movie_card_html(
                    names[position],
                    posters[position],
                    ids[position]
                )


                st.html(
                    movie_html
                )


    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()


    st.html(
        """
        <div
            style="
                text-align:center;
                padding:40px 10px;
                color:#777;
            "
        >

            <div class="footer-title">
                🎬 Movie Recommendation System
            </div>


            <div
                style="
                    margin-top:12px;
                    color:#888;
                "
            >
                Developed By
            </div>


            <div
                style="
                    margin-top:8px;
                    color:#cccccc;
                    font-size:16px;
                    font-weight:700;
                "
            >
                Anish Kumar • Abhishek • Vishal
            </div>


            <div
                style="
                    margin-top:15px;
                    color:#555;
                    font-size:12px;
                "
            >
                Machine Learning & Web Application Project
            </div>

        </div>
        """
    )