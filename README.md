🎬 Movie Recommendation System

<p align="center">
  <b>Content-Based Movie Recommendation System using Machine Learning</b>
</p><p align="center">
  <a href="https://movie-recommend-system-7gxlqk2bwnstctskpdpuyf.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge">
  </a>
  <a href="https://github.com/Anish-kumar-00/movie-recommend-system">
    <img src="https://img.shields.io/badge/💻%20GitHub-Repository-black?style=for-the-badge&logo=github">
  </a>
</p>---

🎞️ Movie Showcase

<p align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://upload.wikimedia.org/wikipedia/en/3/39/Jawan_film_poster.jpg" width="220"><br><br>
        <b>Jawan</b>
      </td>  <td align="center">
    <img src="https://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg" width="220"><br><br>
    <b>3 Idiots</b>
  </td>

  <td align="center">
    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/RRR_Poster.jpg/330px-RRR_Poster.jpg" width="220"><br><br>
    <b>RRR</b>
  </td>

  <td align="center">
    <img src="https://commons.wikimedia.org/wiki/Special:FilePath/Welcome_poster_2007.jpg?width=400" width="220"><br><br>
    <b>Welcome</b>
  </td>

  <td align="center">
    <img src="https://upload.wikimedia.org/wikipedia/en/6/6f/Stanley_Ka_Dabba_Poster.jpg" width="220"><br><br>
    <b>Stanley Ka Dabba</b>
  </td>
</tr>

  </table>
</p>---

✨ Features

- 🎬 Select a movie
- 🤖 Content-Based Recommendation
- ⭐ Top 5 similar movies
- 🖼️ TMDB movie posters
- ⚡ Precomputed similarity
- 🌐 Streamlit Web Application
- 🔐 Secure API configuration

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

📌 Recommendation Method

This project uses Content-Based Filtering.

Movie features such as genres, keywords, cast, director, and overview are combined into a "tags" feature.

"CountVectorizer" converts the text into numerical vectors, and Cosine Similarity is used to find similar movies.

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

The API key is loaded securely using Streamlit Secrets.

---

🌐 Live Demo

<p align="center">
  <a href="https://movie-recommend-system-7gxlqk2bwnstctskpdpuyf.streamlit.app/">
    <img src="https://img.shields.io/badge/🎬%20Open%20Movie%20Recommendation%20System-red?style=for-the-badge">
  </a>
</p>---

👨‍💻 Author

Anish Kumar

<p align="center">
  <a href="https://github.com/Anish-kumar-00">
    <img src="https://img.shields.io/badge/GitHub-Anish--kumar--00-black?style=for-the-badge&logo=github">
  </a>
</p>---

🎬 TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.