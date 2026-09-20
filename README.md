🎬 Movie Recommendation System

<p align="center">🍿 Content-Based Movie Recommendation System

A Machine Learning based movie recommendation system that recommends movies similar to your favourite movie.

</p>---

🚀 Live Demo

<p align="center">👉 "🎬 Open Movie Recommendation System" (https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)

</p>---

🎞️ Popular Indian Movies

<p align="center"><a href="https://www.themoviedb.org/search/movie?query=Drishyam%202">
<img src="https://image.tmdb.org/t/p/w500/yJNNwHQuKYNeHFbsxSFR6yK9Dda.jpg" width="170" alt="Drishyam 2">
</a><a href="https://www.themoviedb.org/search/movie?query=Dangal">
<img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="170" alt="Dangal">
</a><a href="https://www.themoviedb.org/search/movie?query=3%20Idiots">
<img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="170" alt="3 Idiots">
</a><a href="https://www.themoviedb.org/search/movie?query=Jawan">
<img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="170" alt="Jawan">
</a><a href="https://www.themoviedb.org/search/movie?query=RRR">
<img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="170" alt="RRR">
</a></p><p align="center">Drishyam 2 • Dangal • 3 Idiots • Jawan • RRR

</p>«⚠️ Poster images are served from TMDB's image CDN. TMDB documents the image URL format as "base_url + file_size + file_path".»

---

✨ Features

- 🎬 Select your favourite movie
- 🤖 Content-Based Movie Recommendation
- 🔍 Find similar movies
- ⭐ Get top 5 recommendations
- 🖼️ Fetch movie posters using TMDB API
- ⚡ Fast recommendation using precomputed similarity data
- 🌐 Streamlit Web Application
- 📱 Mobile-friendly interface

---

🧠 How It Works

                 Movie Dataset
                      │
                      ▼
              Movies + Credits
                      │
                      ▼
                    Merge
                      │
                      ▼
        ┌─────────────────────────┐
        │ Genres                  │
        │ Keywords                │
        │ Cast                    │
        │ Director                │
        │ Overview                │
        └─────────────────────────┘
                      │
                      ▼
                    Tags
                      │
                      ▼
             Text Preprocessing
                      │
                      ▼
               CountVectorizer
                      │
                      ▼
             Feature Vectors
                      │
                      ▼
             Similarity Analysis
                      │
                      ▼
             Similar Movies
                      │
                      ▼
              Top 5 Recommendations

---

🔬 Recommendation Algorithm

This project uses Content-Based Filtering.

Each movie is represented using important textual information:

- 🎭 Genres
- 🔑 Keywords
- 👨‍🎤 Cast
- 🎬 Director
- 📝 Overview

These features are combined into a single "tags" column.

The text is then converted into numerical vectors using:

CountVectorizer()

After that, movie similarity is calculated using:

Cosine Similarity

The system finally returns the movies with the highest similarity.

---

🧮 Machine Learning Pipeline

Raw Data
   ↓
Data Cleaning
   ↓
Feature Extraction
   ↓
Feature Combination
   ↓
Text Preprocessing
   ↓
Stemming
   ↓
CountVectorizer
   ↓
Cosine Similarity
   ↓
Top Similar Movies

---

🛠️ Tech Stack

Technology| Purpose
🐍 Python| Programming
🐼 Pandas| Data Processing
🔢 NumPy| Numerical Operations
🤖 Scikit-learn| Machine Learning
📝 NLTK| Text Processing
🎨 Streamlit| Web Application
🎬 TMDB API| Movie Posters

---

📂 Project Structure

movie-recommend-system/
│
├── app.py
│
├── movies.pkl
│
├── similarity.pkl.gz
│
├── requirements.txt
│
└── README.md

---

📄 Important Files

"app.py"

Contains the complete Streamlit application.

It:

- Loads the processed movie dataset
- Loads compressed similarity data
- Takes the selected movie
- Finds similar movies
- Fetches posters from TMDB
- Displays recommendations

---

"movies.pkl"

Contains the processed movie DataFrame used by the recommendation system.

It contains information such as:

movie_id
title
overview
genres
keywords
cast
crew
tags

---

"similarity.pkl.gz"

Contains the compressed precomputed recommendation information.

Instead of storing the complete large similarity matrix, the project stores the most relevant movie indices and scores.

This keeps the deployment file much smaller.

---

🔑 TMDB API

The application uses TMDB to fetch movie poster images.

The API key is not stored directly inside "app.py".

It is loaded using Streamlit Secrets:

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

For Streamlit deployment, add:

TMDB_API_KEY = "YOUR_API_KEY"

to the application's Secrets section.

TMDB supports movie searching and returns fields such as "poster_path", which can then be converted into a full image URL.

---

🚀 Run Locally

1️⃣ Clone the Repository

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git

cd movie-recommend-system

---

2️⃣ Install Dependencies

pip install -r requirements.txt

---

3️⃣ Add TMDB API Key

Create:

.streamlit/secrets.toml

and add:

TMDB_API_KEY = "YOUR_API_KEY"

---

4️⃣ Run Streamlit

streamlit run app.py

---

📦 Requirements

streamlit
pandas
numpy
scikit-learn
requests

---

🌐 Deployment

This project can be deployed using:

Streamlit Community Cloud

Deployment flow:

GitHub Repository
       ↓
Streamlit Community Cloud
       ↓
app.py
       ↓
movies.pkl
       ↓
similarity.pkl.gz
       ↓
Live Web Application

---

🔐 Security

The TMDB API key should never be uploaded directly to GitHub.

Use:

st.secrets["TMDB_API_KEY"]

instead of:

TMDB_API_KEY = "YOUR_SECRET_KEY"

---

🎯 Future Improvements

Possible improvements:

- 🔎 Movie Search
- 🎭 Genre Filtering
- 📅 Release Year Filtering
- ⭐ Rating Display
- 📖 Movie Details
- 👨‍🎤 Cast Information
- 🎬 Trailer Integration
- ❤️ Favourite Movies
- 🎨 Better UI
- 📱 Improved Mobile Layout
- 🔥 Popular Movies Section

---

📊 Example

Suppose the user selects:

3 Idiots

The system searches the precomputed similarity data and returns movies having similar content/features.

Example output:

🎬 Recommended Movies

1. Movie A
2. Movie B
3. Movie C
4. Movie D
5. Movie E

The actual recommendations are generated by the trained/precomputed data.

---

🧑‍💻 Author

Anish Kumar

GitHub:

👉 "Anish-kumar-00" (https://github.com/Anish-kumar-00)

---

⭐ Support

If you found this project useful, consider giving the repository a ⭐.

<p align="center">🎬 Happy Movie Discovering! 🍿

</p>---

🎬 TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.

TMDB's documentation states that applications using its API/data should provide the required attribution.