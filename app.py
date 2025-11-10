import streamlit as st
import pickle
import pandas as pd

# ---- Page Configuration ----
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎥",
    layout="centered",
)

# ---- Custom CSS Styling ----
st.markdown("""
    <style> 
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #141e30, #243b55);
        }

        /* Title Styling */
        .title {
            text-align: center;
            color: #FFD700;
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* Make Selectbox label white */
        div[data-testid="stSelectbox"] label {
            color: white !important;
            font-weight: 600 !important;
            font-size: 18px !important;
        }

        /* Make dropdown options dark (for visibility) */
        div[data-baseweb="select"] span {
            color: black !important;
        }

        /* Style for recommended movie names */
        .movie-title {
            font-size:15px !important;
            font-weight: 500 !important;
            color: white !important;
            margin: 8px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Load Data ----
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---- Recommend Function ----
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies           

# ---- UI ----
st.markdown("<div class='title'>🎬 Flick Finder – find your next favorite flick effortlessly.</div>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "🎥 Select a movie you liked:",
    movies['title'].values,
    index=0,
    key="movie_selector"
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.markdown("<br><h3 style='color:#FFD700;'>Recommended Movies 🎯</h3>", unsafe_allow_html=True)
    for i in recommendations:
        st.markdown(f"<div class='movie-title'> {i}</div>", unsafe_allow_html=True)
