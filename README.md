🎬 Movie Recommendation System

<p align="center">
  <b>Content-Based Movie Recommendation System using Machine Learning</b>
</p><p align="center">
  <a href="https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge">
  </a>
  <a href="https://github.com/Anish-kumar-00/movie-recommend-system">
    <img src="https://img.shields.io/badge/💻%20GitHub-Repository-black?style=for-the-badge&logo=github">
  </a>
</p>---

🎞️ Movie Showcase

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/en/3/39/Jawan_film_poster.jpg" width="145">
  <img src="https://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg" width="145">
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/RRR_Poster.jpg/220px-RRR_Poster.jpg" width="145">
  <img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f4/Welcome_poster_2007.jpg/220px-Welcome_poster_2007.jpg" width="145">
  <img src="https://upload.wikimedia.org/wikipedia/en/6/6f/Stanley_Ka_Dabba_Poster.jpg" width="145">
</p>---

✨ Features

- 🎬 Movie selection
- 🤖 Content-based recommendations
- ⭐ Top 5 similar movies
- 🖼️ TMDB movie posters
- ⚡ Precomputed similarity data
- 🌐 Streamlit web application

---

🧠 How It Works

Movie Dataset
     ↓
Data Cleaning & Feature Extraction
     ↓
Genres + Keywords + Cast + Director + Overview
     ↓
Tags + Stemming
     ↓
CountVectorizer
     ↓
Cosine Similarity
     ↓
Top 5 Similar Movies

---

🛠️ Tech Stack

Python • Pandas • NumPy • Scikit-learn • NLTK • Streamlit • TMDB API

---

📂 Project Structure

movie-recommend-system/
│
├── app.py
├── movies.pkl
├── similarity.pkl.gz
├── requirements.txt
└── README.md

---

🚀 Run Locally

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git
cd movie-recommend-system
pip install -r requirements.txt
streamlit run app.py

---

🔐 API Configuration

Create:

.streamlit/secrets.toml

Add:

TMDB_API_KEY = "YOUR_API_KEY"

The API key is loaded securely through Streamlit Secrets.

---

📌 Recommendation Method

This project uses Content-Based Filtering.

Movie information is converted into numerical vectors using "CountVectorizer", and similarity is calculated using Cosine Similarity.

---

🌐 Live Application

"🎬 Open Movie Recommendation System" (https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)

---

👨‍💻 Author

Anish Kumar

"GitHub" (https://github.com/Anish-kumar-00)

---

🎬 TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.