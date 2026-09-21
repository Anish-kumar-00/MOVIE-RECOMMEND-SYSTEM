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
    layout="wide"
)


# ============================================================
# 2. FILE PATHS
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
# 3. LOAD DATA
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
# 4. TMDB API KEY
# ============================================================

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]


# ============================================================
# 5. FETCH MOVIE DETAILS
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
        pass

    return None


# ============================================================
# 6. FETCH POSTER
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

    if poster_path:

        return (
            "https://image.tmdb.org/t/p/w500"
            + poster_path
        )

    return None


# ============================================================
# 7. FETCH TRAILER
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

        # ------------------------------------------
        # Official trailer
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
        # Any trailer
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
        pass

    return None


# ============================================================
# 8. RECOMMENDATION FUNCTION
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
# 9. MOVIE DETAILS PAGE
# ============================================================

def movie_details_page(movie_id):

    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    if st.button(
        "⬅️ Back to Recommendations"
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


    # --------------------------------------------------------
    # BACKDROP
    # --------------------------------------------------------

    if backdrop_path:

        backdrop_url = (
            "https://image.tmdb.org/t/p/original"
            + backdrop_path
        )

        st.image(
            backdrop_url,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.title(
        "🎬 " + title
    )


    # --------------------------------------------------------
    # POSTER + INFORMATION
    # --------------------------------------------------------

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
                "Poster not available."
            )


    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    with col2:

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


        st.divider()


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

            st.subheader(
                "⏱️ Runtime"
            )

            st.write(
                runtime_text
            )


        st.divider()


        # ----------------------------------------------------
        # GENRES
        # ----------------------------------------------------

        if genres:

            st.subheader(
                "🎭 Genres"
            )

            genre_names = []

            for genre in genres:

                genre_names.append(
                    genre.get("name", "")
                )

            st.write(
                " • ".join(genre_names)
            )


        st.divider()


        # ----------------------------------------------------
        # STORY
        # ----------------------------------------------------

        st.subheader(
            "📝 Story"
        )

        st.write(
            overview
        )


        st.divider()


        # ----------------------------------------------------
        # TRAILER
        # ----------------------------------------------------

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
# 10. CHECK MOVIE ID
# ============================================================

movie_id_from_url = st.query_params.get(
    "movie_id"
)


# ============================================================
# 11. DETAILS PAGE
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
# 12. MAIN PAGE
# ============================================================

else:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title(
        "🎬 CineMatch AI"
    )

    st.subheader(
        "Movie Recommendation System"
    )

    st.write(
        "Discover movies similar to your favourite movie."
    )


    st.divider()


    # --------------------------------------------------------
    # MOVIE SELECTOR
    # --------------------------------------------------------

    st.header(
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
        index=default_index
    )


    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    names, posters, ids = recommend(
        selected_movie
    )


    st.divider()


    st.header(
        "✨ Recommended Movies"
    )


    st.write(
        f"Movies similar to **{selected_movie}**"
    )


    # --------------------------------------------------------
    # MOVIE GRID
    # --------------------------------------------------------

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

            position = i + j


            if position >= len(names):
                continue


            name = names[position]

            poster = posters[position]

            movie_id = ids[position]


            with cols[j]:

                # --------------------------------------------
                # POSTER
                # --------------------------------------------

                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )


                # --------------------------------------------
                # MOVIE NAME
                # --------------------------------------------

                st.write(
                    f"**{name}**"
                )


                # --------------------------------------------
                # DETAILS BUTTON
                # --------------------------------------------

                if st.button(
                    "🎬 View Details",
                    key=f"details_{movie_id}_{position}",
                    use_container_width=True
                ):

                    st.query_params[
                        "movie_id"
                    ] = str(movie_id)

                    st.rerun()


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.divider()

    st.header(
        "👨‍💻 Developed By"
    )

    st.write(
        "Anish Kumar • Abhishek • Vishal"
    )

    st.write(
        "Machine Learning & Web Application Project"
    )

    st.caption(
        "🎬 CineMatch AI"
    )