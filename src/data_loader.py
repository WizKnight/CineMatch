import requests
import csv
import pandas as pd
import time

api_key = '0efecc2129382b13b10723d96b774990'
base_url = 'https://api.themoviedb.org/3'

def fetch_popular_movies(page):
    url = f'{base_url}/movie/popular?api_key={api_key}&page={page}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request fails
    return response.json()['results']

def fetch_movie_details(movie_id):
    url = f'{base_url}/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Collect movie IDs
movie_ids = []
for page in range(1, 51):  # 50 pages for 1000 movies
    movie_ids.extend([movie['id'] for movie in fetch_popular_movies(page)])

# Fetch movie details
movie_data = []
for movie_id in movie_ids:
    details = fetch_movie_details(movie_id)
    
    if 'credits' in details:
        cast = [cast['name'] for cast in details['credits']['cast'][:5]]
    else:
        cast = []
    
    movie_data.append({
        'Title': details['title'],
        'Overview': details['overview'],
        'Genres': [genre['name'] for genre in details['genres']],
        'Cast': cast#[cast['name'] for cast in details['credits']['cast'][:5]],  # Top 5 cast members
        #'Release Date': details['release_date'],
        #'Runtime': details['runtime'],
        #'Rating': details['vote_average']
    })
    
    time.sleep(0.5)

with open('notebook/data/raw/tmdb_movies_data.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['title', 'overview', 'release_date', 'genres', 'cast', 'runtime', 'rating']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movie_data:
        writer.writerow(movie)

print("Movie data saved to 'tmdb_movies_data.csv'")