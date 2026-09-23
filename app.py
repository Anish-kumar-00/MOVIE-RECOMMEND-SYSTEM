import gzip
import os
import pickle
import html
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

st.html("""
<style>

* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    padding: 0;
    background: #000;
}

body {
    overflow-x: hidden;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(229, 9, 20, 0.10),
            transparent 35%
        ),
        linear-gradient(
            180deg,
            #000000 0%,
            #050505 45%,
            #000000 100%
        );

    color: white;
}

[data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
}

.main .block-container {
    position: relative;
    z-index: 5;
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   HIDE STREAMLIT UI
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   BUTTERFLY FIELD
   ============================================================ */

.butterfly-field {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}

.butterfly {
    position: absolute;
    width: 52px;
    height: 44px;
    opacity: 0.28;
    filter: blur(1.5px);
    transform-origin: center;

    animation:
        butterfly-fly 28s linear infinite,
        butterfly-float 3s ease-in-out infinite;
}

.butterfly .wing {
    position: absolute;
    top: 7px;
    width: 25px;
    height: 32px;

    border-radius:
        75% 25% 65% 35%;

    transform-origin: 100% 70%;

    animation:
        wing-flap 0.85s ease-in-out infinite;
}

.butterfly .left {
    left: 1px;
    transform: rotate(-25deg);
}

.butterfly .right {
    right: 1px;

    transform:
        scaleX(-1)
        rotate(-25deg);
}

.butterfly .body {
    position: absolute;

    width: 7px;
    height: 29px;

    left: 23px;
    top: 9px;

    background:
        rgba(255,255,255,0.65);

    border-radius: 50%;

    filter: blur(1px);

    z-index: 3;
}


/* ============================================================
   BUTTERFLY COLORS
   ============================================================ */

.b1 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(0, 210, 255, 0.95),
            rgba(0, 100, 255, 0.40) 45%,
            rgba(0, 80, 255, 0.02) 75%
        );
}

.b2 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(180, 80, 255, 0.95),
            rgba(110, 30, 255, 0.40) 45%,
            rgba(90, 0, 255, 0.02) 75%
        );
}

.b3 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(255, 70, 180, 0.95),
            rgba(255, 0, 120, 0.40) 45%,
            rgba(255, 0, 120, 0.02) 75%
        );
}

.b4 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(80, 255, 230, 0.90),
            rgba(0, 180, 200, 0.35) 45%,
            rgba(0, 180, 200, 0.02) 75%
        );
}

.b5 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(255, 90, 160, 0.90),
            rgba(230, 20, 80, 0.35) 45%,
            rgba(230, 20, 80, 0.02) 75%
        );
}

.b6 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(120, 150, 255, 0.95),
            rgba(50, 70, 230, 0.35) 45%,
            rgba(50, 70, 230, 0.02) 75%
        );
}

.b7 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(255, 180, 100, 0.75),
            rgba(255, 70, 40, 0.30) 45%,
            rgba(255, 50, 20, 0.02) 75%
        );
}

.b8 .wing {
    background:
        radial-gradient(
            circle at 35% 40%,
            rgba(220, 100, 255, 0.90),
            rgba(150, 20, 220, 0.35) 45%,
            rgba(150, 20, 220, 0.02) 75%
        );
}


/* ============================================================
   BUTTERFLY POSITIONS
   ============================================================ */

.b1 {
    left: -8%;
    top: 18%;
    animation-duration: 28s, 3s;
    animation-delay: -4s, 0s;
}

.b2 {
    left: 12%;
    top: 65%;
    animation-duration: 31s, 3.5s;
    animation-delay: -16s, -1s;
}

.b3 {
    left: 35%;
    top: 10%;
    animation-duration: 24s, 2.8s;
    animation-delay: -8s, -0.5s;
}

.b4 {
    left: 65%;
    top: 72%;
    animation-duration: 34s, 3.8s;
    animation-delay: -20s, -1.5s;
}

.b5 {
    left: 80%;
    top: 20%;
    animation-duration: 29s, 3.2s;
    animation-delay: -13s, -2s;
}

.b6 {
    left: 92%;
    top: 55%;
    animation-duration: 27s, 3.6s;
    animation-delay: -5s, -1s;
}

.b7 {
    left: 48%;
    top: 88%;
    animation-duration: 32s, 4s;
    animation-delay: -25s, -2s;
}

.b8 {
    left: 25%;
    top: 38%;
    animation-duration: 30s, 3.3s;
    animation-delay: -18s, -1s;
}


/* ============================================================
   ANIMATIONS
   ============================================================ */

@keyframes wing-flap {

    0%, 100% {
        transform:
            rotateY(0deg)
            rotate(-25deg);
    }

    50% {
        transform:
            rotateY(65deg)
            rotate(-25deg);
    }
}

@keyframes butterfly-float {

    0%, 100% {
        margin-top: 0;
        margin-left: 0;
    }

    25% {
        margin-top: -25px;
        margin-left: 35px;
    }

    50% {
        margin-top: 15px;
        margin-left: -25px;
    }

    75% {
        margin-top: -18px;
        margin-left: 20px;
    }
}

@keyframes butterfly-fly {

    0% {
        transform:
            translate(-10vw, 10vh)
            rotate(10deg)
            scale(0.8);
    }

    20% {
        transform:
            translate(15vw, -8vh)
            rotate(-8deg)
            scale(1);
    }

    40% {
        transform:
            translate(38vw, 12vh)
            rotate(12deg)
            scale(0.9);
    }

    60% {
        transform:
            translate(58vw, -10vh)
            rotate(-12deg)
            scale(1.1);
    }

    80% {
        transform:
            translate(80vw, 15vh)
            rotate(8deg)
            scale(0.85);
    }

    100% {
        transform:
            translate(115vw, -5vh)
            rotate(-8deg)
            scale(0.75);
    }
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;

    margin-top: 10px;
    margin-bottom: 35px;

    padding: 75px 35px;

    border-radius: 22px;

    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,0.98),
            rgba(0,0,0,0.92),
            rgba(20,0,0,0.75)
        );

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.7);
}

.hero::before {
    content: "";

    position: absolute;

    width: 450px;
    height: 450px;

    right: -150px;
    top: -170px;

    background:
        radial-gradient(
            circle,
            rgba(229,9,20,0.30),
            transparent 65%
        );

    filter: blur(20px);
}

.hero::after {
    content: "";

    position: absolute;

    left: 0;
    bottom: 0;

    width: 180px;
    height: 4px;

    background: #e50914;

    box-shadow:
        0 0 20px rgba(229,9,20,0.7);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-block;

    margin-bottom: 18px;

    padding: 7px 13px;

    border-radius: 30px;

    background:
        rgba(229,9,20,0.12);

    border:
        1px solid rgba(229,9,20,0.35);

    color: #ff5a62;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1.5px;
}

.hero-title {
    margin: 0;

    font-size:
        clamp(35px, 5vw, 68px);

    font-weight: 900;

    letter-spacing: -2px;

    color: white;
}

.hero-title span {
    color: #e50914;
}

.hero-subtitle {
    margin-top: 15px;

    max-width: 700px;

    font-size: 18px;

    line-height: 1.7;

    color: #bcbcbc;
}


/* ============================================================
   SECTION HEADINGS
   ============================================================ */

.section-heading {
    margin-top: 30px;
    margin-bottom: 22px;

    font-size: 27px;

    font-weight: 800;

    color: white;

    border-left:
        4px solid #e50914;

    padding-left: 14px;
}


/* ============================================================
   SELECTBOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background: #111 !important;

    border:
        1px solid #333 !important;

    border-radius:
        10px !important;

    color: white !important;
}

div[data-baseweb="select"] > div:hover {
    border-color:
        #e50914 !important;
}

div[data-baseweb="select"] * {
    color: white !important;
}

label {
    color: #aaa !important;
}


/* ============================================================
   SELECTED MOVIE
   ============================================================ */

.selected-box {

    margin-top: 30px;
    margin-bottom: 35px;

    padding: 25px;

    display: flex;

    gap: 25px;

    align-items: center;

    background:
        linear-gradient(
            120deg,
            #101010,
            #080808
        );

    border:
        1px solid #292929;

    border-left:
        4px solid #e50914;

    border-radius: 15px;

    box-shadow:
        0 15px 45px rgba(0,0,0,0.55);
}

.selected-poster {

    width: 170px;
    height: 250px;

    object-fit: cover;

    border-radius: 10px;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.7);
}

.selected-info {
    flex: 1;
}

.selected-title {

    font-size: 30px;

    font-weight: 850;

    margin-bottom: 12px;

    color: white;
}

.selected-description {

    color: #aaa;

    line-height: 1.75;

    font-size: 15px;
}


/* ============================================================
   MOVIE CARDS
   ============================================================ */

.movie-wrapper {
    margin-bottom: 25px;
}

.movie-poster-container {

    position: relative;

    overflow: hidden;

    border-radius: 12px;

    background: #111;

    border:
        1px solid #292929;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.45);

    transition:
        transform 0.35s ease,
        border-color 0.35s ease,
        box-shadow 0.35s ease;
}

.movie-poster-container:hover {

    transform:
        translateY(-7px)
        scale(1.025);

    border-color:
        rgba(229,9,20,0.85);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.75),
        0 0 18px rgba(229,9,20,0.18);
}

.movie-poster {

    display: block;

    width: 100%;

    aspect-ratio: 2 / 3;

    object-fit: cover;

    transition:
        transform 0.5s ease,
        filter 0.5s ease;
}

.movie-poster-container:hover
.movie-poster {

    transform:
        scale(1.06);

    filter:
        brightness(0.65);
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
            180deg,
            transparent 30%,
            rgba(0,0,0,0.75)
        );

    transition:
        opacity 0.3s ease;
}

.movie-poster-container:hover
.movie-overlay {
    opacity: 1;
}

.play-circle {

    width: 55px;
    height: 55px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background: #e50914;

    color: white;

    font-size: 21px;

    padding-left: 3px;

    box-shadow:
        0 0 30px rgba(229,9,20,0.5);
}

.movie-title {

    margin-top: 10px;

    color: #eee;

    font-size: 14px;

    font-weight: 650;

    text-align: center;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


/* ============================================================
   VIDEO SECTION
   ============================================================ */

.video-heading {

    max-width: 1100px;

    margin:
        30px auto 18px auto;

    font-size: 27px;

    font-weight: 850;

    color: white;

    border-left:
        4px solid #e50914;

    padding-left: 14px;
}


.video-box {

    width: 100%;

    max-width: 1100px;

    margin:
        0 auto 38px auto;

    padding: 0;

    background: #080808;

    border-radius: 15px;

    border:
        1px solid #292929;

    overflow: hidden;

    box-shadow:
        0 20px 60px rgba(0,0,0,0.70);

    position: relative;
}


/*
   Streamlit st.video iframe/video area
   Force same 16:9 size for trailer and full movie.
*/

.video-box [data-testid="stVideo"] {

    width: 100% !important;

    aspect-ratio: 16 / 9 !important;

    min-height: 0 !important;

    background: #000 !important;

    border-radius: 14px !important;

    overflow: hidden !important;
}

.video-box [data-testid="stVideo"] video,
.video-box iframe {

    width: 100% !important;

    height: 100% !important;

    aspect-ratio: 16 / 9 !important;

    border: none !important;
}


/* ============================================================
   FULL MOVIE PLACEHOLDER
   ============================================================ */

.full-movie-placeholder {

    width: 100%;

    aspect-ratio: 16 / 9;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-direction: column;

    gap: 12px;

    background:
        radial-gradient(
            circle at center,
            rgba(229,9,20,0.12),
            #080808 55%
        );

    color: #aaa;

    text-align: center;
}

.full-movie-placeholder .big-play {

    width: 64px;
    height: 64px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background: #e50914;

    color: white;

    font-size: 25px;

    box-shadow:
        0 0 35px rgba(229,9,20,0.35);
}

.full-movie-placeholder strong {
    color: white;
    font-size: 18px;
}


/* ============================================================
   DETAILS TITLE
   ============================================================ */

.details-title {

    text-align: left;

    max-width: 1100px;

    margin:
        25px auto 25px auto;

    padding-left: 18px;

    border-left:
        5px solid #e50914;

    font-size:
        clamp(30px, 5vw, 48px);

    font-weight: 900;

    color: white;
}


/* ============================================================
   DETAILS PANEL
   ============================================================ */

.details-panel {

    max-width: 1100px;

    margin:
        0 auto 50px auto;

    padding: 28px;

    background:
        linear-gradient(
            135deg,
            #111,
            #080808
        );

    border:
        1px solid #292929;

    border-left:
        4px solid #e50914;

    border-radius: 15px;

    box-shadow:
        0 20px 50px rgba(0,0,0,0.6);
}

.detail-row {

    display: flex;

    flex-wrap: wrap;

    gap:
        10px 35px;

    margin-bottom: 22px;
}

.detail-item {

    color: #aaa;

    font-size: 15px;
}

.detail-item strong {
    color: white;
}

.story-heading {

    color: white;

    font-size: 21px;

    font-weight: 800;

    margin-bottom: 10px;
}

.story-text {

    color: #aaa;

    line-height: 1.8;

    font-size: 15px;
}

.genre-tag {

    display: inline-block;

    margin:
        4px 5px 4px 0;

    padding:
        6px 11px;

    border-radius: 20px;

    background:
        rgba(229,9,20,0.10);

    border:
        1px solid rgba(229,9,20,0.30);

    color: #ff6b72;

    font-size: 12px;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {

    background:
        #e50914 !important;

    color:
        white !important;

    border:
        none !important;

    border-radius:
        8px !important;

    font-weight:
        700 !important;

    padding:
        10px 20px !important;

    transition:
        all 0.25s ease !important;
}

.stButton > button:hover {

    background:
        #f6121d !important;

    transform:
        translateY(-2px);

    box-shadow:
        0 8px 25px
        rgba(229,9,20,0.3);
}


/* ============================================================
   TEAM
   ============================================================ */

.team-section {

    margin-top: 65px;

    padding-top: 35px;

    border-top:
        1px solid #222;
}

.team-heading {

    text-align: center;

    font-size: 28px;

    font-weight: 850;

    color: white;

    margin-bottom: 30px;
}

.team-heading span {
    color: #e50914;
}

.team-card {

    background: #0d0d0d;

    border:
        1px solid #242424;

    border-radius: 14px;

    padding: 20px;

    text-align: center;

    height: 100%;

    transition:
        transform 0.3s ease,
        border-color 0.3s ease;
}

.team-card:hover {

    transform:
        translateY(-5px);

    border-color:
        #e50914;
}

.team-photo {

    width: 95px;
    height: 95px;

    object-fit: cover;

    border-radius: 50%;

    border:
        2px solid #333;

    margin-bottom: 12px;
}

.team-name {

    font-size: 17px;

    font-weight: 800;

    color: white;
}

.team-role {

    margin-top: 6px;

    font-size: 13px;

    color: #999;
}

.footer-text {

    text-align: center;

    margin-top: 40px;

    color: #666;

    font-size: 12px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .main .block-container {

        padding-left: 14px;
        padding-right: 14px;
    }

    .hero {

        padding:
            50px 22px;

        border-radius: 16px;
    }

    .hero-title {
        font-size: 38px;
    }

    .hero-subtitle {
        font-size: 14px;
    }

    .selected-box {

        flex-direction:
            column;

        text-align:
            center;
    }

    .selected-poster {

        width: 145px;
        height: 215px;
    }

    .selected-title {
        font-size: 24px;
    }

    .section-heading {
        font-size: 22px;
    }

    .movie-title {
        font-size: 12px;
    }

    .video-heading {

        margin-top: 25px;

        font-size: 22px;

        padding-left: 12px;
    }

    .video-box {

        width: 100%;

        margin-bottom: 28px;

        border-radius: 10px;
    }

    .video-box [data-testid="stVideo"] {

        width: 100% !important;

        aspect-ratio: 16 / 9 !important;

        height: auto !important;

        border-radius: 9px !important;
    }

    .video-box iframe {

        width: 100% !important;

        height: auto !important;

        aspect-ratio: 16 / 9 !important;
    }

    .full-movie-placeholder {

        aspect-ratio: 16 / 9;

        border-radius: 9px;
    }

    .details-title {

        font-size: 32px;

        margin-top: 20px;

        margin-bottom: 22px;
    }

    .details-panel {

        padding: 20px;

        border-radius: 12px;
    }

    .detail-row {

        gap:
            10px 18px;

        font-size: 13px;
    }

    .story-text {
        font-size: 13px;
    }

    .butterfly {

        opacity: 0.18;

        filter:
            blur(2px);
    }

    .b7,
    .b8 {
        display: none;
    }
}

</style>
""")


# ============================================================
# 3. BUTTERFLIES
# ============================================================

st.html("""
<div class="butterfly-field">

    <div class="butterfly b1">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b2">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b3">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b4">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b5">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b6">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b7">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

    <div class="butterfly b8">
        <div class="wing left"></div>
        <div class="wing right"></div>
        <div class="body"></div>
    </div>

</div>
""")


# ============================================================
# 4. FILE PATHS
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
# 5. ANISH PHOTO
# ============================================================

ANISH_PHOTO_URL = (
    "https://i.ibb.co/PsGGDLyW/"
    "IMG-20260920-084857-1.png"
)


# ============================================================
# 6. FULL MOVIE URLS
#
# Add only official/legal full-movie URLs here.
#
# Example:
#
# FULL_MOVIE_URLS = {
#     "Movie Name": "https://www.youtube.com/watch?v=VIDEO_ID"
# }
#
# ============================================================

FULL_MOVIE_URLS = {
    # "Avatar": "PASTE_OFFICIAL_FULL_MOVIE_YOUTUBE_URL_HERE",
}


# ============================================================
# 7. LOAD DATA
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
# 8. TMDB API
# ============================================================

TMDB_API_KEY = st.secrets[
    "TMDB_API_KEY"
]


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
            timeout=15
        )

        if response.status_code == 200:
            return response.json()

    except Exception:
        return None

    return None


# ============================================================
# 9. MOVIE DETAILS
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
# 10. POSTER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_poster(movie_id):

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
# 11. TRAILER
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_trailer(movie_id):

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
    # OFFICIAL TRAILER
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

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )

    # --------------------------------------------------------
    # NORMAL TRAILER
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # TEASER
    # --------------------------------------------------------

    for video in videos:

        if (
            video.get("site") == "YouTube"
            and
            video.get("type") == "Teaser"
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )

    return None


# ============================================================
# 12. FULL MOVIE
# ============================================================

def fetch_full_movie(
    movie_title
):

    if not movie_title:
        return None

    return FULL_MOVIE_URLS.get(
        str(movie_title)
    )


# ============================================================
# 13. RECOMMEND
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

    similar_movies = (
        similarity_indices[index][0:20]
    )

    for movie_index in similar_movies:

        try:

            movie_index = int(
                movie_index
            )

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

        names.append(
            movie_name
        )

        posters.append(
            fetch_poster(movie_id)
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
# 14. MOVIE CARD
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
# 15. SELECTED MOVIE PREVIEW
# ============================================================

def selected_movie_preview(
    movie_name
):

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

    details = fetch_movie_details(
        movie_id
    )

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

    st.html(f"""

    <div class="selected-box">

        <img
            class="selected-poster"
            src="{poster_url}"
            alt="{safe_title}"
        >

        <div class="selected-info">

            <div class="selected-title">
                {safe_title}
            </div>

            <div class="selected-description">
                {safe_overview}
            </div>

        </div>

    </div>

    """)


# ============================================================
# 16. MOVIE DETAILS PAGE
# ============================================================

def show_movie_details(
    movie_id
):

    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    if st.button(
        "←  Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


    # --------------------------------------------------------
    # FETCH DETAILS
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


    # ========================================================
    # TRAILER
    # ========================================================

    st.html("""
    <div class="video-heading">
        ▶️ Trailer
    </div>
    """)


    trailer_url = fetch_trailer(
        movie_id
    )


    if trailer_url:

        st.html("""
        <div class="video-box">
        """)

        st.video(
            trailer_url
        )

        st.html("""
        </div>
        """)

    else:

        st.html("""
        <div class="video-box">

            <div class="full-movie-placeholder">

                <div class="big-play">
                    ▶
                </div>

                <strong>
                    Trailer Not Available
                </strong>

                <span>
                    No trailer was found for this movie.
                </span>

            </div>

        </div>
        """)


    # ========================================================
    # FULL MOVIE
    # ========================================================

    st.html("""
    <div class="video-heading">
        🎞️ Full Movie
    </div>
    """)


    full_movie_url = fetch_full_movie(
        title
    )


    if full_movie_url:

        st.html("""
        <div class="video-box">
        """)

        st.video(
            full_movie_url
        )

        st.html("""
        </div>
        """)

    else:

        st.html("""
        <div class="video-box">

            <div class="full-movie-placeholder">

                <div class="big-play">
                    ▶
                </div>

                <strong>
                    Full Movie
                </strong>

                <span>
                    Add an official/legal full-movie
                    YouTube URL to FULL_MOVIE_URLS.
                </span>

            </div>

        </div>
        """)


    # ========================================================
    # TITLE
    # ========================================================

    st.html(f"""

    <div class="details-title">
        🎬 {html.escape(str(title))}
    </div>

    """)


    # ========================================================
    # RUNTIME
    # ========================================================

    runtime_text = "Unknown"

    if runtime:

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


    # ========================================================
    # GENRES
    # ========================================================

    genre_html = ""

    for genre in genres:

        genre_name = genre.get(
            "name"
        )

        if genre_name:

            genre_html += (
                '<span class="genre-tag">'
                +
                html.escape(
                    str(genre_name)
                )
                +
                '</span>'
            )


    # ========================================================
    # STORY
    # ========================================================

    safe_overview = html.escape(
        str(overview)
    )


    # ========================================================
    # DETAILS PANEL
    # ========================================================

    st.html(f"""

    <div class="details-panel">

        <div class="detail-row">

            <div class="detail-item">
                ⭐ <strong>Rating:</strong>
                {float(rating):.1f}/10
            </div>

            <div class="detail-item">
                📅 <strong>Release:</strong>
                {html.escape(str(release_date))}
            </div>

            <div class="detail-item">
                ⏱️ <strong>Runtime:</strong>
                {html.escape(str(runtime_text))}
            </div>

        </div>


        <div class="story-heading">
            🎭 Genres
        </div>

        <div style="margin-bottom:25px;">
            {genre_html}
        </div>


        <div class="story-heading">
            📖 Story
        </div>

        <div class="story-text">
            {safe_overview}
        </div>

    </div>

    """)


# ============================================================
# 17. TEAM
# ============================================================

def show_team():

    st.html("""

    <div class="team-section">

        <div class="team-heading">
            Meet The <span>Developer</span>
        </div>

    </div>

    """)


    cols = st.columns(
        4,
        gap="medium"
    )


    # ========================================================
    # ANISH
    # ========================================================

    with cols[0]:

        st.html(f"""

        <a
            href="https://github.com/Anish-kumar-00"
            target="_blank"
            rel="noopener noreferrer"
            style="
                display:block;
                text-decoration:none;
                color:inherit;
                height:100%;
            "
        >

            <div class="team-card">

                <img
                    class="team-photo"
                    src="{ANISH_PHOTO_URL}"
                    alt="Anish Kumar"
                >

                <div class="team-name">
                    Anish Kumar
                </div>

                <div class="team-role">
                    Coding & Development
                </div>

            </div>

        </a>

        """)


    # ========================================================
    # ABHISHEK
    # ========================================================

    with cols[1]:

        st.html("""

        <div class="team-card">

            <div
                class="team-photo"
                style="
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#171717;
                    color:#e50914;
                    font-size:30px;
                "
            >
                A
            </div>

            <div class="team-name">
                Abhishek Kumar
            </div>

            <div class="team-role">
                Mathematical Calculation
            </div>

        </div>

        """)


    # ========================================================
    # ABRAR
    # ========================================================

    with cols[2]:

        st.html("""

        <div class="team-card">

            <div
                class="team-photo"
                style="
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#171717;
                    color:#e50914;
                    font-size:30px;
                "
            >
                A
            </div>

            <div class="team-name">
                Abrar Ahmad
            </div>

            <div class="team-role">
                Special Project Manager
            </div>

        </div>

        """)


    # ========================================================
    # VISHAL
    # ========================================================

    with cols[3]:

        st.html("""

        <div class="team-card">

            <div
                class="team-photo"
                style="
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    background:#171717;
                    color:#e50914;
                    font-size:30px;
                "
            >
                V
            </div>

            <div class="team-name">
                Vishal Kumar
            </div>

            <div class="team-role">
                Frontend Development
            </div>

        </div>

        """)


    # ========================================================
    # FOOTER
    # ========================================================

    st.html("""

    <div class="footer-text">

        🎬 Movie Recommendation System

        <br><br>

        Developed with Python • Streamlit •
        Machine Learning • TMDB

    </div>

    """)


# ============================================================
# 18. URL ROUTING
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 19. DETAILS PAGE
# ============================================================

if movie_id_from_url:

    try:

        movie_id = int(
            movie_id_from_url
        )

        show_movie_details(
            movie_id
        )

    except (
        ValueError,
        TypeError
    ):

        st.error(
            "Invalid movie ID."
        )


# ============================================================
# 20. HOME PAGE
# ============================================================

else:

    # ========================================================
    # HERO
    # ========================================================

    st.html("""

    <div class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                AI POWERED • CONTENT BASED
            </div>

            <h1 class="hero-title">
                Movie
                <span>Recommendation</span>
                System
            </h1>

            <div class="hero-subtitle">

                Discover movies you will love.
                Select a movie and explore similar
                recommendations powered by Machine Learning.

            </div>

        </div>

    </div>

    """)


    # ========================================================
    # MOVIE SELECTOR
    # ========================================================

    st.html("""

    <div class="section-heading">
        🎬 Choose Your Movie
    </div>

    """)


    movie_list = (
        movies["title"]
        .dropna()
        .values
    )


    if "Avatar" in movie_list:

        default_index = list(
            movie_list
        ).index("Avatar")

    else:

        default_index = 0


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


    st.html(f"""

    <div class="section-heading">
        ✨ Recommended Movies
    </div>

    <div style="
        color:#777;
        margin-bottom:25px;
        font-size:14px;
    ">

        Movies similar to

        <strong style="color:#ddd;">
            {html.escape(str(selected_movie))}
        </strong>

    </div>

    """)


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

                st.html(
                    movie_card_html(
                        names[position],
                        posters[position],
                        ids[position]
                    )
                )


    # ========================================================
    # TEAM
    # ========================================================

    show_team()