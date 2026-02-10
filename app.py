import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": API_KEY,
            "language": "en-US"
        }
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5
        )
        if response.status_code != 200:
            return None
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"{BASE_IMAGE_URL}{poster_path}"
        return None
    except requests.exceptions.RequestException:
        return None


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key = lambda x: x[1])

    recommended_movies = []
    recommended_posters = []
    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

#load Data
similarity = pickle.load(open('similarity.pkl','rb'))
movies= pickle.load(open('movies.pkl', 'rb'))
movie_titles = movies['title'].values

#streamlit UI
st.title('Movie Recommender system')
selected_movie_name= st.selectbox(
    "Select a movie",
    movie_titles
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.write("No poster")






