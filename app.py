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
                rgba(0, 90, 255, 0.18),
                transparent 28%
            ),
            radial-gradient(
                circle at 95% 20%,
                rgba(255, 0, 80, 0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(100, 0, 255, 0.12),
                transparent 35%
            ),
            #03050b;

        color: white;
    }


    /* =====================================================
       MAIN CONTAINER
       ===================================================== */

    .block-container {
        max-width: 1500px !important;

        padding-top: 25px !important;
        padding-bottom: 50px !important;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {

        background:
            linear-gradient(
                100deg,
                rgba(0, 60, 150, 0.25),
                rgba(180, 0, 80, 0.20)
            ) !important;

        border: 1px solid
            #168cff !important;

        border-radius: 10px !important;

        color: white !important;

        box-shadow:
            0 0 15px
            rgba(0, 110, 255, 0.25),
            inset 0 0 12px
            rgba(255, 0, 80, 0.08);
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {

        background:
            linear-gradient(
                90deg,
                #006eff,
                #7b00ff,
                #ff0055
            ) !important;

        color: white !important;

        border: 1px solid
            rgba(255,255,255,0.25) !important;

        border-radius: 9px !important;

        font-weight: 800 !important;

        transition:
            all 0.3s ease !important;

        box-shadow:
            0 0 15px
            rgba(0, 110, 255, 0.25);
    }


    .stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0 0 25px
            rgba(0, 120, 255, 0.55),
            0 0 35px
            rgba(255, 0, 80, 0.25) !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {

        border: none !important;

        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                #006eff,
                #ff0066,
                transparent
            ) !important;

        margin-top: 28px !important;

        margin-bottom: 28px !important;
    }


    /* =====================================================
       HERO
       ===================================================== */

    @keyframes heroGlow {

        0% {
            box-shadow:
                0 0 15px
                rgba(0,110,255,0.25),
                0 0 25px
                rgba(255,0,80,0.10);
        }

        50% {
            box-shadow:
                0 0 35px
                rgba(0,110,255,0.55),
                0 0 50px
                rgba(255,0,80,0.35);
        }

        100% {
            box-shadow:
                0 0 15px
                rgba(0,110,255,0.25),
                0 0 25px
                rgba(255,0,80,0.10);
        }

    }


    .hero-box {

        animation:
            heroGlow 3s
            ease-in-out
            infinite;

        border:
            2px solid transparent;

        border-image:
            linear-gradient(
                90deg,
                #006eff,
                #8a00ff,
                #ff0055
            ) 1;

        position: relative;

        overflow: hidden;
    }


    /* =====================================================
       TITLE ANIMATION
       ===================================================== */

    @keyframes titleFade {

        0% {
            opacity: 0;

            transform:
                translateY(20px);
        }

        100% {
            opacity: 1;

            transform:
                translateY(0);
        }

    }


    .hero-content {

        animation:
            titleFade 1s
            ease-out;
    }


    /* =====================================================
       SECTION TITLE
       ===================================================== */

    .section-title {

        font-size: 32px;

        font-weight: 900;

        margin-top: 25px;

        margin-bottom: 5px;

        background:
            linear-gradient(
                90deg,
                #00aaff,
                #7c00ff,
                #ff0055
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color:
            transparent;
    }


    .section-subtitle {

        color: #aaaaaa;

        margin-bottom: 25px;
    }


    /* =====================================================
       MOVIE CARD
       ===================================================== */

    .movie-wrapper {

        position: relative;

        background:
            linear-gradient(
                145deg,
                rgba(15,25,45,0.95),
                rgba(20,5,20,0.95)
            );

        border:
            2px solid transparent;

        border-radius: 13px;

        padding: 6px;

        margin-bottom: 22px;

        overflow: hidden;

        transition:
            transform 0.35s ease,
            box-shadow 0.35s ease;

        box-shadow:
            0 8px 25px
            rgba(0,0,0,0.5);

        background-clip:
            padding-box;

        isolation: isolate;
    }


    /* =====================================================
       NEON BORDER
       ===================================================== */

    .movie-wrapper::before {

        content: "";

        position: absolute;

        inset: -3px;

        border-radius: 15px;

        background:
            linear-gradient(
                90deg,
                #006eff,
                #00d4ff,
                #7200ff,
                #ff0055,
                #ff0033,
                #006eff
            );

        background-size:
            400% 400%;

        animation:
            neonBorder 4s
            linear
            infinite;

        z-index: -2;

        opacity: 0.9;
    }


    .movie-wrapper::after {

        content: "";

        position: absolute;

        inset: 2px;

        border-radius: 10px;

        background:
            linear-gradient(
                145deg,
                #101522,
                #10070f
            );

        z-index: -1;
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
            0 0 18px
            rgba(0,110,255,0.75),
            0 0 35px
            rgba(255,0,90,0.45);

        z-index: 20;
    }


    /* =====================================================
       POSTER
       ===================================================== */

    .movie-poster-container {

        position: relative;

        overflow: hidden;

        border-radius: 8px;

        z-index: 1;
    }


    .movie-poster {

        width: 100%;

        aspect-ratio: 2 / 3;

        object-fit: cover;

        display: block;

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
       MOVIE OVERLAY
       ===================================================== */

    .movie-overlay {

        position: absolute;

        inset: 0;

        display: flex;

        align-items: center;

        justify-content: center;

        opacity: 0;

        background:
            linear-gradient(
                to bottom,
                rgba(0,0,0,0.05),
                rgba(0,0,0,0.85)
            );

        transition:
            opacity 0.35s ease;
    }


    .movie-wrapper:hover
    .movie-overlay {

        opacity: 1;
    }


    /* =====================================================
       PLAY BUTTON
       ===================================================== */

    .play-circle {

        width: 58px;

        height: 58px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                #006eff,
                #ff0055
            );

        color: white;

        font-size: 23px;

        box-shadow:
            0 0 25px
            rgba(0,110,255,0.65);

        animation:
            playPulse 1.7s
            infinite;
    }


    @keyframes playPulse {

        0% {
            box-shadow:
                0 0 0 0
                rgba(0,110,255,0.6);
        }

        70% {
            box-shadow:
                0 0 0 14px
                rgba(255,0,80,0);
        }

        100% {
            box-shadow:
                0 0 0 0
                rgba(255,0,80,0);
        }

    }


    /* =====================================================
       MOVIE TITLE
       ===================================================== */

    .movie-title {

        position: relative;

        z-index: 2;

        color: white;

        font-size: 13px;

        font-weight: 700;

        text-align: center;

        padding:
            10px 5px 7px;

        min-height: 42px;

        display: flex;

        align-items: center;

        justify-content: center;
    }


    /* =====================================================
       SELECTED MOVIE BOX
       ===================================================== */

    .selected-movie-box {

        display: flex;

        align-items: center;

        gap: 25px;

        padding: 18px;

        margin-top: 20px;

        margin-bottom: 20px;

        border-radius: 15px;

        background:
            linear-gradient(
                100deg,
                rgba(0,50,120,0.28),
                rgba(70,0,100,0.20),
                rgba(120,0,50,0.25)
            );

        border:
            2px solid transparent;

        background-clip:
            padding-box;

        position: relative;

        box-shadow:
            0 0 25px
            rgba(0,100,255,0.18);
    }


    .selected-movie-box::before {

        content: "";

        position: absolute;

        inset: -2px;

        border-radius: 15px;

        padding: 2px;

        background:
            linear-gradient(
                90deg,
                #006eff,
                #8a00ff,
                #ff0055
            );

        -webkit-mask:
            linear-gradient(#fff 0 0)
            content-box,
            linear-gradient(#fff 0 0);

        -webkit-mask-composite:
            xor;

        mask-composite: exclude;

        pointer-events: none;
    }


    .selected-poster {

        width: 130px;

        height: 195px;

        object-fit: cover;

        border-radius: 10px;

        box-shadow:
            0 0 20px
            rgba(0,110,255,0.5);
    }


    /* =====================================================
       DETAILS HERO
       ===================================================== */

    .details-backdrop {

        width: 100%;

        height: 420px;

        border-radius: 16px;

        background-size: cover;

        background-position: center;

        border:
            2px solid transparent;

        border-image:
            linear-gradient(
                90deg,
                #006eff,
                #7c00ff,
                #ff0055
            ) 1;

        box-shadow:
            0 0 25px
            rgba(0,110,255,0.25),
            0 0 40px
            rgba(255,0,80,0.15);

        margin-bottom: 25px;
    }


    /* =====================================================
       DETAIL INFO
       ===================================================== */

    .detail-item {

        padding: 18px;

        margin-bottom: 12px;

        border-left:
            3px solid #008cff;

        border-right:
            2px solid #ff0055;

        background:
            linear-gradient(
                90deg,
                rgba(0,100,255,0.08),
                rgba(255,0,80,0.08)
            );

        border-radius: 8px;

        box-shadow:
            0 0 12px
            rgba(0,100,255,0.08);
    }


    /* =====================================================
       TRAILER SECTION
       ===================================================== */

    .trailer-title {

        font-size: 28px;

        font-weight: 900;

        background:
            linear-gradient(
                90deg,
                #00aaff,
                #7c00ff,
                #ff0055
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;

        margin-bottom: 15px;
    }


    /* =====================================================
       YOUTUBE PLAYER
       ===================================================== */

    .youtube-container {

        position: relative;

        width: 100%;

        aspect-ratio: 16 / 9;

        overflow: hidden;

        border-radius: 16px;

        background: #000;

        border: 2px solid transparent;

        box-shadow:
            0 0 20px
            rgba(0,110,255,0.55),
            0 0 45px
            rgba(255,0,80,0.28);

        background-clip:
            padding-box;

        margin-top: 15px;

        margin-bottom: 25px;
    }


    .youtube-container::before {

        content: "";

        position: absolute;

        inset: -2px;

        border-radius: 17px;

        background:
            linear-gradient(
                90deg,
                #006eff,
                #00d4ff,
                #7c00ff,
                #ff0055,
                #006eff
            );

        background-size:
            400% 400%;

        animation:
            youtubeGlow 4s
            linear
            infinite;

        z-index: -1;
    }


    @keyframes youtubeGlow {

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


    .youtube-container iframe {

        position: absolute;

        top: 0;

        left: 0;

        width: 100%;

        height: 100%;

        border: 0;

        border-radius: 14px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding-left: 12px !important;

            padding-right: 12px !important;
        }


        .movie-wrapper {

            margin-bottom: 15px;

            padding: 5px;
        }


        .movie-wrapper:hover {

            transform:
                translateY(-3px)
                scale(1.01);
        }


        .movie-title {

            font-size: 11px;

            min-height: 38px;
        }


        .section-title {

            font-size: 25px;
        }


        .hero-box {

            min-height: 300px !important;

            padding: 28px !important;
        }


        .selected-movie-box {

            gap: 15px;

            padding: 12px;
        }


        .selected-poster {

            width: 100px;

            height: 150px;
        }


        .details-backdrop {

            height: 250px;
        }


        .youtube-container {

            aspect-ratio: 16 / 9;

            border-radius: 12px;
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
# 9. TRAILER KEY
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_trailer_key(
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


    # --------------------------------------------------------
    # OFFICIAL YOUTUBE TRAILER
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # ANY YOUTUBE TRAILER
    # --------------------------------------------------------

    for video in videos:

        if (
            video.get("site") == "YouTube"
            and
            video.get("type") == "Trailer"
        ):

            key = video.get("key")

            if key:

                return key


    # --------------------------------------------------------
    # ANY YOUTUBE VIDEO
    # --------------------------------------------------------

    for video in videos:

        if (
            video.get("site") == "YouTube"
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
# 12. YOUTUBE PLAYER
# ============================================================

def youtube_player(
    video_key
):

    if not video_key:

        return

    embed_url = (
        "https://www.youtube.com/embed/"
        + str(video_key)
        + "?rel=0"
        + "&modestbranding=1"
        + "&playsinline=1"
        + "&controls=1"
        + "&fs=1"
    )

    st.html(
        f"""
        <div class="youtube-container">

            <iframe
                src="{embed_url}"
                title="Movie Trailer"
                allow="
                    accelerometer;
                    autoplay;
                    clipboard-write;
                    encrypted-media;
                    gyroscope;
                    picture-in-picture;
                    web-share;
                    fullscreen
                "
                allowfullscreen>
            </iframe>

        </div>
        """
    )


# ============================================================
# 13. DETAILS PAGE
# ============================================================

def show_movie_details(
    movie_id
):

    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    if st.button(
        "← Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # GET DETAILS
    # --------------------------------------------------------

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
    # BACKDROP
    # ========================================================

    if backdrop_path:

        backdrop_url = (
            "https://image.tmdb.org/t/p/original"
            + backdrop_path
        )

        st.html(
            f"""
            <div
                class="details-backdrop"
                style="
                    background-image:
                        linear-gradient(
                            to top,
                            #03050b 0%,
                            rgba(3,5,11,0.15) 75%
                        ),
                        url('{backdrop_url}');
                "
            >
            </div>
            """
        )


    # ========================================================
    # TITLE
    # ========================================================

    st.title(
        "🎬 " + title
    )


    # ========================================================
    # POSTER + INFORMATION
    # ========================================================

    poster_col, info_col = st.columns(
        [1, 2],
        gap="large"
    )


    # ========================================================
    # POSTER
    # ========================================================

    with poster_col:

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

    with info_col:

        # ----------------------------------------------------
        # RATING
        # ----------------------------------------------------

        st.html(
            f"""
            <div class="detail-item">

                <div
                    style="
                        font-size:21px;
                        font-weight:800;
                    "
                >
                    ⭐ Rating
                </div>

                <div
                    style="
                        color:#ffd700;
                        font-size:28px;
                        font-weight:900;
                        margin-top:5px;
                    "
                >
                    {rating:.1f}/10
                </div>

                <div
                    style="
                        color:#777;
                        font-size:11px;
                    "
                >
                    TMDB Rating
                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # RELEASE DATE
        # ----------------------------------------------------

        st.html(
            f"""
            <div class="detail-item">

                <div
                    style="
                        font-size:20px;
                        font-weight:800;
                    "
                >
                    📅 Release Date
                </div>

                <div
                    style="
                        color:#dddddd;
                        margin-top:7px;
                    "
                >
                    {release_date}
                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # RUNTIME
        # ----------------------------------------------------

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

            st.html(
                f"""
                <div class="detail-item">

                    <div
                        style="
                            font-size:20px;
                            font-weight:800;
                        "
                    >
                        ⏱️ Runtime
                    </div>

                    <div
                        style="
                            color:#dddddd;
                            margin-top:7px;
                        "
                    >
                        {runtime_text}
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # GENRES
        # ----------------------------------------------------

        if genres:

            genre_names = []

            for genre in genres:

                name = genre.get(
                    "name"
                )

                if name:

                    genre_names.append(
                        name
                    )

            st.html(
                f"""
                <div class="detail-item">

                    <div
                        style="
                            font-size:20px;
                            font-weight:800;
                        "
                    >
                        🎭 Genres
                    </div>

                    <div
                        style="
                            color:#dddddd;
                            margin-top:7px;
                        "
                    >
                        {" • ".join(genre_names)}
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # STORY
        # ----------------------------------------------------

        st.html(
            f"""
            <div class="detail-item">

                <div
                    style="
                        font-size:20px;
                        font-weight:800;
                    "
                >
                    📝 Story
                </div>

                <div
                    style="
                        color:#cccccc;
                        line-height:1.7;
                        margin-top:8px;
                    "
                >
                    {overview}
                </div>

            </div>
            """
        )


    # ========================================================
    # TRAILER
    # ========================================================

    st.divider()


    st.html(
        """
        <div class="trailer-title">
            ▶️ Trailer
        </div>

        <div
            style="
                color:#999;
                margin-bottom:8px;
                font-size:14px;
            "
        >
            Watch the official movie trailer
        </div>
        """
    )


    # --------------------------------------------------------
    # GET YOUTUBE VIDEO KEY
    # --------------------------------------------------------

    trailer_key = fetch_trailer_key(
        movie_id
    )


    if trailer_key:

        youtube_player(
            trailer_key
        )

    else:

        st.info(
            "Trailer not available for this movie."
        )


# ============================================================
# 14. CHECK MOVIE ID
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 15. DETAILS PAGE
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
# 16. MAIN PAGE
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
                    linear-gradient(
                        90deg,
                        rgba(0,10,25,0.98),
                        rgba(5,5,15,0.82),
                        rgba(30,0,20,0.55)
                    );

                margin-bottom:40px;
            "
        >

            <div
                class="hero-content"
            >

                <div
                    style="
                        color:#ff0055;

                        font-size:14px;

                        font-weight:900;

                        letter-spacing:4px;

                        margin-bottom:12px;
                    "
                >
                    DEVELOPED BY
                    ANISH • ABRAR • ABHISHEK • VISHAL
                </div>


                <div
                    style="
                        font-size:
                            clamp(
                                36px,
                                6vw,
                                68px
                            );

                        font-weight:900;

                        line-height:1.05;

                        margin-bottom:18px;

                        background:
                            linear-gradient(
                                90deg,
                                #ffffff,
                                #00aaff,
                                #9b00ff,
                                #ff0055
                            );

                        -webkit-background-clip:
                            text;

                        -webkit-text-fill-color:
                            transparent;
                    "
                >
                    Movie Recommendation
                    System
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
                margin-bottom:5px;
            "
        >
            🎬
            <span
                style="
                    background:
                        linear-gradient(
                            90deg,
                            #00aaff,
                            #8a00ff,
                            #ff0055
                        );
                    -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent;
                "
            >
                Choose Your Movie
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

        selected_poster = fetch_poster(
            selected_id
        )

        selected_details = fetch_movie_details(
            selected_id
        )


        if selected_details:

            selected_overview = selected_details.get(
                "overview",
                "No description available."
            )

        else:

            selected_overview = (
                "No description available."
            )


        if selected_poster:

            st.html(
                f"""
                <div class="selected-movie-box">

                    <img
                        class="selected-poster"
                        src="{selected_poster}"
                    >

                    <div>

                        <div
                            style="
                                display:inline-block;
                                padding:5px 10px;
                                border-radius:20px;
                                background:
                                    linear-gradient(
                                        90deg,
                                        #006eff,
                                        #7c00ff
                                    );
                                font-size:12px;
                                font-weight:800;
                                margin-bottom:8px;
                            "
                        >
                            ⭐ Selected Movie
                        </div>

                        <div
                            style="
                                font-size:30px;
                                font-weight:900;
                                margin-bottom:8px;
                            "
                        >
                            {selected_movie}
                        </div>

                        <div
                            style="
                                color:#cccccc;
                                line-height:1.6;
                                max-width:700px;
                            "
                        >
                            {selected_overview}
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
            🔥 Recommended Movies
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

            <div
                style="
                    font-size:22px;

                    font-weight:900;

                    background:
                        linear-gradient(
                            90deg,
                            #00aaff,
                            #8a00ff,
                            #ff0055
                        );

                    -webkit-background-clip:text;

                    -webkit-text-fill-color:
                        transparent;
                "
            >
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