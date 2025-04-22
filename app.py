import streamlit as st
import pandas as pd
import requests
import pickle

# S3 URLs
movie_dict_url = "https://my-movie-recommendation-bucket-sahithi.s3.ap-south-1.amazonaws.com/movie_dict.pkl"
movies_url = "https://my-movie-recommendation-bucket-sahithi.s3.ap-south-1.amazonaws.com/movies.pkl"
similarity_url = "https://my-movie-recommendation-bucket-sahithi.s3.ap-south-1.amazonaws.com/similarity.pkl"

def load_pickle_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.loads(response.content)
    except Exception as e:
        st.error(f"Failed to load from {url}")
        st.text(str(e))
        return None

# Load pickles from S3
movie_dict = load_pickle_from_url(movie_dict_url)
movies = load_pickle_from_url(movies_url)
similarity = load_pickle_from_url(similarity_url)

# If any are None, stop
if movie_dict is None or movies is None or similarity is None:
    st.stop()

movies = pd.DataFrame(movie_dict)

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=48882e2856f670764365c82955d6f8be&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# App UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox("Select or Enter Movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i][:20])
            st.image(posters[i])
