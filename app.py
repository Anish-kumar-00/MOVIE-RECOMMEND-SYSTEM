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
# 2. GLOBAL STYLE
# ============================================================

st.html(
    """
    <style>

    /* =========================================
       MAIN APP
       ========================================= */

    .stApp {
        background: #050505;
        color: white;
    }


    /* Main content width */

    .block-container {
        max-width: 1500px;
        padding-top: 25px;
        padding-bottom: 40px;
    }


    /* =========================================
       SELECTBOX
       ========================================= */

    div[data-baseweb="select"] > div {
        background-color: #181818 !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        color: white !important;
    }


    /* =========================================
       NORMAL BUTTONS
       ========================================= */

    .stButton > button {
        background-color: #e50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: 700 !important;
    }


    .stButton > button:hover {
        background-color: #f40612 !important;
    }


    /* =========================================
       LINK BUTTON
       ========================================= */

    .stLinkButton > a {
        background-color: #e50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }


    /* =========================================
       DIVIDER
       ========================================= */

    hr {
        border-color: #292929 !important;
    }


    /* =========================================
       MOVIE CARD
       ========================================= */

    .movie-card {
        position: relative;
        overflow: hidden;
        border-radius: 8px;
        background: #181818;
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }


    .movie-card:hover {
        transform: scale(1.06);
        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.75);
        z-index: 10;
    }


    .movie-card-image {
        width: 100%;
        aspect-ratio: 2 / 3;
        object-fit: cover;
        display: block;
        transition:
            transform 0.35s ease,
            filter 0.35s ease;
    }


    .movie-card:hover .movie-card-image {
        transform: scale(1.08);
        filter: brightness(0.65);
    }


    .movie-card-overlay {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;

        display: flex;
        align-items: center;
        justify-content: center;

        opacity: 0;

        background:
            linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0.05),
                rgba(0, 0, 0, 0.80)
            );

        transition: opacity 0.3s ease;
    }


    .movie-card:hover .movie-card-overlay {
        opacity: 1;
    }


    .play-button {
        width: 55px;
        height: 55px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #e50914;
        color: white;

        border-radius: 50%;

        font-size: 22px;
        font-weight: bold;

        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.5);
    }


    .movie-title {
        margin-top: 8px;
        margin-bottom: 20px;

        color: white;

        font-size: 14px;
        font-weight: 700;

        text-align: center;

        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }


    /* =========================================
       MOBILE
       ========================================= */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 12px;
            padding-right: 12px;
        }

        .movie-card:hover {
            transform: none;
        }

        .movie-card:hover .movie-card-image {
            transform: none;
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

    with open(MOVIES_FILE, "rb") as file:

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
# 6. TMDB REQUEST HELPER
# ============================================================

def tmdb_request(endpoint, params=None):

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
# 7. FETCH MOVIE DETAILS
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
# 8. FETCH POSTER
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
# 9. FETCH TRAILER
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
    # First priority: official YouTube trailer
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
    # Second priority: any YouTube trailer
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


    return None


# ============================================================
# 10. RECOMMEND MOVIES
# ============================================================

def recommend(movie):

    movie_indexes = movies[
        movies["title"] == movie
    ].index


    if len(movie_indexes) == 0:

        return [], [], []


    index = movie_indexes[0]


    names = []
    posters = []
    ids = []


    # First 20 similar movies

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
# 11. MOVIE CARD
# ============================================================

def movie_card_html(
    movie_name,
    poster_url,
    movie_id
):

    # --------------------------------------------------------
    # Fallback poster
    # --------------------------------------------------------

    if not poster_url:

        poster_url = (
            "https://via.placeholder.com/"
            "500x750?text=No+Poster"
        )


    # --------------------------------------------------------
    # IMPORTANT:
    #
    # No CSS block inside this f-string.
    # Therefore previous transform syntax error
    # cannot happen here.
    # --------------------------------------------------------

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

        <div class="movie-card">

            <img
                class="movie-card-image"
                src="{poster_url}"
                alt="{movie_name}"
            >

            <div class="movie-card-overlay">

                <div class="play-button">
                    ▶
                </div>

            </div>

        </div>


        <div class="movie-title">
            {movie_name}
        </div>

    </a>
    """


    return html


# ============================================================
# 12. DETAILS PAGE
# ============================================================

def show_movie_details(movie_id):

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
    # MOVIE DETAILS
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
    # MOVIE BACKDROP
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
                    height:400px;

                    border-radius:12px;

                    background-image:
                        linear-gradient(
                            to top,
                            #050505 0%,
                            rgba(5,5,5,0.15) 70%
                        ),
                        url('{backdrop_url}');

                    background-size:cover;
                    background-position:center;
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

    poster_column, info_column = st.columns(
        [1, 2],
        gap="large"
    )


    # ========================================================
    # POSTER
    # ========================================================

    with poster_column:

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

    with info_column:

        st.subheader(
            "⭐ Rating"
        )


        st.metric(
            "TMDB Rating",
            f"{rating:.1f}/10"
        )


        st.divider()


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

                genre_name = genre.get(
                    "name"
                )


                if genre_name:

                    genre_names.append(
                        genre_name
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


        # ----------------------------------------------------
        # TRAILER
        # ----------------------------------------------------

        st.divider()


        st.subheader(
            "▶️ Trailer"
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
                "Trailer not available."
            )


# ============================================================
# 13. CHECK URL
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 14. MOVIE DETAILS PAGE
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
    # HERO SECTION
    # ========================================================

    st.html(
        """
        <div
            style="
                min-height:380px;

                display:flex;
                align-items:flex-end;

                padding:45px;

                border-radius:14px;

                background:
                    linear-gradient(
                        90deg,
                        #050505 0%,
                        #090909 45%,
                        rgba(5,5,5,0.55) 100%
                    );

                box-shadow:
                    0 20px 60px
                    rgba(0,0,0,0.65);

                margin-bottom:35px;
            "
        >

            <div>

                <div
                    style="
                        color:#e50914;
                        font-size:14px;
                        font-weight:800;
                        letter-spacing:3px;
                        margin-bottom:10px;
                    "
                >
                    🎬 MOVIE RECOMMENDATION
                </div>


                <div
                    style="
                        color:white;
                        font-size:clamp(
                            34px,
                            6vw,
                            64px
                        );
                        font-weight:900;
                        line-height:1.05;
                        margin-bottom:15px;
                    "
                >
                    Movie Recommendation System
                </div>


                <div
                    style="
                        color:#bdbdbd;
                        font-size:17px;
                        max-width:650px;
                        line-height:1.6;
                    "
                >
                    Discover movies you will love
                    with AI-powered recommendations.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # CHOOSE MOVIE
    # ========================================================

    st.header(
        "🎥 Choose Your Movie"
    )


    movie_list = movies[
        "title"
    ].values


    # --------------------------------------------------------
    # Avatar as default
    # --------------------------------------------------------

    default_index = 0


    if "Avatar" in movie_list:

        default_index = list(
            movie_list
        ).index("Avatar")


    selected_movie = st.selectbox(
        "Select a movie",
        movie_list,
        index=default_index
    )


    # ========================================================
    # GET RECOMMENDATIONS
    # ========================================================

    names, posters, ids = recommend(
        selected_movie
    )


    st.divider()


    # ========================================================
    # RECOMMENDATION HEADER
    # ========================================================

    st.header(
        "🔥 Recommended Movies"
    )


    st.write(
        f"Movies similar to **{selected_movie}**"
    )


    st.caption(
        "👆 Tap any movie poster to view complete details."
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

        columns = st.columns(
            COLS_PER_ROW,
            gap="small"
        )


        for column_number in range(
            COLS_PER_ROW
        ):

            movie_position = (
                row_start
                + column_number
            )


            if movie_position >= len(names):

                continue


            with columns[column_number]:

                card = movie_card_html(
                    names[movie_position],
                    posters[movie_position],
                    ids[movie_position]
                )


                st.html(
                    card
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
                padding:35px 10px;
                color:#777;
            "
        >

            <div
                style="
                    color:white;
                    font-size:21px;
                    font-weight:800;
                "
            >
                🎬 Movie Recommendation System
            </div>


            <div
                style="
                    margin-top:12px;
                    color:#999;
                "
            >
                Developed By
            </div>


            <div
                style="
                    margin-top:7px;
                    color:#cccccc;
                    font-size:16px;
                    font-weight:600;
                "
            >
                Anish Kumar • Abhishek • Vishal
            </div>


            <div
                style="
                    margin-top:15px;
                    font-size:12px;
                    color:#666;
                "
            >
                Machine Learning & Web Application Project
            </div>

        </div>
        """
    )