import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=48882e2856f670764365c82955d6f8be&language=en-US".format(movie_id))

    data=response.json()

    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]


    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from tmdb API
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from tmdb API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

import streamlit as st

selected_movie_name = st.selectbox(
"Select or Enter Movie",
movies['title'].values)

st.write("You selected:",selected_movie_name )
import streamlit as st


if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)

    import streamlit as st
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0][:20])
        st.image(posters[0])
    with col2:
        st.text(names[0][:20])
        st.image(posters[1])
    with col3:
        st.text(names[0][:20])
        st.image(posters[2])
    with col4:
        st.text(names[0][:20])
        st.image(posters[3])
    with col5:
        st.text(names[0][:20])
        st.image(posters[4])

