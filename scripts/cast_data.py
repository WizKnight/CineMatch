import tmdbsimple as tmdb
import pandas as pd
import time
import os

api_key = os.environ.get('API_KEY')  
tmdb.API_KEY = api_key

# Initialize a list to store movie cast data
movie_cast_data = []

# Fetch the first 5000 popular movies
page = 1
total_movies = 0
while total_movies < 5000:
    movies = tmdb.Movies().popular(page=page)["results"]
    
    for movie in movies:
        movie_id = movie['id']
        cast = [person['name'] for person in tmdb.Movies(movie_id).credits()['cast'][:5]]

        movie_cast_info = {
            'id': movie_id,
            'cast': cast,
        }
        movie_cast_data.append(movie_cast_info)
        total_movies += 1

        if total_movies >= 5000:
            break

    page += 1
    time.sleep(0.5)

# Create DataFrame and save to CSV
df = pd.DataFrame(movie_cast_data)
df.to_csv("notebook/data/raw/movie_cast.csv", index=False)
