import tmdbsimple as tmdb
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
api_key = os.environ.get("API_KEY")

tmdb.API_KEY = api_key

# Function to extract popular movies
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
    
# Get Poplular movies
def fetch_movies_from_page(page):
    popular_movies_url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&page={page}"
    response = requests.get(popular_movies_url)
    return response.json().get('results', [])

# Initialize lists to store movie data
movie_data = []

# Fetch and process data for 5000 movies
total_movies = 0
page = 1

while total_movies < 5000:
    movies_on_page = fetch_movies_from_page(page)

    for movie in movies_on_page:
        movie_id = movie['id']
        details = get_movie_details(movie_id)
        
        if details:
            cast = details['credits']['cast'][:5]
            actors_actresses = [person['name'] for person in cast]

            movie_info = {
                'id': movie_id,
                'title': movie['title'],
                'overview': movie['overview'],
                'genres': [genre['name'] for genre in movie.get('genres', [])],  # Handle missing genres
                'actors_actresses': actors_actresses
            }
            movie_data.append(movie_info)
            total_movies += 1

            if total_movies >= 5000:
                break

    page += 1
    time.sleep(0.5)
        
## Saving the data
df = pd.DataFrame(movie_data)
df.to_csv("data/raw/tmdb_movie_data.csv", index=False)