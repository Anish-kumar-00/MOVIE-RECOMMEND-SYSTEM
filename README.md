

# 🎬 Movie Recommendation System

> 🍿 A Content-Based Movie Recommendation System built with Python, Machine Learning and Streamlit.

## 🚀 Live Demo

👉 [**Open Movie Recommendation System**](https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)

---

## ✨ Features

- 🎬 Select your favourite movie
- 🤖 Content-Based Recommendation
- 🔍 Find similar movies
- ⭐ Get 5 movie recommendations
- 🖼️ Movie posters using TMDB API
- ⚡ Fast recommendations
- 🌐 Streamlit Web App

---

## 🧠 How It Works

```text
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

Genres

Keywords

Cast

Director

Overview


are combined into a tags feature.

CountVectorizer converts the text into numerical vectors.

Then Cosine Similarity is used to find similar movies.


---

🛠️ Tech Stack

Technology	Used For

🐍 Python	Programming
🐼 Pandas	Data Processing
🔢 NumPy	Numerical Operations
🤖 Scikit-learn	Machine Learning
📝 NLTK	Text Processing
🎨 Streamlit	Web App
🎬 TMDB API	Movie Posters



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

app.py

Main Streamlit application.

movies.pkl

Processed movie dataset created from the original movie data.

similarity.pkl.gz

Precomputed similarity/recommendation indices.

requirements.txt

Contains the Python libraries required to run the project.


---

🚀 Run Locally

Clone the repository

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git
cd movie-recommend-system

Install dependencies

pip install -r requirements.txt

Start the application

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

🔎 Movie search

⭐ Movie ratings

🎭 Genre filtering

📅 Release year filtering

📖 Detailed movie information

👤 Personalized recommendations

🎨 Improved UI



---

👨‍💻 Author

Anish Kumar

🔗 GitHub


---

⭐ Support

If you like this project, please consider giving the repository a ⭐.

🎬 Happy Movie Discovering! 🍿

