Haan, samajh gaya. Problem ye hai ki GitHub README me raw HTML <p>, <img> etc. kabhi-kabhi text/tag ki tarah render ho raha hai, aur external image URLs bhi reliable nahi hain.

Tumhare liye pure GitHub Markdown use karte hain—<p>/<img> hata dete hain. Isse tags dikhne ka issue nahi hoga.

# 🎬 Movie Recommendation System

![Movie Recommendation](https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=80)

## 🍿 Discover Movies You'll Love

A **Content-Based Movie Recommendation System** built using Python, Machine Learning and Streamlit.

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge)](https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

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
Movie Dataset + Credits Dataset
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

Movies Dataset
      +
Credits Dataset
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

For Streamlit Cloud:

Manage App → Settings → Secrets

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

🔗 GitHub Profile


---

⭐ Support

If you like this project, consider giving the repository a ⭐.

🎬 Happy Movie Discovering! 🍿

**Is version me `<p>`, `<img>` jaise HTML tags nahi hain**, isliye woh README me text ki tarah dikhne ka problem nahi aana chahiye.Haan, samajh gaya. Problem ye hai ki GitHub README me raw HTML <p>, <img> etc. kabhi-kabhi text/tag ki tarah render ho raha hai, aur external image URLs bhi reliable nahi hain.

Tumhare liye pure GitHub Markdown use karte hain—<p>/<img> hata dete hain. Isse tags dikhne ka issue nahi hoga.

# 🎬 Movie Recommendation System

![Movie Recommendation](https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1600&q=80)

## 🍿 Discover Movies You'll Love

A **Content-Based Movie Recommendation System** built using Python, Machine Learning and Streamlit.

[![🚀 Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge)](https://movie-recommend-system-f4fbvjdrp7s2p6hhfspsfo.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

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
Movie Dataset + Credits Dataset
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

Movies Dataset
      +
Credits Dataset
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

For Streamlit Cloud:

Manage App → Settings → Secrets

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

🔗 GitHub Profile


---

⭐ Support

If you like this project, consider giving the repository a ⭐.

🎬 Happy Movie Discovering! 🍿

**Is version me `<p>`, `<img>` jaise HTML tags nahi hain**, isliye woh README me text ki tarah dikhne ka problem nahi aana chahiye.