import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=d8b9b4c0a814755e5b7d951d3f07fbce&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

movies_dict = pickle.load(open('C:/Users/Asus/OneDrive/Desktop/MRS/movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('C:/Users/Asus/OneDrive/Desktop/MRS/similarity.pkl','rb'))


st.title('Movie Recommendation System')
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)



def Recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

  recommended_movies = []
  recommended_movies_posters = []
  for i in movies_list:
    movie_id = movies.iloc[i[0]].movie_id
    #fetch poster from API
    recommended_movies.append(movies.iloc[i[0]].title)
    recommended_movies_posters.append(fetch_poster(movie_id))
  return recommended_movies,recommended_movies_posters



if st.button('Recommend'):
    names,posters = Recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])