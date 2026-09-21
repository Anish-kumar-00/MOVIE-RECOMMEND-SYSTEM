import gzip
import os
import pickle
import requests
import streamlit as st


# ============================================================
# 1. PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. GLOBAL STREAMLIT STYLE
# ============================================================

st.html("""
<style>

    /* Main background */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #050505 0%,
                #0b0b0b 45%,
                #050505 100%
            );
        color: white;
    }


    /* Remove extra top space */

    .block-container {
        padding-top: 1rem;
        max-width: 1600px;
    }


    /* Selectbox */

    div[data-baseweb="select"] > div {
        background-color: #181818 !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
    }


    /* Normal Streamlit buttons */

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


    /* Link button */

    .stLinkButton > a {
        background-color: #e50914 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }


    /* Divider */

    hr {
        border-color: #292929 !important;
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
# 8. FETCH BACKDROP
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def fetch_backdrop(movie_id):

    details = fetch_movie_details(movie_id)

    if not details:
        return None

    backdrop_path = details.get(
        "backdrop_path"
    )

    if backdrop_path:

        return (
            "https://image.tmdb.org/t/p/original"
            + backdrop_path
        )

    return None


# ============================================================
# 9. FETCH TRAILER
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

        if response.status_code != 200:
            return None

        videos = response.json().get(
            "results",
            []
        )

        # Official trailer

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


        # Any trailer

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
# 10. RECOMMENDATION
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

    return names, posters, ids


# ============================================================
# 11. MOVIE CARD HTML
# ============================================================

def movie_card_html(
    movie_name,
    poster_url,
    movie_id
):

    if not poster_url:

        poster_url = (
            "https://via.placeholder.com/500x750"
            "?text=No+Poster"
        )


    return f"""
    <a
        href="?movie_id={movie_id}"
        target="_self"
        style="
            text-decoration:none;
            color:white;
            display:block;
        "
    >

        <div
            class="movie-card"
            style="
                position:relative;
                overflow:hidden;
                border-radius:7px;
                background:#181818;
                transition:
                    transform 0.3s ease,
                    box-shadow 0.3s ease;
            "
        >

            <img
                src="{poster_url}"
                style="
                    width:100%;
                    aspect-ratio:2/3;
                    object-fit:cover;
                    display:block;
                    transition:
                        transform 0.4s ease,
                        filter 0.4s ease;
                "
            >


            <div
                class="movie-overlay"
                style="
                    position:absolute;
                    inset:0;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    opacity:0;
                    background:
                        linear-gradient(
                            rgba(0,0,0,0.15),
                            rgba(0,0,0,0.80)
                        );
                    transition:opacity 0.3s ease;
                "
            >

                <div
                    style="
                        background:#e50914;
                        padding:10px 15px;
                        border-radius:50%;
                        font-size:20px;
                    "
                >
                    ▶
                </div>

            </div>

        </div>


        <div
            style="
                padding-top:8px;
                padding-bottom:18px;
                font-size:14px;
                font-weight:600;
                color:#ffffff;
                white-space:nowrap;
                overflow:hidden;
                text-overflow:ellipsis;
            "
        >
            {movie_name}
        </div>

    </a>


    <style>

        .movie-card:hover {

            transform:
                scale(1.06);

            box-shadow:
                0 15px 40px
                rgba(0,0,0,0.75);

            z-index:5;
        }


        .movie-card:hover img {

            transform:
                scale(1.08);

            filter:
                brightness(0.65);
        }


        .movie-card:hover
        .movie-overlay {

            opacity:1;
        }

    </style>
    """


# ============================================================
# 12. MOVIE DETAILS PAGE
# ============================================================

def movie_details_page(movie_id):

    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    if st.button(
        "← Back",
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

    poster_path = details.get(
        "poster_path"
    )

    backdrop_path = details.get(
        "backdrop_path"
    )


    # ========================================================
    # DETAILS HERO
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
                    height:420px;
                    border-radius:12px;
                    background:
                        linear-gradient(
                            to top,
                            #080808 5%,
                            rgba(0,0,0,0.1)
                        ),
                        url('{backdrop_url}');
                    background-size:cover;
                    background-position:center;
                    margin-top:15px;
                    margin-bottom:25px;
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
                "Poster unavailable"
            )


    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    with col2:

        st.metric(
            "⭐ Rating",
            f"{rating:.1f}/10"
        )


        st.divider()


        st.subheader(
            "📅 Release Date"
        )

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

            st.subheader(
                "⏱️ Runtime"
            )

            st.write(
                runtime_text
            )


        if genres:

            st.divider()

            st.subheader(
                "🎭 Genres"
            )

            genre_names = [
                genre.get("name", "")
                for genre in genres
            ]

            st.write(
                " • ".join(genre_names)
            )


        st.divider()


        st.subheader(
            "📝 Story"
        )

        st.write(
            overview
        )


        st.divider()


        st.subheader(
            "▶️ Trailer"
        )


        trailer_url = fetch_trailer(
            movie_id
        )


        if trailer_url:

            st.link_button(
                "▶️ Watch Trailer",
                trailer_url,
                use_container_width=True
            )

        else:

            st.info(
                "Trailer not available."
            )


# ============================================================
# 13. CHECK DETAILS URL
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

        movie_details_page(
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
    # NETFLIX STYLE HERO
    # ========================================================

    st.html("""
    <div
        style="
            position:relative;
            min-height:360px;
            border-radius:12px;
            overflow:hidden;
            margin-bottom:30px;

            background:
                linear-gradient(
                    90deg,
                    #050505 0%,
                    rgba(5,5,5,0.85) 35%,
                    rgba(5,5,5,0.20) 75%,
                    #050505 100%
                );
        "
    >

        <div
            style="
                position:absolute;
                bottom:45px;
                left:35px;
                max-width:600px;
            "
        >

            <div
                style="
                    color:#e50914;
                    font-size:14px;
                    font-weight:800;
                    letter-spacing:2px;
                "
            >
                NETFLIX STYLE
            </div>


            <div
                style="
                    color:white;
                    font-size:clamp(32px,5vw,65px);
                    font-weight:900;
                    margin-top:8px;
                "
            >
                Movie Recommendation System
            </div>


            <div
                style="
                    color:#d0d0d0;
                    font-size:18px;
                    margin-top:12px;
                "
            >
                Discover movies similar to
                your favourite movies.
            </div>

        </div>

    </div>
    """)


    # ========================================================
    # SELECT MOVIE
    # ========================================================

    st.subheader(
        "🎬 Choose a Movie"
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


    st.header(
        "🔥 Recommended Movies"
    )


    st.caption(
        f"Because you selected {selected_movie}"
    )


    # ========================================================
    # MOVIE GRID
    # ========================================================

    # 5 columns on desktop
    # Streamlit will stack them on smaller screens

    COLS_PER_ROW = 5


    for i in range(
        0,
        len(names),
        COLS_PER_ROW
    ):

        cols = st.columns(
            COLS_PER_ROW,
            gap="small"
        )


        for j in range(
            COLS_PER_ROW
        ):

            position = i + j


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


    st.html("""
    <div
        style="
            text-align:center;
            padding:30px 10px;
            color:#777;
        "
    >

        <div
            style="
                color:white;
                font-size:20px;
                font-weight:800;
            "
        >
            🎬 Movie Recommendation System
        </div>

        <div style="margin-top:10px;">
            Developed By
        </div>

        <div
            style="
                color:#aaa;
                margin-top:5px;
            "
        >
            Anish Kumar • Abhishek • Vishal
        </div>

        <div
            style="
                margin-top:15px;
                font-size:12px;
            "
        >
            Machine Learning & Web Application Project
        </div>

    </div>
    """)