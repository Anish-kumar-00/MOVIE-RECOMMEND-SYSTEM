🎬 Movie Recommendation System

<p align="center">🍿 Movie Recommendation System

🤖 Content-Based Movie Recommendation using Machine Learning

</p><p align="center"><a href="https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/">
<img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge">
</a><a href="https://github.com/Anish-kumar-00/movie-recommend-system">
<img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github">
</a></p>---

🎬 Movie Showcase

<p align="center"><img src="https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/RRR_Poster.jpg/220px-RRR_Poster.jpg" width="160" alt="RRR"><img src="https://upload.wikimedia.org/wikipedia/en/3/39/Jawan_film_poster.jpg" width="160" alt="Jawan"><img src="https://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg" width="160" alt="3 Idiots"><img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Welcome_poster_2007.jpg/220px-Welcome_poster_2007.jpg" width="160" alt="Welcome"><img src="https://upload.wikimedia.org/wikipedia/en/6/6f/Stanley_Ka_Dabba_Poster.jpg" width="160" alt="Stanley Ka Dabba"></p><p align="center">RRR • Jawan • 3 Idiots • Welcome • Stanley Ka Dabba

</p>---

🚀 Live Demo

<p align="center">👉 "🎬 Open the Movie Recommendation System" (https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)

</p>---

✨ Features

- 🎬 Select your favourite movie
- 🤖 Content-Based Recommendation
- 🔍 Find similar movies
- ⭐ Get Top 5 recommendations
- 🖼️ Fetch movie posters using TMDB API
- ⚡ Fast recommendations
- 🌐 Streamlit Web Application
- 📦 Precomputed similarity data
- 🔐 API key protected using Streamlit Secrets

---

🧠 How It Works

                🎬 Movie Dataset
                       │
                       ▼
              Movies + Credits
                       │
                       ▼
                     Merge
                       │
                       ▼
        ┌────────────────────────────┐
        │ Genres                     │
        │ Keywords                   │
        │ Cast                       │
        │ Director                   │
        │ Overview                   │
        └────────────────────────────┘
                       │
                       ▼
                     Tags
                       │
                       ▼
              Text Preprocessing
                       │
                       ▼
                 Stemming
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

🔬 Recommendation System

This project uses Content-Based Filtering.

The recommendation system uses information about each movie such as:

- 🎭 Genres
- 🔑 Keywords
- 👨‍🎤 Cast
- 🎬 Director
- 📝 Overview

All these features are combined into a single "tags" column.

The text is then converted into numerical vectors using:

CountVectorizer()

Movie similarity is calculated using:

Cosine Similarity

The system then selects the most similar movies.

---

🧮 Machine Learning Pipeline

Raw CSV Data
     ↓
Data Cleaning
     ↓
Merge Movies + Credits
     ↓
Feature Extraction
     ↓
Create Tags
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
     ↓
Recommendation

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

📄 Project Files

"app.py"

Main Streamlit application.

It handles:

- Movie selection
- Recommendation generation
- TMDB poster fetching
- User interface

---

"movies.pkl"

Contains the processed movie DataFrame.

The processed data contains information such as:

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

Contains compressed precomputed recommendation information.

Instead of storing the complete large similarity matrix, this project stores the most relevant movie indices and similarity scores.

This makes the deployment file much smaller.

---

"requirements.txt"

Contains the libraries required to run the application.

streamlit
pandas
numpy
scikit-learn
requests

---

🔑 TMDB API

The application uses the TMDB API to fetch movie posters.

The API key is not hardcoded in "app.py".

The application reads it from Streamlit Secrets:

TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

TMDB's official documentation describes movie search responses containing "poster_path", which can be combined with the TMDB image base URL and size to create a poster URL.

---

🔐 Streamlit Secrets

For deployment, add the following to Streamlit Secrets:

TMDB_API_KEY = "YOUR_API_KEY"

Never upload the real API key to GitHub.

---

🚀 Run Locally

1️⃣ Clone the Repository

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git

cd movie-recommend-system

---

2️⃣ Install Dependencies

pip install -r requirements.txt

---

3️⃣ Add API Key

Create:

.streamlit/secrets.toml

Add:

TMDB_API_KEY = "YOUR_API_KEY"

---

4️⃣ Run the Application

streamlit run app.py

---

🌐 Deployment

The project is deployed using Streamlit Community Cloud.

GitHub Repository
        ↓
   Streamlit Cloud
        ↓
      app.py
        ↓
   movies.pkl
        ↓
 similarity.pkl.gz
        ↓
    TMDB API
        ↓
🎬 Movie Recommendations

---

🎯 Example

Suppose the user selects:

3 Idiots

The system searches the precomputed similarity information and returns the top similar movies.

🎬 Recommended Movies

1. Movie A
2. Movie B
3. Movie C
4. Movie D
5. Movie E

The actual recommendations are generated from the processed movie data.

---

📈 Future Improvements

- 🔎 Movie Search
- 🎭 Genre Filtering
- 📅 Release Year Filtering
- ⭐ Movie Ratings
- 📖 Movie Details
- 👨‍🎤 Cast Information
- 🎞️ Trailer Integration
- ❤️ Favourite Movies
- 🎨 Improved UI
- 📱 Better Mobile Layout
- 🔥 Popular Movies Section

---

👨‍💻 Author

Anish Kumar

<p align="center"><a href="https://github.com/Anish-kumar-00"><img src="https://img.shields.io/badge/GitHub-Anish--kumar--00-black?style=for-the-badge&logo=github"></a></p>---

⭐ Support

If you like this project, please consider giving the repository a ⭐.

<p align="center">🎬 Happy Movie Discovering! 🍿

</p>---

🎬 TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.