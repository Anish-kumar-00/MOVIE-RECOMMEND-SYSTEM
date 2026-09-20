🎬 Movie Recommendation System

«🍿 A Content-Based Movie Recommendation System built using Python, Machine Learning and Streamlit.»

🚀 Live Demo

👉 "Open Movie Recommendation System" (https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)

---

🎬 Popular Indian Movies

<p align="center"><img src="https://image.tmdb.org/t/p/w500/yJNNwHQuKYNeHFbsxSFR6yK9Dda.jpg" width="180" alt="Drishyam 2"><img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="180" alt="Indian Movie"><img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="180" alt="Indian Movie"><img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="180" alt="Indian Movie"><img src="https://image.tmdb.org/t/p/w500/1E5baAaEse26fej7uHcjOgEE2t2.jpg" width="180" alt="Indian Movie"></p><p align="center"><b>Drishyam 2</b>    
<b>Dangal</b>    
<b>3 Idiots</b>    
<b>Jawan</b>    
<b>RRR</b>

</p>---

✨ Features

- 🎬 Select your favourite movie
- 🤖 Content-Based Recommendation
- 🔍 Find similar movies
- ⭐ Get 5 movie recommendations
- 🖼️ Movie posters using TMDB API
- ⚡ Fast recommendations
- 🌐 Streamlit Web Application

---

🧠 How It Works

Movies + Credits
       ↓
     Merge
       ↓
Genres + Keywords + Cast + Director + Overview
       ↓
      Tags
       ↓
Text Preprocessing
       ↓
CountVectorizer
       ↓
Cosine Similarity
       ↓
Similar Movies
       ↓
Top 5 Recommendations

---

🔬 Recommendation Method

This project uses Content-Based Filtering.

Movie features such as:

- 🎭 Genres
- 🔑 Keywords
- 👨‍🎤 Cast
- 🎬 Director
- 📝 Overview

are combined into a "tags" feature.

"CountVectorizer" converts the text into numerical vectors.

Then Cosine Similarity is used to find similar movies.

---

🛠️ Tech Stack

Technology| Used For
🐍 Python| Programming
🐼 Pandas| Data Processing
🔢 NumPy| Numerical Operations
🤖 Scikit-learn| Machine Learning
📝 NLTK| Text Processing
🎨 Streamlit| Web App
🎬 TMDB API| Movie Posters

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

📄 Project Files

"app.py"

Main Streamlit application.

"movies.pkl"

Processed movie dataset used by the recommendation system.

"similarity.pkl.gz"

Compressed precomputed similarity/recommendation indices.

"requirements.txt"

Contains the Python libraries required to run the project.

---

🚀 Run Locally

Clone Repository

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git
cd movie-recommend-system

Install Dependencies

pip install -r requirements.txt

Run Application

streamlit run app.py

---

🔑 TMDB API

This project uses the TMDB API to fetch movie posters.

The API key is kept private using Streamlit Secrets.

TMDB_API_KEY = "YOUR_API_KEY"

---

🎯 Future Improvements

- 🔎 Movie Search
- ⭐ Movie Ratings
- 🎭 Genre Filtering
- 📅 Release Year Filtering
- 📖 Detailed Movie Information
- 👤 Personalized Recommendations
- 🎨 Improved User Interface
- 🔥 Popular Indian Movies Section

---

👨‍💻 Author

Anish Kumar

🔗 "GitHub" (https://github.com/Anish-kumar-00)

---

⭐ Support

If you like this project, please consider giving the repository a ⭐.

🎬 Happy Movie Discovering! 🍿

---

🎬 TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.