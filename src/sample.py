import requests
import csv
import pandas as pd
import time
import os

api_key = os.environ.get('API_KEY')
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
for page in range(1, 6):  # 250 pages for 5000 movies
    movie_ids.extend([movie['id'] for movie in fetch_popular_movies(page)])

# Fetch movie details
movie_data = []
for movie_id in movie_ids:
    details = fetch_movie_details(movie_id)
    
    if 'credits' in details and 'cast' in details['credits']:  # Check for both 'credits' and 'cast'
        cast = [person['name'] for person in details['credits']['cast'][:5]]
    else:
        cast = []

    # Create a new dictionary with the correct field names (lowercase)
    movie_for_csv = {
        'title': details['title'],
        'overview': details['overview'],
        'genres': [genre['name'] for genre in details['genres']],
        'cast': ", ".join(cast),  # Convert cast list to a comma-separated string
        'release_date': details['release_date'],
        'runtime': details['runtime'],
        'rating': details['vote_average']
    }
    
    movie_data.append(movie_for_csv)  # Append the corrected dictionary
    
    time.sleep(0.5)

with open('notebook/data/raw/movies_data1.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['title', 'overview', 'release_date', 'genres', 'cast', 'runtime', 'rating']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movie_data:
        writer.writerow(movie)

print("Movie data saved to 'movies_data1.csv'")