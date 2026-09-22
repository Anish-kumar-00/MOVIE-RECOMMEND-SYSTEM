import gzip
import os
import pickle
import requests
import html
import streamlit as st
import streamlit.components.v1 as components


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

st.html("""
<style>

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    background: #03030a;
}

.stApp {
    background:
        radial-gradient(
            circle at 0% 20%,
            rgba(0, 75, 255, 0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 100% 30%,
            rgba(255, 0, 60, 0.20),
            transparent 32%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(100, 0, 255, 0.12),
            transparent 35%
        ),
        #03030a;

    color: white;
    overflow-x: hidden;
}

.block-container {
    max-width: 1500px;
    padding-top: 25px;
    padding-bottom: 50px;
}

[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background:
        linear-gradient(
            135deg,
            rgba(0, 20, 50, 0.95),
            rgba(25, 0, 25, 0.95)
        ) !important;

    border: 2px solid #006cff !important;

    border-radius: 12px !important;

    color: white !important;

    box-shadow:
        0 0 10px rgba(0, 110, 255, 0.30),
        0 0 15px rgba(255, 0, 60, 0.20) !important;
}

div[data-baseweb="select"] > div:focus-within {

    border-color: #ff0066 !important;

    box-shadow:
        0 0 15px rgba(0, 140, 255, 0.65),
        0 0 25px rgba(255, 0, 80, 0.35) !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            #006cff,
            #7b00ff,
            #ff003c
        ) !important;

    color: white !important;

    border: 1px solid #ff174f !important;

    border-radius: 10px !important;

    font-weight: 800 !important;

    transition: all 0.3s ease !important;

    box-shadow:
        0 0 12px rgba(0, 110, 255, 0.25),
        0 0 12px rgba(255, 0, 70, 0.20) !important;
}

.stButton > button:hover {

    transform: translateY(-3px);

    box-shadow:
        0 0 18px rgba(0, 110, 255, 0.60),
        0 0 30px rgba(255, 0, 70, 0.50) !important;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {

    border: none !important;

    height: 1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            #006cff,
            #ff0066,
            transparent
        ) !important;

    box-shadow:
        0 0 10px rgba(0, 100, 255, 0.5);
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {

    position: relative;

    min-height: 390px;

    display: flex;

    align-items: flex-end;

    padding: 55px;

    border-radius: 20px;

    overflow: hidden;

    background:

        radial-gradient(
            circle at 75% 45%,
            rgba(0, 100, 255, 0.30),
            transparent 30%
        ),

        radial-gradient(
            circle at 90% 55%,
            rgba(255, 0, 70, 0.28),
            transparent 30%
        ),

        linear-gradient(
            110deg,
            #02030a,
            #080814,
            #11030a
        );

    border: 2px solid transparent;

    background-clip: padding-box;

    box-shadow:
        0 0 15px rgba(0, 110, 255, 0.45),
        0 0 30px rgba(255, 0, 70, 0.30);

    margin-bottom: 40px;

    animation: heroPulse 4s ease-in-out infinite;
}

.hero-box::before {

    content: "";

    position: absolute;

    inset: 0;

    border-radius: 20px;

    padding: 2px;

    background:
        linear-gradient(
            90deg,
            #006cff,
            #00c8ff,
            #9d00ff,
            #ff0066,
            #ff1744,
            #006cff
        );

    background-size: 300% 100%;

    animation: neonBorder 5s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;

    mask-composite: exclude;

    pointer-events: none;
}

.hero-box::after {

    content: "";

    position: absolute;

    width: 450px;

    height: 450px;

    right: -100px;

    top: -120px;

    background:
        radial-gradient(
            circle,
            rgba(0, 100, 255, 0.25),
            transparent 65%
        );

    filter: blur(25px);

    animation: heroLight 5s ease-in-out infinite;
}

@keyframes heroPulse {

    0% {
        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.35),
            0 0 20px rgba(255, 0, 70, 0.20);
    }

    50% {
        box-shadow:
            0 0 30px rgba(0, 110, 255, 0.65),
            0 0 45px rgba(255, 0, 70, 0.45);
    }

    100% {
        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.35),
            0 0 20px rgba(255, 0, 70, 0.20);
    }
}

@keyframes neonBorder {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

@keyframes heroLight {

    0% {
        transform: translateX(0) translateY(0);
    }

    50% {
        transform: translateX(-100px) translateY(50px);
    }

    100% {
        transform: translateX(0) translateY(0);
    }
}

.hero-content {

    position: relative;

    z-index: 5;

    animation: titleFade 1s ease-out;
}

@keyframes titleFade {

    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* ============================================================
   HERO TITLE
   ============================================================ */

.hero-title {

    font-size: clamp(38px, 6vw, 72px);

    font-weight: 950;

    line-height: 0.98;

    margin: 10px 0 20px;

    color: white;

    text-shadow:
        0 0 15px rgba(255,255,255,0.15);
}

.gradient-text {

    background:
        linear-gradient(
            90deg,
            #00aaff,
            #7b00ff,
            #ff0077
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-clip: text;
}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {

    font-size: 32px;

    font-weight: 950;

    margin-top: 15px;

    margin-bottom: 5px;

    background:
        linear-gradient(
            90deg,
            #ffffff 0%,
            #00aaff 35%,
            #9d00ff 65%,
            #ff0066 100%
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-clip: text;
}

.section-subtitle {

    color: #aeb4c5;

    margin-bottom: 25px;

    font-size: 15px;
}


/* ============================================================
   SELECTED MOVIE
   ============================================================ */

.selected-movie-box {

    position: relative;

    display: flex;

    align-items: center;

    gap: 28px;

    padding: 18px;

    min-height: 180px;

    margin-top: 25px;

    margin-bottom: 30px;

    border-radius: 18px;

    background:
        linear-gradient(
            110deg,
            rgba(0, 40, 90, 0.48),
            rgba(25, 5, 50, 0.42),
            rgba(80, 0, 25, 0.45)
        );

    border: 2px solid transparent;

    background-clip: padding-box;

    box-shadow:
        0 0 18px rgba(0, 100, 255, 0.35),
        0 0 30px rgba(255, 0, 70, 0.25);

    overflow: hidden;
}

.selected-movie-box::before {

    content: "";

    position: absolute;

    inset: 0;

    border-radius: 18px;

    padding: 2px;

    background:
        linear-gradient(
            90deg,
            #0077ff,
            #00ccff,
            #9d00ff,
            #ff0066,
            #ff003c,
            #0077ff
        );

    background-size: 300% 100%;

    animation: neonBorder 4s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;

    mask-composite: exclude;

    pointer-events: none;
}

.selected-poster {

    width: 120px;

    height: 175px;

    object-fit: cover;

    border-radius: 12px;

    position: relative;

    z-index: 2;

    box-shadow:
        0 0 12px rgba(0, 110, 255, 0.65),
        0 0 20px rgba(255, 0, 70, 0.35);
}

.selected-info {

    position: relative;

    z-index: 2;
}

.selected-badge {

    display: inline-block;

    padding: 5px 12px;

    border-radius: 50px;

    color: #ffffff;

    font-size: 12px;

    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #006cff,
            #8b00ff,
            #ff0066
        );

    box-shadow:
        0 0 12px rgba(0, 120, 255, 0.45);
}

.selected-title {

    font-size: 32px;

    font-weight: 900;

    margin: 8px 0;
}

.selected-overview {

    color: #c5cad5;

    line-height: 1.6;

    max-width: 750px;
}


/* ============================================================
   MOVIE CARD
   ============================================================ */

.movie-wrapper {

    position: relative;

    background:
        linear-gradient(
            145deg,
            #0d1425,
            #0a0a12
        );

    border: 2px solid transparent;

    border-radius: 14px;

    padding: 5px;

    margin-bottom: 18px;

    overflow: hidden;

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.5);

    z-index: 2;
}

.movie-wrapper::before {

    content: "";

    position: absolute;

    inset: -2px;

    border-radius: 15px;

    padding: 2px;

    background:
        linear-gradient(
            130deg,
            #006cff,
            #00c8ff,
            #7000ff,
            #ff0066,
            #ff1744,
            #006cff
        );

    background-size: 350% 350%;

    animation: cardLightning 3.5s linear infinite;

    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);

    -webkit-mask-composite: xor;

    mask-composite: exclude;

    opacity: 0.95;

    pointer-events: none;
}

@keyframes cardLightning {

    0% {
        background-position: 0% 50%;
    }

    25% {
        background-position: 50% 0%;
    }

    50% {
        background-position: 100% 50%;
    }

    75% {
        background-position: 50% 100%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.movie-wrapper:hover {

    transform:
        translateY(-9px)
        scale(1.035);

    box-shadow:
        0 0 15px rgba(0, 110, 255, 0.65),
        0 0 25px rgba(255, 0, 70, 0.55),
        0 18px 40px rgba(0,0,0,0.75);

    z-index: 50;
}

.movie-poster-container {

    position: relative;

    overflow: hidden;

    border-radius: 9px;

    z-index: 3;
}

.movie-poster {

    width: 100%;

    aspect-ratio: 2 / 3;

    object-fit: cover;

    display: block;

    transition:
        transform 0.55s ease,
        filter 0.55s ease;
}

.movie-wrapper:hover .movie-poster {

    transform: scale(1.08);

    filter:
        brightness(0.48)
        saturate(1.2);
}

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
            rgba(0,0,0,0.88)
        );

    transition: opacity 0.35s ease;
}

.movie-wrapper:hover .movie-overlay {
    opacity: 1;
}

.play-circle {

    width: 60px;

    height: 60px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            #006cff,
            #8b00ff,
            #ff003c
        );

    color: white;

    font-size: 24px;

    box-shadow:
        0 0 15px rgba(0, 110, 255, 0.8),
        0 0 30px rgba(255, 0, 70, 0.65);

    animation: playPulse 1.7s infinite;
}

@keyframes playPulse {

    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(1.08);
    }

    100% {
        transform: scale(1);
    }
}

.movie-title {

    position: relative;

    z-index: 5;

    color: #ffffff;

    font-size: 13px;

    font-weight: 800;

    text-align: center;

    padding: 10px 5px 8px;

    min-height: 43px;

    display: flex;

    align-items: center;

    justify-content: center;
}


/* ============================================================
   TRAILER SECTION
   ============================================================ */

.trailer-section {

    margin-top: 25px;

    width: 100%;

    position: relative;
}

.trailer-heading {

    font-size: 27px;

    font-weight: 900;

    margin-bottom: 15px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #00aaff,
            #9d00ff,
            #ff0066
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    background-clip: text;
}


/*
   Main 16:9 YouTube-style player
*/

.trailer-player {

    width: 100%;

    aspect-ratio: 16 / 9;

    position: relative;

    overflow: hidden;

    border-radius: 18px;

    border: 2px solid transparent;

    background:
        linear-gradient(
            #050510,
            #050510
        ) padding-box,
        linear-gradient(
            90deg,
            #006cff,
            #00c8ff,
            #8b00ff,
            #ff0066,
            #ff1744,
            #006cff
        ) border-box;

    box-shadow:
        0 0 18px rgba(0, 110, 255, 0.50),
        0 0 35px rgba(255, 0, 70, 0.30);

    animation: trailerGlow 4s ease-in-out infinite;
}

.trailer-player iframe {

    position: absolute;

    inset: 0;

    width: 100%;

    height: 100%;

    border: 0;

    display: block;

    border-radius: 16px;
}

@keyframes trailerGlow {

    0% {
        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.40),
            0 0 20px rgba(255, 0, 70, 0.20);
    }

    50% {
        box-shadow:
            0 0 30px rgba(0, 110, 255, 0.70),
            0 0 45px rgba(255, 0, 70, 0.45);
    }

    100% {
        box-shadow:
            0 0 15px rgba(0, 110, 255, 0.40),
            0 0 20px rgba(255, 0, 70, 0.20);
    }
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    position: relative;

    text-align: center;

    padding: 40px 10px;

    margin-top: 20px;

    color: #777;
}

.footer-title {

    font-size: 22px;

    font-weight: 900;

    color: white;
}

.footer-line {

    width: 180px;

    height: 2px;

    margin: 12px auto;

    background:
        linear-gradient(
            90deg,
            #006cff,
            #9d00ff,
            #ff0066
        );

    box-shadow:
        0 0 12px rgba(0, 110, 255, 0.5),
        0 0 12px rgba(255, 0, 70, 0.5);
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .block-container {
        padding-left: 10px;
        padding-right: 10px;
    }

    .hero-box {

        min-height: 300px;

        padding: 28px 24px;

        border-radius: 15px;
    }

    .hero-title {

        font-size: 42px;

        line-height: 1;
    }

    .selected-movie-box {

        gap: 15px;

        padding: 12px;

        min-height: 145px;
    }

    .selected-poster {

        width: 85px;

        height: 125px;
    }

    .selected-title {
        font-size: 24px;
    }

    .selected-overview {

        font-size: 12px;

        line-height: 1.45;

        display: -webkit-box;

        -webkit-line-clamp: 4;

        -webkit-box-orient: vertical;

        overflow: hidden;
    }

    .section-title {
        font-size: 25px;
    }

    .movie-wrapper {

        border-radius: 11px;

        padding: 4px;

        margin-bottom: 12px;
    }

    .movie-wrapper:hover {

        transform:
            translateY(-4px)
            scale(1.015);
    }

    .movie-title {

        font-size: 10px;

        min-height: 36px;

        padding: 7px 3px;
    }

    .play-circle {

        width: 44px;

        height: 44px;

        font-size: 18px;
    }

    .trailer-player {

        border-radius: 12px;
    }

    .trailer-player iframe {

        border-radius: 10px;
    }

    .trailer-heading {
        font-size: 23px;
    }
}

</style>
""")


# ============================================================
# 3. FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

    with open(MOVIES_FILE, "rb") as file:
        movies_data = pickle.load(file)

    with gzip.open(SIMILARITY_FILE, "rb") as file:
        similarity_data = pickle.load(file)

    return (
        movies_data,
        similarity_data["indices"]
    )


movies, similarity_indices = load_data()


# ============================================================
# 5. TMDB API KEY
# ============================================================

try:

    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

except Exception:

    st.error(
        "TMDB_API_KEY is missing from Streamlit Secrets."
    )

    st.stop()


# ============================================================
# 6. TMDB REQUEST
# ============================================================

def tmdb_request(endpoint, params=None):

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
            timeout=15
        )

        if response.status_code == 200:

            return response.json()

    except requests.RequestException:

        return None

    return None


# ============================================================
# 7. MOVIE DETAILS
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_movie_details(movie_id):

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
def fetch_poster(movie_id):

    details = fetch_movie_details(movie_id)

    if not details:
        return None

    poster_path = details.get("poster_path")

    if not poster_path:
        return None

    return (
        "https://image.tmdb.org/t/p/w500"
        + poster_path
    )


# ============================================================
# 9. GET ALL YOUTUBE VIDEOS
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_youtube_videos(movie_id):

    data = tmdb_request(
        f"movie/{movie_id}/videos",
        {
            "language": "en-US"
        }
    )

    if not data:
        return []

    videos = data.get("results", [])

    youtube_videos = []

    for video in videos:

        if video.get("site") != "YouTube":
            continue

        key = video.get("key")

        if not key:
            continue

        youtube_videos.append({
            "key": key,
            "name": video.get("name", ""),
            "type": video.get("type", ""),
            "official": video.get("official", False),
            "published_at": video.get("published_at", "")
        })

    return youtube_videos


# ============================================================
# 10. FIND BEST TRAILER
# ============================================================

def get_best_trailer(movie_id):

    videos = fetch_youtube_videos(movie_id)

    if not videos:
        return None


    # --------------------------------------------------------
    # 1. Official Trailer
    # --------------------------------------------------------

    for video in videos:

        if (
            video["type"] == "Trailer"
            and video["official"] is True
        ):

            return video


    # --------------------------------------------------------
    # 2. Any Trailer
    # --------------------------------------------------------

    for video in videos:

        if video["type"] == "Trailer":

            return video


    # --------------------------------------------------------
    # 3. Teaser
    # --------------------------------------------------------

    for video in videos:

        if video["type"] == "Teaser":

            return video


    # --------------------------------------------------------
    # 4. Clip
    # --------------------------------------------------------

    for video in videos:

        if video["type"] == "Clip":

            return video


    return videos[0]


# ============================================================
# 11. YOUTUBE EMBED PLAYER
# ============================================================

def show_youtube_trailer(movie_id):

    trailer = get_best_trailer(movie_id)

    if not trailer:

        st.info(
            "🎬 Trailer not available for this movie."
        )

        return


    youtube_key = trailer["key"]

    video_name = html.escape(
        trailer.get("name", "Movie Trailer")
    )


    # --------------------------------------------------------
    # YOUTUBE NO-COOKIE EMBED
    # --------------------------------------------------------

    embed_url = (
        "https://www.youtube-nocookie.com/embed/"
        + youtube_key
        + "?rel=0"
        + "&modestbranding=1"
        + "&playsinline=1"
        + "&controls=1"
        + "&fs=1"
        + "&iv_load_policy=3"
    )


    # --------------------------------------------------------
    # HEADING
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="trailer-section">

            <div class="trailer-heading">
                ▶️ Trailer
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # ACTUAL YOUTUBE PLAYER
    # --------------------------------------------------------

    iframe_html = f"""
    <div class="trailer-player">

        <iframe
            src="{embed_url}"
            title="{video_name}"
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
    """


    components.html(
        iframe_html,
        height=0,
        scrolling=False
    )


    # --------------------------------------------------------
    # FALLBACK DIRECT STREAMLIT PLAYER
    # --------------------------------------------------------

    # A normal Streamlit player is also placed below only as
    # a fallback option if YouTube iframe doesn't load.
    #
    # User can click the direct YouTube link.

    youtube_watch_url = (
        "https://www.youtube.com/watch?v="
        + youtube_key
    )


    st.html(
        f"""
        <div
            style="
                margin-top:12px;
                text-align:center;
                color:#888;
                font-size:12px;
            "
        >
            🎬 {video_name}
        </div>

        <div
            style="
                margin-top:8px;
                text-align:center;
            "
        >
            <a
                href="{youtube_watch_url}"
                target="_blank"
                style="
                    display:inline-block;
                    padding:8px 18px;
                    border-radius:30px;
                    text-decoration:none;
                    color:white;
                    font-weight:800;
                    background:
                        linear-gradient(
                            90deg,
                            #006cff,
                            #8b00ff,
                            #ff0066
                        );
                    box-shadow:
                        0 0 15px
                        rgba(0,110,255,0.45);
                "
            >
                ▶ Open Trailer on YouTube
            </a>
        </div>
        """
    )


# ============================================================
# 12. RECOMMENDATION
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

    similar_movies = similarity_indices[index][0:20]

    for movie_index in similar_movies:

        try:
            movie_index = int(movie_index)

        except Exception:
            continue

        try:

            movie_id = movies.iloc[
                movie_index
            ]["movie_id"]

            movie_name = movies.iloc[
                movie_index
            ]["title"]

        except Exception:
            continue

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
# 13. MOVIE CARD
# ============================================================

def movie_card_html(
    movie_name,
    poster_url,
    movie_id
):

    safe_name = html.escape(
        str(movie_name)
    )

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
                    alt="{safe_name}"
                    loading="lazy"
                >

                <div class="movie-overlay">

                    <div class="play-circle">
                        ▶
                    </div>

                </div>

            </div>

            <div class="movie-title">
                {safe_name}
            </div>

        </div>

    </a>
    """


# ============================================================
# 14. SELECTED MOVIE PREVIEW
# ============================================================

def selected_movie_preview(movie_name):

    indexes = movies[
        movies["title"] == movie_name
    ].index

    if len(indexes) == 0:
        return

    index = indexes[0]

    try:

        movie_id = movies.iloc[
            index
        ]["movie_id"]

    except Exception:

        return

    details = fetch_movie_details(movie_id)

    if not details:
        return

    poster_path = details.get(
        "poster_path"
    )

    overview = details.get(
        "overview",
        "No description available."
    )

    safe_title = html.escape(
        str(
            details.get(
                "title",
                movie_name
            )
        )
    )

    safe_overview = html.escape(
        str(overview)
    )

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

    else:

        poster_url = (
            "https://via.placeholder.com/"
            "500x750?text=No+Poster"
        )

    st.html(
        f"""
        <div class="selected-movie-box">

            <img
                class="selected-poster"
                src="{poster_url}"
                alt="{safe_title}"
            >

            <div class="selected-info">

                <span class="selected-badge">
                    ⭐ Selected Movie
                </span>

                <div class="selected-title">
                    {safe_title}
                </div>

                <div class="selected-overview">
                    {safe_overview}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# 15. DETAILS PAGE
# ============================================================

def show_movie_details(movie_id):

    if st.button(
        "← Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


    st.divider()


    details = fetch_movie_details(movie_id)

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
                style="
                    width:100%;
                    height:420px;
                    border-radius:18px;

                    background-image:

                        linear-gradient(
                            to top,
                            #03030a 0%,
                            rgba(3,3,10,0.10) 80%
                        ),

                        url('{backdrop_url}');

                    background-size:cover;

                    background-position:center;

                    border:2px solid #222;

                    box-shadow:
                        0 0 20px
                        rgba(0,110,255,0.25),

                        0 0 25px
                        rgba(255,0,70,0.20);
                "
            >
            </div>
            """
        )


    st.title(
        "🎬 " + title
    )


    # ========================================================
    # POSTER + BASIC INFO
    # ========================================================

    poster_col, info_col = st.columns(
        [1, 2],
        gap="large"
    )


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


    with info_col:

        st.subheader("⭐ Rating")

        st.metric(
            "TMDB Rating",
            f"{rating:.1f}/10"
        )

        st.divider()

        st.subheader("📅 Release Date")

        st.write(
            release_date
        )


        if runtime:

            st.divider()

            hours = runtime // 60

            minutes = runtime % 60

            if hours:

                runtime_text = (
                    f"{hours}h {minutes}min"
                )

            else:

                runtime_text = (
                    f"{minutes}min"
                )

            st.subheader("⏱️ Runtime")

            st.write(
                runtime_text
            )


        if genres:

            st.divider()

            st.subheader("🎭 Genres")

            genre_names = []

            for genre in genres:

                name = genre.get("name")

                if name:

                    genre_names.append(name)

            st.write(
                " • ".join(genre_names)
            )


        st.divider()

        st.subheader("📝 Story")

        st.write(
            overview
        )


    # ========================================================
    # TRAILER
    # ========================================================

    st.divider()

    show_youtube_trailer(movie_id)


# ============================================================
# 16. QUERY PARAMETER
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 17. DETAILS PAGE
# ============================================================

if movie_id_from_url:

    try:

        movie_id = int(
            movie_id_from_url
        )

        show_movie_details(
            movie_id
        )

    except (ValueError, TypeError):

        st.error(
            "Invalid movie ID."
        )


# ============================================================
# 18. MAIN PAGE
# ============================================================

else:

    # ========================================================
    # HERO
    # ========================================================

    st.html(
        """
        <div class="hero-box">

            <div class="hero-content">

                <div
                    style="
                        color:#ff1744;
                        font-size:13px;
                        font-weight:900;
                        letter-spacing:3px;
                    "
                >
                    🎬 DEVELOPED BY
                    ANISH-ABRAR-ABHISHEK-VISHAL
                </div>

                <div class="hero-title">

                    Movie

                    <br>

                    <span class="gradient-text">
                        Recommendation
                    </span>

                    <br>

                    System

                </div>

                <div
                    style="
                        color:#c5cad5;
                        font-size:17px;
                        line-height:1.6;
                        max-width:650px;
                    "
                >
                    Discover movies similar to your
                    favourite movies using
                    AI-powered recommendations.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # CHOOSE MOVIE
    # ========================================================

    st.html(
        """
        <div
            style="
                font-size:32px;
                font-weight:900;
                margin-bottom:8px;
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
                        #9d00ff,
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


    movie_list = (
        movies["title"]
        .dropna()
        .values
    )


    default_index = 0


    if "Avatar" in movie_list:

        default_index = list(
            movie_list
        ).index("Avatar")


    selected_movie = st.selectbox(
        "Choose movie",
        movie_list,
        index=default_index,
        key="movie_selector"
    )


    # ========================================================
    # SELECTED MOVIE
    # ========================================================

    selected_movie_preview(
        selected_movie
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    names, posters, ids = recommend(
        selected_movie
    )


    st.html(
        f"""
        <div class="section-title">
            🔥 Recommended Movies
        </div>

        <div class="section-subtitle">

            Because you selected

            <strong
                style="
                    color:#00aaff;
                    text-shadow:
                        0 0 8px
                        rgba(0,170,255,0.6);
                "
            >
                {html.escape(str(selected_movie))}
            </strong>

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


        for j in range(COLS_PER_ROW):

            position = (
                row_start + j
            )


            if position >= len(names):
                continue


            with cols[j]:

                st.html(
                    movie_card_html(
                        names[position],
                        posters[position],
                        ids[position]
                    )
                )


    # ========================================================
    # FOOTER
    # ========================================================

    st.html(
        """
        <div class="footer">

            <div class="footer-line"></div>

            <div class="footer-title">

                🎬 Movie Recommendation System

            </div>

            <div
                style="
                    margin-top:10px;
                    color:#888;
                "
            >
                Developed By
            </div>

            <div
                style="
                    margin-top:8px;
                    color:#ffffff;
                    font-size:16px;
                    font-weight:800;
                "
            >
                Anish Kumar • Abhishek • Vishal
            </div>

            <div
                style="
                    margin-top:12px;
                    color:#555;
                    font-size:12px;
                "
            >
                Machine Learning &
                Web Application Project
            </div>

        </div>
        """
    )