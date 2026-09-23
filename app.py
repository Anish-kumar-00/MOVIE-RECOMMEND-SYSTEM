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
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. GLOBAL CSS — CLEAN NETFLIX STYLE
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
    background: #000;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #000000 0%,
            #080808 45%,
            #000000 100%
        );

    color: #ffffff;
    overflow-x: hidden;
}


/* ============================================================
   STREAMLIT CONTAINER
   ============================================================ */

.block-container {
    max-width: 1500px;
    padding-top: 18px;
    padding-bottom: 50px;
}

[data-testid="stVerticalBlock"] {
    gap: 0.35rem;
}


/* ============================================================
   HIDE DEFAULT STREAMLIT ELEMENTS
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
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background: #141414 !important;

    border: 1px solid #333333 !important;

    border-radius: 5px !important;

    color: #ffffff !important;

    min-height: 46px;

    box-shadow: none !important;

    transition: border-color 0.2s ease;
}

div[data-baseweb="select"] > div:hover {

    border-color: #777777 !important;
}

div[data-baseweb="select"] > div:focus-within {

    border-color: #e50914 !important;

    box-shadow: 0 0 0 1px #e50914 !important;
}


/* Dropdown text */

div[data-baseweb="select"] span {
    color: #ffffff !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {

    background: #e50914 !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 4px !important;

    font-weight: 700 !important;

    padding: 8px 18px !important;

    transition:
        background 0.2s ease,
        transform 0.2s ease !important;

    box-shadow: none !important;
}

.stButton > button:hover {

    background: #f40612 !important;

    transform: translateY(-1px);

    box-shadow: none !important;
}


/* ============================================================
   HR
   ============================================================ */

hr {

    border: none !important;

    height: 1px !important;

    background: #292929 !important;

    margin: 30px 0 !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {

    position: relative;

    min-height: 470px;

    display: flex;

    align-items: flex-end;

    padding: 50px;

    border-radius: 4px;

    overflow: hidden;

    margin-bottom: 42px;

    background:
        linear-gradient(
            90deg,
            #000000 0%,
            rgba(0,0,0,0.95) 18%,
            rgba(0,0,0,0.72) 42%,
            rgba(0,0,0,0.30) 70%,
            rgba(0,0,0,0.78) 100%
        ),
        linear-gradient(
            180deg,
            rgba(0,0,0,0.05) 35%,
            #000000 100%
        ),
        radial-gradient(
            circle at 75% 35%,
            #351014 0%,
            #170708 28%,
            #090909 58%,
            #000000 100%
        );

    box-shadow:
        inset 0 -100px 100px rgba(0,0,0,0.65);
}


/* subtle cinematic line */

.hero-box::after {

    content: "";

    position: absolute;

    left: 0;
    right: 0;
    bottom: 0;

    height: 2px;

    background: #e50914;

    opacity: 0.75;
}


.hero-content {

    position: relative;

    z-index: 5;

    max-width: 720px;

    animation: heroFade 0.8s ease-out;
}


@keyframes heroFade {

    from {
        opacity: 0;
        transform: translateY(18px);
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

    font-size: clamp(42px, 6vw, 76px);

    font-weight: 900;

    line-height: 0.98;

    letter-spacing: -2px;

    margin: 12px 0 20px;

    color: #ffffff;
}


.gradient-text {

    color: #e50914;

    background: none;

    -webkit-text-fill-color: #e50914;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section-title {

    font-size: 27px;

    font-weight: 800;

    color: #ffffff;

    margin-top: 15px;

    margin-bottom: 5px;
}


.section-subtitle {

    color: #8c8c8c;

    margin-bottom: 22px;

    font-size: 14px;
}


.section-subtitle strong {

    color: #ffffff !important;

    text-shadow: none !important;
}


/* ============================================================
   SELECTED MOVIE
   ============================================================ */

.selected-movie-box {

    position: relative;

    display: flex;

    align-items: center;

    gap: 24px;

    padding: 18px;

    min-height: 175px;

    margin-top: 22px;

    margin-bottom: 34px;

    border-radius: 5px;

    background: #111111;

    border: 1px solid #252525;

    box-shadow: 0 8px 25px rgba(0,0,0,0.35);

    overflow: hidden;
}


.selected-movie-box::after {

    content: "";

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 4px;

    background: #e50914;
}


.selected-poster {

    width: 115px;

    height: 165px;

    object-fit: cover;

    border-radius: 3px;

    position: relative;

    z-index: 2;

    box-shadow:
        0 8px 20px rgba(0,0,0,0.55);
}


.selected-info {

    position: relative;

    z-index: 2;
}


.selected-badge {

    display: inline-block;

    padding: 5px 10px;

    border-radius: 3px;

    color: #ffffff;

    font-size: 11px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.7px;

    background: #e50914;
}


.selected-title {

    font-size: 30px;

    font-weight: 800;

    margin: 8px 0 10px;

    color: #ffffff;
}


.selected-overview {

    color: #b3b3b3;

    line-height: 1.6;

    max-width: 780px;

    font-size: 14px;
}


/* ============================================================
   MOVIE GRID
   ============================================================ */

div[data-testid="stHorizontalBlock"] {

    position: relative;

    padding: 5px 2px;

    margin-bottom: 6px;

    overflow: visible;
}


/* ============================================================
   MOVIE CARD
   ============================================================ */

.movie-wrapper {

    position: relative;

    background: #111111;

    border: 1px solid #242424;

    border-radius: 4px;

    padding: 0;

    margin-bottom: 18px;

    overflow: hidden;

    transition:
        transform 0.28s ease,
        box-shadow 0.28s ease,
        border-color 0.28s ease;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.35);

    z-index: 2;
}


.movie-wrapper:hover {

    transform:
        translateY(-7px)
        scale(1.025);

    border-color: #444444;

    box-shadow:
        0 15px 30px rgba(0,0,0,0.75);

    z-index: 50;
}


/* ============================================================
   POSTER
   ============================================================ */

.movie-poster-container {

    position: relative;

    overflow: hidden;

    border-radius: 3px 3px 0 0;

    z-index: 3;

    background: #181818;
}


.movie-poster {

    width: 100%;

    aspect-ratio: 2 / 3;

    object-fit: cover;

    display: block;

    transition:
        transform 0.4s ease,
        filter 0.4s ease;
}


.movie-wrapper:hover .movie-poster {

    transform: scale(1.055);

    filter:
        brightness(0.62)
        saturate(1.05);
}


/* ============================================================
   HOVER OVERLAY
   ============================================================ */

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
            rgba(0,0,0,0.05),
            rgba(0,0,0,0.72)
        );

    transition: opacity 0.25s ease;
}


.movie-wrapper:hover .movie-overlay {

    opacity: 1;
}


.play-circle {

    width: 50px;

    height: 50px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 50%;

    background: #e50914;

    color: #ffffff;

    font-size: 20px;

    box-shadow:
        0 5px 18px rgba(0,0,0,0.55);

    transition:
        transform 0.2s ease,
        background 0.2s ease;
}


.movie-wrapper:hover .play-circle {

    transform: scale(1.08);

    background: #f40612;
}


/* ============================================================
   MOVIE TITLE
   ============================================================ */

.movie-title {

    position: relative;

    z-index: 5;

    color: #e5e5e5;

    font-size: 13px;

    font-weight: 650;

    text-align: center;

    padding: 11px 5px;

    min-height: 44px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #111111;

    transition: color 0.2s ease;
}


.movie-wrapper:hover .movie-title {

    color: #ffffff;
}


/* ============================================================
   DETAILS PAGE
   ============================================================ */

.details-title {

    font-size: clamp(30px, 5vw, 55px);

    font-weight: 900;

    margin-top: 25px;

    margin-bottom: 20px;

    color: #ffffff;
}


.trailer-heading {

    font-size: 27px;

    font-weight: 800;

    margin-top: 18px;

    margin-bottom: 15px;

    color: #ffffff;
}


.trailer-heading::first-letter {

    color: #e50914;
}


/* ============================================================
   TRAILER
   ============================================================ */

.trailer-box {

    width: 100%;

    padding: 0;

    border-radius: 4px;

    background: #111111;

    border: 1px solid #2a2a2a;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.55);

    margin-bottom: 35px;

    overflow: hidden;
}


.trailer-inner {

    width: 100%;

    border-radius: 4px;

    overflow: hidden;

    background: #000;
}


/* ============================================================
   CENTER POSTER
   ============================================================ */

.center-poster-wrap {

    width: 100%;

    aspect-ratio: 16 / 9;

    margin: 25px auto 35px;

    padding: 0;

    border-radius: 4px;

    background: #111111;

    border: 1px solid #292929;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.6);

    overflow: hidden;
}


.center-poster {

    width: 100%;

    height: 100%;

    aspect-ratio: 16 / 9;

    object-fit: cover;

    display: block;

    border-radius: 3px;
}


/* ============================================================
   DETAILS PANEL
   ============================================================ */

.details-panel {

    position: relative;

    padding: 28px;

    border-radius: 5px;

    background: #111111;

    border: 1px solid #292929;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.4);

    overflow: hidden;
}


.details-panel::before {

    content: "";

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 4px;

    background: #e50914;
}


.info-heading {

    font-size: 27px;

    font-weight: 800;

    color: #ffffff;

    margin-bottom: 22px;
}


.info-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;

    margin-bottom: 25px;
}


.info-item {

    padding: 17px;

    border-radius: 4px;

    background: #181818;

    border: 1px solid #2b2b2b;

    transition:
        background 0.2s ease,
        border-color 0.2s ease;
}


.info-item:hover {

    background: #202020;

    border-color: #444444;
}


.info-label {

    color: #8c8c8c;

    font-size: 12px;

    margin-bottom: 6px;

    text-transform: uppercase;

    letter-spacing: 0.4px;
}


.info-value {

    color: #ffffff;

    font-size: 19px;

    font-weight: 750;
}


/* ============================================================
   GENRES / STORY
   ============================================================ */

.genre-section,
.story-section {

    padding-top: 20px;

    margin-top: 18px;

    border-top:
        1px solid #292929;
}


.genre-title,
.story-title {

    font-size: 19px;

    font-weight: 800;

    color: #ffffff;

    margin-bottom: 10px;
}


.genre-tag {

    display: inline-block;

    padding: 6px 12px;

    margin: 4px 5px 4px 0;

    border-radius: 3px;

    color: #ffffff;

    border: 1px solid #444444;

    background: #181818;

    font-size: 13px;
}


.story-text {

    color: #b3b3b3;

    line-height: 1.8;

    font-size: 14px;
}


/* ============================================================
   TEAM FOOTER
   ============================================================ */

.team-footer {

    position: relative;

    width: 100%;

    margin-top: 55px;

    padding: 0 12px 35px;

    text-align: center;

    overflow: hidden;
}


.team-neon-line {

    width: 82%;

    height: 1px;

    margin: 0 auto 28px;

    background: #333333;

    border-radius: 0;

    box-shadow: none;

    animation: none;
}


.team-grid {

    width: 92%;

    max-width: 1150px;

    margin: 0 auto;

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    align-items: stretch;
}


.team-member {

    min-height: 145px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    padding: 8px 12px;

    position: relative;
}


.team-member + .team-member {

    border-left:
        1px solid
        #2b2b2b;
}


/* ============================================================
   ANISH PHOTO
   ============================================================ */

.team-photo {

    width: 58px;

    height: 58px;

    border-radius: 50%;

    object-fit: cover;

    object-position: center;

    padding: 2px;

    margin-bottom: 8px;

    background: #222222;

    border: 2px solid #e50914;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.6);

    animation: none;
}


/* ============================================================
   TEAM ICONS
   ============================================================ */

.team-icon {

    height: 38px;

    display: flex;

    align-items: center;

    justify-content: center;

    margin-bottom: 8px;

    font-size: 27px;

    font-weight: 900;

    line-height: 1;

    color: #e50914;

    text-shadow: none;
}


.icon-math,
.icon-project,
.icon-front {

    color: #e50914;

    text-shadow: none;
}


/* ============================================================
   TEAM TEXT
   ============================================================ */

.team-role {

    color: #999999;

    font-size: 12px;

    font-weight: 500;

    line-height: 1.35;

    min-height: 35px;

    display: flex;

    align-items: center;

    justify-content: center;

    text-align: center;
}


.team-name {

    margin-top: 5px;

    font-size: 16px;

    font-weight: 800;

    line-height: 1.2;

    white-space: nowrap;

    color: #ffffff;
}


.name-anish,
.name-abhishek,
.name-abrar,
.name-vishal {

    color: #ffffff;

    text-shadow: none;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .block-container {

        padding-left: 9px;

        padding-right: 9px;

        padding-top: 10px;
    }


    .hero-box {

        min-height: 330px;

        padding: 28px 22px;

        border-radius: 3px;

        margin-bottom: 30px;
    }


    .hero-title {

        font-size: 41px;

        line-height: 1;

        letter-spacing: -1px;
    }


    .selected-movie-box {

        gap: 14px;

        padding: 12px;

        min-height: 140px;
    }


    .selected-poster {

        width: 82px;

        height: 120px;
    }


    .selected-title {

        font-size: 22px;

        margin: 7px 0;
    }


    .selected-overview {

        font-size: 11px;

        line-height: 1.45;

        display: -webkit-box;

        -webkit-line-clamp: 4;

        -webkit-box-orient: vertical;

        overflow: hidden;
    }


    .section-title {

        font-size: 23px;
    }


    .movie-wrapper {

        border-radius: 3px;

        margin-bottom: 10px;
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

        width: 42px;

        height: 42px;

        font-size: 17px;
    }


    div[data-testid="stHorizontalBlock"] {

        padding: 3px 1px;

        margin-bottom: 4px;
    }


    .trailer-box {

        border-radius: 3px;

        margin-bottom: 25px;
    }


    .trailer-heading {

        font-size: 23px;
    }


    .center-poster-wrap {

        width: 100%;

        aspect-ratio: 16 / 9;

        margin: 18px auto 25px;

        border-radius: 3px;
    }


    .center-poster {

        border-radius: 2px;
    }


    .details-panel {

        padding: 18px;
    }


    .info-grid {

        grid-template-columns: 1fr;

        gap: 9px;
    }


    .info-value {

        font-size: 17px;
    }


    .genre-tag {

        font-size: 11px;

        padding: 5px 9px;
    }


    .story-text {

        font-size: 13px;

        line-height: 1.7;
    }


    /* ========================================================
       MOBILE FOOTER
       ======================================================== */

    .team-footer {

        margin-top: 35px;

        padding: 0 3px 25px;
    }


    .team-neon-line {

        width: 88%;

        margin-bottom: 18px;
    }


    .team-grid {

        width: 100%;

        grid-template-columns:
            repeat(4, 1fr);
    }


    .team-member {

        min-height: 130px;

        padding: 5px 3px;
    }


    .team-member + .team-member {

        border-left:
            1px solid
            #292929;
    }


    .team-photo {

        width: 43px;

        height: 43px;

        padding: 2px;

        margin-bottom: 5px;
    }


    .team-icon {

        height: 28px;

        font-size: 21px;

        margin-bottom: 5px;
    }


    .team-role {

        font-size: 8px;

        line-height: 1.25;

        min-height: 31px;
    }


    .team-name {

        margin-top: 5px;

        font-size: 10px;
    }

}

</style>
""")


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
# 4. ANISH PHOTO
# ============================================================

ANISH_PHOTO_URL = (
    "https://i.ibb.co/PsGGDLyW/"
    "IMG-20260920-084857-1.png"
)


# ============================================================
# 5. LOAD DATA
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
# 6. TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# 7. TMDB REQUEST
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
            timeout=15
        )

        if response.status_code == 200:

            return response.json()

    except Exception:

        return None

    return None


# ============================================================
# 8. MOVIE DETAILS
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
# 9. POSTER
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
# 10. TRAILER
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


    # OFFICIAL TRAILER

    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
            and video.get("official") is True
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    # NORMAL TRAILER

    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Trailer"
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    # TEASER

    for video in videos:

        if (
            video.get("site") == "YouTube"
            and video.get("type") == "Teaser"
        ):

            key = video.get("key")

            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    return None


# ============================================================
# 11. RECOMMENDATION
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
# 12. MOVIE CARD
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
# 13. SELECTED MOVIE PREVIEW
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
                    Selected Movie
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
# 14. DETAILS PAGE
# ============================================================

def show_movie_details(
    movie_id
):

    if st.button(
        "←  Back to Recommendations",
        key="back_button"
    ):

        st.query_params.clear()

        st.rerun()


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


    # ========================================================
    # TRAILER
    # ========================================================

    st.html(
        '<div class="trailer-heading">'
        '▶ Trailer'
        '</div>'
    )


    trailer_url = fetch_trailer(
        movie_id
    )


    if trailer_url:

        st.html(
            '<div class="trailer-box">'
            '<div class="trailer-inner">'
        )

        st.video(
            trailer_url
        )

        st.html(
            "</div></div>"
        )

    else:

        st.warning(
            "Trailer is not available for this movie."
        )


    # ========================================================
    # POSTER
    # ========================================================

    if poster_path:

        poster_url = (
            "https://image.tmdb.org/t/p/w780"
            + poster_path
        )


        st.html(
            f"""
            <div class="center-poster-wrap">

                <img
                    class="center-poster"
                    src="{poster_url}"
                    alt="{html.escape(str(title))}"
                >

            </div>
            """
        )


    # ========================================================
    # TITLE
    # ========================================================

    st.html(
        f"""
        <div class="details-title">

            🎬 {html.escape(str(title))}

        </div>
        """
    )


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
                f'{html.escape(str(genre_name))}'
                '</span>'
            )


    safe_overview = html.escape(
        str(overview)
    )


    # ========================================================
    # DETAILS PANEL
    # ========================================================

    st.html(
        f"""
        <div class="details-panel">

            <div class="info-heading">

                🎬 {html.escape(str(title))}

            </div>


            <div class="info-grid">


                <div class="info-item">

                    <div class="info-label">
                        TMDB Rating
                    </div>

                    <div class="info-value">
                        ⭐ {float(rating):.1f}/10
                    </div>

                </div>


                <div class="info-item">

                    <div class="info-label">
                        Release Date
                    </div>

                    <div class="info-value">
                        {html.escape(
                            str(release_date)
                        )}
                    </div>

                </div>


                <div class="info-item">

                    <div class="info-label">
                        Runtime
                    </div>

                    <div class="info-value">
                        {html.escape(
                            str(runtime_text)
                        )}
                    </div>

                </div>


            </div>


            <div class="genre-section">

                <div class="genre-title">
                    Genres
                </div>

                <div>
                    {genre_html}
                </div>

            </div>


            <div class="story-section">

                <div class="story-title">
                    Story
                </div>

                <div class="story-text">
                    {safe_overview}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# 15. QUERY PARAMETER
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 16. DETAILS PAGE
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
# 17. MAIN PAGE
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
                        color:#e50914;
                        font-size:12px;
                        font-weight:800;
                        letter-spacing:2px;
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
                        color:#b3b3b3;
                        font-size:16px;
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
                font-size:28px;
                font-weight:800;
                margin-bottom:8px;
                color:#ffffff;
            "
        >

            🎬 Choose Your Movie

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

            <strong>

                {html.escape(
                    str(selected_movie)
                )}

            </strong>

            <br>

            Select any poster to view movie details.

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

                st.html(
                    movie_card_html(
                        names[position],
                        posters[position],
                        ids[position]
                    )
                )


    # ========================================================
    # TEAM FOOTER
    # ========================================================

    st.html(
        f"""
        <div class="team-footer">

            <div class="team-neon-line"></div>


            <div class="team-grid">


                <!-- ANISH -->

                <div class="team-member">

                    <img
                        class="team-photo"
                        src="{ANISH_PHOTO_URL}"
                        alt="Anish Kumar"
                        loading="lazy"
                    >


                    <div class="team-role">

                        Coding development<br>
                        by

                    </div>


                    <div class="team-name name-anish">

                        Anish Kumar

                    </div>

                </div>


                <!-- ABHISHEK -->

                <div class="team-member">

                    <div class="team-icon icon-math">

                        ▦

                    </div>


                    <div class="team-role">

                        Mathematical<br>
                        calculation by

                    </div>


                    <div class="team-name name-abhishek">

                        Abhishek Kumar

                    </div>

                </div>


                <!-- ABRAR -->

                <div class="team-member">

                    <div class="team-icon icon-project">

                        ☁

                    </div>


                    <div class="team-role">

                        Manage project by

                    </div>


                    <div class="team-name name-abrar">

                        Abrar Ahmad

                    </div>

                </div>


                <!-- VISHAL -->

                <div class="team-member">

                    <div class="team-icon icon-front">

                        ▱

                    </div>


                    <div class="team-role">

                        Front development by

                    </div>


                    <div class="team-name name-vishal">

                        Vishal Kumar

                    </div>

                </div>


            </div>

        </div>
        """
    )