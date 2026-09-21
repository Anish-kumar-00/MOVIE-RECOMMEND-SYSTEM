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
# 2. CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(255, 0, 80, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(80, 30, 180, 0.12),
            transparent 30%
        ),
        #08090d;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-container {
    text-align: center;
    padding: 35px 20px;
    margin-bottom: 30px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(255, 20, 70, 0.16),
            rgba(100, 30, 180, 0.14)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 15px 50px rgba(0,0,0,0.35);
}


.hero-title {
    font-size: 48px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            white,
            #ff416c,
            #ff4b2b,
            white
        );

    background-size: 300%;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: gradientMove 5s linear infinite;
}


.hero-subtitle {
    margin-top: 10px;
    font-size: 18px;
    color: #bdbdbd;
}


@keyframes gradientMove {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }

}


/* ============================================================
   MOVIE POSTERS
   ============================================================ */

[data-testid="stImage"] img {

    border-radius: 14px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.45);

    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease;
}


[data-testid="stImage"] img:hover {

    transform: translateY(-6px) scale(1.03);

    box-shadow:
        0 15px 35px
        rgba(255,60,100,0.25);
}


/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background: #171920 !important;

    border:
        1px solid
        rgba(255,255,255,0.10) !important;

    border-radius: 12px !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    width: 100%;

    border: none;

    border-radius: 10px;

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


/* ============================================================
   MOVIE NAME
   ============================================================ */

.movie-name {

    text-align: center;

    font-size: 15px;

    font-weight: 700;

    color: white;

    min-height: 42px;

    padding-top: 8px;

    padding-bottom: 5px;
}


/* ============================================================
   DETAILS PAGE
   ============================================================ */

.details-title {

    font-size: 45px;

    font-weight: 900;

    margin-bottom: 20px;
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


.rating-box {

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


/* ============================================================
   FOOTER
   ============================================================ */

.footer-box {

    text-align: center;

    margin-top: 50px;

    padding: 30px;

    border-top:
        1px solid
        rgba(255,255,255,0.08);

    color: #999;
}


.footer-name {

    color: white;

    font-size: 20px;

    font-weight: 800;
}


/* ============================================================
   MOBILE
   ============================================================ */

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
""", unsafe_allow_html=True)


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
# 5. TMDB API
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# 6. MOVIE DETAILS
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
# 7. POSTER
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
# 8. TRAILER
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
# 9. RECOMMENDATION
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
# 10. MOVIE DETAILS PAGE
# ============================================================

def movie_details_page(movie_id):

    if st.button(
        "⬅️ Back to Recommendations",
        key="back"
    ):

        st.query_params.clear()

        st.rerun()


    st.divider()


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

        st.image(
            backdrop_url,
            use_container_width=True
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

    col1, col2 = st.columns(
        [1, 2],
        gap="large"
    )


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


    with col2:

        # Rating

        st.markdown(
            f"""
            <div class="detail-box">

                <span class="rating-box">
                    ⭐ {rating:.1f}/10
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Release date

        st.markdown(
            f"""
            <div class="detail-box">

                <b>📅 Release Date</b>

                <br><br>

                {release_date}

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

                    <b>⏱️ Runtime</b>

                    <br><br>

                    {runtime_text}

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
                <div class="detail-box">

                    <b>🎭 Genres</b>

                    <br><br>

                    {genre_text}

                </div>
                """,
                unsafe_allow_html=True
            )


        # Story

        st.markdown(
            f"""
            <div class="detail-box">

                <b>📝 Story</b>

                <br><br>

                {overview}

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
# 11. CHECK MOVIE DETAILS URL
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
        <div class="hero-container">
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


    st.caption(
        "Choose a movie and open its details."
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

                # Poster

                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )


                # Movie name

                st.markdown(
                    f"""
                    <div class="movie-name">
                        {name}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # Details button

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

    st.divider()

    st.markdown(
        """
        <div class="footer-box">

            <div class="footer-name">
                👨‍💻 Developed By
            </div>

            <br>

            Anish Kumar • Abhishek • Vishal

            <br><br>

            Machine Learning & Web Application Project

            <br><br>

            🎬 CineMatch AI

        </div>
        """,
        unsafe_allow_html=True
    )