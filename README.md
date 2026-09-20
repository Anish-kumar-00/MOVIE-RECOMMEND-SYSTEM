🎬 Movie Recommendation System

«🍿 A Content-Based Movie Recommendation System built using Python, Machine Learning and Streamlit.»

🚀 Live Demo

👉 "Open Movie Recommendation System" (https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)

---

🎥 Popular Indian Movies

🎬 Drishyam 2| 🏆 Dangal| 🤝 3 Idiots| 🔥 Jawan| ⚔️ RRR
<img src="https://image.tmdb.org/t/p/w500/7G4s0j3B8qG7QJz5h8Y8x6G4Q7m.jpg" width="150">| <img src="https://image.tmdb.org/t/p/w500/1P7w3A6z5Y5Y5Y5Y5Y5Y5Y5Y5Y.jpg" width="150">| <img src="https://image.tmdb.org/t/p/w500/6U2FQq0q3j4j5j6j7j8j9j0j1j.jpg" width="150">| <img src="https://image.tmdb.org/t/p/w500/j9v6G7j8K9L0M1N2O3P4Q5R6S7T.jpg" width="150">| <img src="https://image.tmdb.org/t/p/w500/nE3J2R7G8Y9X0W1V2U3T4S5R6Q.jpg" width="150">

---

✨ Features

- 🎬 Select your favourite movie
- 🤖 Content-Based Recommendation
- 🔍 Find similar movies
- ⭐ Get 5 movie recommendations
- 🖼️ Movie posters using TMDB API
- ⚡ Fast recommendations
- 🌐 Streamlit Web App

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

Movie-Recommendation/
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

Processed movie dataset created from the original movie data.

"similarity.pkl.gz"

Precomputed similarity/recommendation indices.

"requirements.txt"

Contains the Python libraries required to run the project.

---

🚀 Run Locally

Clone the Repository

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git
cd movie-recommend-system

Install Dependencies

pip install -r requirements.txt

Start the Application

streamlit run app.py

---

🔑 TMDB API

The application uses the TMDB API to fetch movie posters.

The API key is kept private using Streamlit Secrets.

Manage App
    ↓
Settings
    ↓
Secrets

Add:

TMDB_API_KEY = "YOUR_API_KEY"

---

🎯 Future Improvements

- 🔎 Movie Search
- ⭐ Movie Ratings
- 🎭 Genre Filtering
- 📅 Release Year Filtering
- 📖 Detailed Movie Information
- 👤 Personalized Recommendations
- 🎨 Improved UI
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