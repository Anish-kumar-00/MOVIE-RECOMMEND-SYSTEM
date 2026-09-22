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
       MAIN APP
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 90, 255, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 80%,
                rgba(229, 9, 20, 0.08),
                transparent 30%
            ),
            #050505;

        color: #ffffff;
    }


    .block-container {
        max-width: 1500px;

        padding-top: 25px;
        padding-bottom: 50px;
    }


    /* =====================================================
       SELECT BOX
       ===================================================== */

    div[data-baseweb="select"] > div {

        background-color: #181818 !important;

        border: 1px solid #444 !important;

        border-radius: 8px !important;

        color: white !important;
    }


    /* =====================================================
       NORMAL STREAMLIT BUTTON
       ===================================================== */

    .stButton > button {

        background:
            linear-gradient(
                135deg,
                #e50914,
                #b20710
            ) !important;

        color: white !important;

        border: 1px solid #ff3441 !important;

        border-radius: 7px !important;

        font-weight: 700 !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease !important;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 8px 20px
            rgba(229, 9, 20, 0.35) !important;
    }


    /* =====================================================
       LINK BUTTON
       ===================================================== */

    .stLinkButton > a {

        background:
            linear-gradient(
                135deg,
                #e50914,
                #b20710
            ) !important;

        color: white !important;

        border: 1px solid #ff3441 !important;

        border-radius: 7px !important;

        font-weight: 700 !important;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: #292929 !important;
    }


    /* =====================================================
       HERO ANIMATION
       ===================================================== */

    @keyframes heroGlow {

        0% {
            box-shadow:
                0 0 20px
                rgba(229, 9, 20, 0.08);
        }

        50% {
            box-shadow:
                0 0 45px
                rgba(229, 9, 20, 0.20);
        }

        100% {
            box-shadow:
                0 0 20px
                rgba(229, 9, 20, 0.08);
        }
    }


    .hero-box {

        animation:
            heroGlow 4s
            ease-in-out
            infinite;

        border: 1px solid
            rgba(229, 9, 20, 0.25);
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
            titleFade 1s
            ease-out;
    }


    /* =====================================================
       MOVIE ROW
       BLUE + RED GLOW
       ===================================================== */

    div[data-testid="stHorizontalBlock"] {

        position: relative;

        padding:
            8px 5px;

        border-radius: 18px;

        background:

            radial-gradient(
                circle at 5% 50%,
                rgba(0, 90, 255, 0.24),
                transparent 25%
            ),

            radial-gradient(
                circle at 95% 50%,
                rgba(229, 9, 20, 0.26),
                transparent 25%
            ),

            linear-gradient(
                90deg,
                rgba(0, 90, 255, 0.06),
                rgba(229, 9, 20, 0.07),
                rgba(0, 90, 255, 0.06)
            );

        background-size:
            200% 100%,
            200% 100%,
            300% 100%;

        animation:
            gapGlow 8s
            ease-in-out
            infinite;

        margin-bottom: 10px;
    }


    /* =====================================================
       BLUE + RED MOVING LIGHT
       ===================================================== */

    @keyframes gapGlow {

        0% {

            background-position:
                0% 50%,
                100% 50%,
                0% 50%;
        }

        25% {

            background-position:
                35% 50%,
                65% 50%,
                25% 50%;
        }

        50% {

            background-position:
                100% 50%,
                0% 50%,
                100% 50%;
        }

        75% {

            background-position:
                65% 50%,
                35% 50%,
                75% 50%;
        }

        100% {

            background-position:
                0% 50%,
                100% 50%,
                0% 50%;
        }
    }


    /* =====================================================
       MOVIE CARD
       ===================================================== */

    .movie-wrapper {

        position: relative;

        background:
            linear-gradient(
                145deg,
                #181c27,
                #101014
            );

        border: 1px solid
            #333333;

        border-radius: 12px;

        padding: 6px;

        margin-bottom: 22px;

        overflow: hidden;

        transition:
            transform 0.35s ease,
            border-color 0.35s ease,
            box-shadow 0.35s ease;

        box-shadow:
            0 8px 20px
            rgba(0, 0, 0, 0.35);

        z-index: 2;
    }


    /* =====================================================
       ANIMATED CARD BORDER
       ===================================================== */

    .movie-wrapper::before {

        content: "";

        position: absolute;

        top: -2px;
        left: -2px;

        right: -2px;
        bottom: -2px;

        border-radius: 13px;

        background:
            linear-gradient(
                120deg,
                transparent,
                rgba(0, 90, 255, 0.85),
                transparent,
                rgba(229, 9, 20, 0.90),
                transparent
            );

        background-size:
            300% 300%;

        opacity: 0;

        z-index: 0;

        transition:
            opacity 0.35s ease;

        animation:
            borderMove 4s
            linear
            infinite;
    }


    @keyframes borderMove {

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


    .movie-wrapper:hover::before {

        opacity: 1;
    }


    /* =====================================================
       MOVIE CARD HOVER
       ===================================================== */

    .movie-wrapper:hover {

        transform:
            translateY(-8px)
            scale(1.025);

        border-color:
            #e50914;

        box-shadow:

            0 18px 40px
            rgba(229, 9, 20, 0.28),

            0 0 25px
            rgba(0, 90, 255, 0.18);

        z-index: 20;
    }


    /* =====================================================
       MOVIE POSTER
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
       PLAY OVERLAY
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
                #e50914,
                #0057ff
            );

        color: white;

        font-size: 23px;

        box-shadow:
            0 5px 25px
            rgba(229, 9, 20, 0.55);

        animation:
            playPulse 1.7s
            infinite;
    }


    @keyframes playPulse {

        0% {

            box-shadow:
                0 0 0 0
                rgba(229, 9, 20, 0.55);
        }

        70% {

            box-shadow:
                0 0 0 14px
                rgba(229, 9, 20, 0);
        }

        100% {

            box-shadow:
                0 0 0 0
                rgba(229, 9, 20, 0);
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
       SECTION TITLE
       ===================================================== */

    .section-title {

        font-size: 32px;

        font-weight: 900;

        margin-top: 25px;

        margin-bottom: 5px;
    }


    .section-subtitle {

        color: #999;

        margin-bottom: 25px;
    }


    /* =====================================================
       TRAILER PLAYER
       ===================================================== */

    .stVideo {

        border-radius: 14px;

        overflow: hidden;

        border: 1px solid #333;

        box-shadow:
            0 15px 40px
            rgba(0, 0, 0, 0.45);

        margin-top: 10px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 700px) {

        .block-container {

            padding-left: 12px;

            padding-right: 12px;
        }


        div[data-testid="stHorizontalBlock"] {

            padding:
                5px 3px;

            border-radius:
                14px;

            margin-bottom:
                7px;
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


        .section-title {

            font-size:
                25px;
        }


        .play-circle {

            width:
                45px;

            height:
                45px;

            font-size:
                18px;
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

        movies_data = pickle.load(
            file
        )


    with gzip.open(
        SIMILARITY_FILE,
        "rb"
    ) as file:

        similarity_data = pickle.load(
            file
        )


    return (
        movies_data,
        similarity_data["indices"]
    )


movies, similarity_indices = load_data()


# ============================================================
# 5. TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets[
    "TMDB_API_KEY"
]


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


    params["api_key"] = TMDB_API_KEY


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


    # --------------------------------------------------------
    # OFFICIAL YOUTUBE TRAILER
    # --------------------------------------------------------

    for video in videos:

        if (
            video.get("site")
            == "YouTube"

            and

            video.get("type")
            == "Trailer"

            and

            video.get("official")
            is True
        ):

            key = video.get(
                "key"
            )


            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


    # --------------------------------------------------------
    # ANY YOUTUBE TRAILER
    # --------------------------------------------------------

    for video in videos:

        if (
            video.get("site")
            == "YouTube"

            and

            video.get("type")
            == "Trailer"
        ):

            key = video.get(
                "key"
            )


            if key:

                return (
                    "https://www.youtube.com/watch?v="
                    + key
                )


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


    html = f"""
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


    return html


# ============================================================
# 12. DETAILS PAGE
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
                style="
                    width:100%;

                    height:420px;

                    border-radius:15px;

                    background-image:

                        linear-gradient(
                            to top,
                            #050505 0%,
                            rgba(5,5,5,0.15) 75%
                        ),

                        url('{backdrop_url}');

                    background-size:
                        cover;

                    background-position:
                        center;

                    border:
                        1px solid #292929;

                    box-shadow:
                        0 15px 45px
                        rgba(0,0,0,0.55);
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
    # POSTER + DETAILS
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

        st.subheader(
            "⭐ Rating"
        )


        st.metric(
            "TMDB Rating",
            f"{rating:.1f}/10"
        )


        st.divider()


        # ----------------------------------------------------
        # RELEASE DATE
        # ----------------------------------------------------

        st.subheader(
            "📅 Release Date"
        )


        st.write(
            release_date
        )


        # ----------------------------------------------------
        # RUNTIME
        # ----------------------------------------------------

        if runtime:

            st.divider()


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


            st.subheader(
                "⏱️ Runtime"
            )


            st.write(
                runtime_text
            )


        # ----------------------------------------------------
        # GENRES
        # ----------------------------------------------------

        if genres:

            st.divider()


            st.subheader(
                "🎭 Genres"
            )


            genre_names = []


            for genre in genres:

                name = genre.get(
                    "name"
                )


                if name:

                    genre_names.append(
                        name
                    )


            st.write(
                " • ".join(
                    genre_names
                )
            )


        # ----------------------------------------------------
        # STORY
        # ----------------------------------------------------

        st.divider()


        st.subheader(
            "📝 Story"
        )


        st.write(
            overview
        )


    # ========================================================
    # TRAILER
    # ========================================================

    st.divider()


    st.subheader(
        "▶️ Trailer"
    )


    trailer_url = fetch_trailer(
        movie_id
    )


    if trailer_url:

        st.video(
            trailer_url
        )

    else:

        st.info(
            "Trailer not available."
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

                    linear-gradient(
                        90deg,
                        #050505 0%,
                        #080808 50%,
                        rgba(5,5,5,0.5) 100%
                    );

                margin-bottom:40px;
            "
        >

            <div
                class="hero-content"
            >

                <div
                    style="
                        color:#e50914;

                        font-size:14px;

                        font-weight:900;

                        letter-spacing:4px;

                        margin-bottom:12px;
                    "
                >
                    DEVELOPED BY
                    ANISH-ABRAR-ABHISHEK-VISHAL
                </div>


                <div
                    style="
                        color:white;

                        font-size:
                            clamp(
                                36px,
                                6vw,
                                68px
                            );

                        font-weight:900;

                        line-height:1.05;

                        margin-bottom:18px;
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

    st.markdown(
        "## 🎥 Choose Your Movie"
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
    # RECOMMENDATIONS
    # ========================================================

    names, posters, ids = recommend(
        selected_movie
    )


    st.divider()


    st.markdown(
        f"""
        <div class="section-title">

            🔥 Recommended Movies

        </div>

        <div class="section-subtitle">

            Because you selected

            <b style="color:#ffffff;">
                {selected_movie}
            </b>

            <br>

            👆 Tap any poster to open
            movie details

        </div>
        """,
        unsafe_allow_html=True
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
                    color:#ffffff;

                    font-size:22px;

                    font-weight:800;
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
                Machine Learning &
                Web Application Project
            </div>

        </div>
        """
    )