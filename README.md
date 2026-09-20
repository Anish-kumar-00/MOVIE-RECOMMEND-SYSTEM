# MOVIE-RECOMMEND-SYSTEM

# 🎬 Movie Recommendation System

<p align="center">
  <img src="https://commons.wikimedia.org/wiki/Special:Redirect/file/Movie_theater_seats_%28Unsplash%29.jpg" width="100%" alt="Movie Recommendation System">
</p>

<h2 align="center">🍿 Discover Movies You'll Love</h2>

<p align="center">
A Content-Based Movie Recommendation System built with Python, Machine Learning and Streamlit.
</p>

<p align="center">
<a href="https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/">
<img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge">
</a>
<img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit">
<img src="https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikit-learn">
</p>

---

## 🎥 Live Demo

👉 **[Open Movie Recommendation System](https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)**

Select your favourite movie and get **5 similar movie recommendations**.

---

## ✨ Features

- 🎬 Select a movie from the database
- 🤖 Content-Based Movie Recommendation
- 🔍 Find similar movies using movie features
- ⭐ Get 5 similar movie recommendations
- 🖼️ Fetch movie posters using TMDB API
- ⚡ Fast recommendations using precomputed similarity data
- 🌐 Interactive Streamlit web application

---

## 🧠 How It Works

```text
                 Movie Dataset
                       │
                       ▼
              Data Preprocessing
                       │
                       ▼
       ┌─────────────────────────────┐
       │ Genres                      │
       │ Keywords                    │
       │ Cast                        │
       │ Director                    │
       │ Movie Overview              │
       └─────────────────────────────┘
                       │
                       ▼
                Create Tags
                       │
                       ▼
              Text Preprocessing
                       │
                       ▼
               CountVectorizer
                       │
                       ▼
             Cosine Similarity
                       │
                       ▼
          Find Similar Movies
                       │
                       ▼
            Top 5 Recommendations


---

🔬 Recommendation Method

This project uses Content-Based Filtering.

Movie information such as:

Genres

Keywords

Cast

Director

Overview


is combined into a single tags feature.

The text data is converted into numerical vectors using CountVectorizer.

Then Cosine Similarity is used to find movies with similar content.


---

🛠️ Technologies Used

Technology	Purpose

🐍 Python	Programming
🐼 Pandas	Data Processing
🔢 NumPy	Numerical Operations
🤖 Scikit-learn	Machine Learning
📝 NLTK	Text Processing & Stemming
🎨 Streamlit	Web Application
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

📄 File Description

File	Description

app.py	Streamlit application
movies.pkl	Processed movie dataset
similarity.pkl.gz	Precomputed movie similarity indices
requirements.txt	Required Python packages
README.md	Project documentation



---

📊 Data Processing

Movies Dataset + Credits Dataset
              │
              ▼
            Merge
              │
              ▼
Genres + Keywords + Cast + Director + Overview
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
       Cosine Similarity
              │
              ▼
      Similar Movie Indices

The processed movie information is stored in:

movies.pkl

The precomputed recommendation indices are stored in:

similarity.pkl.gz


---

🚀 Run Locally

1. Clone the repository

git clone https://github.com/Anish-kumar-00/movie-recommend-system.git
cd movie-recommend-system

2. Install dependencies

pip install -r requirements.txt

3. Run the application

streamlit run app.py


---

🔑 TMDB API

The application uses the TMDB API to fetch movie posters.

The API key is not stored in the source code.

For Streamlit Cloud, add it through:

Manage App
     ↓
Settings
     ↓
Secrets

Add:

TMDB_API_KEY = "YOUR_API_KEY"


---

🎯 Future Improvements

🔎 Movie search functionality

⭐ Movie ratings

🎭 Genre-based filtering

📅 Release year filtering

📖 Detailed movie information

🎨 Improved user interface

👤 Personalized recommendations



---

👨‍💻 Author

Anish Kumar

🔗 GitHub:
https://github.com/Anish-kumar-00


---

<p align="center">⭐ If you like this project, consider giving it a star! ⭐

<br>🎬 Happy Movie Discovering! 🍿

</p>
```Bas itna hi hai — ek hi baar me पूरा README.md replace kar dena.