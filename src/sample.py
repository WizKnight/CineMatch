import requests
import csv

# TMDb Configuration
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZjM2NjU1YjRkYzllNmEyOWEzODRiODlmMWJmNDM2MCIsIm5iZiI6MTcyMjEyMTA2My42OTQyOTQsInN1YiI6IjY0MzFlYWRhNmRlYTNhMDBmMzk3YTI3YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.UDpcZa4-f_Omz6OLh_JsIaUx7AcOkgLoD5C0q5YVuZM" 
# Base URL and headers
base_url = "https://api.themoviedb.org/3/discover/movie"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Function to fetch genre details
def get_genres():
    genres_url = "https://api.themoviedb.org/3/genre/movie/list"
    response = requests.get(genres_url, headers=headers)
    genres_data = response.json()
    return {genre['id']: genre['name'] for genre in genres_data['genres']}

# Function to get movie cast
def get_cast(movie_id):
    cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    response = requests.get(cast_url, headers=headers)
    cast_data = response.json()
    return ", ".join([cast['name'] for cast in cast_data['cast'][:5]])  # Get top 5 cast members

# Get genre details
genres = get_genres()

# Data to collect
all_movies = []
for page in range(1, 101):
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": page,
        "sort_by": "popularity.desc"
    }

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    for movie in data['results']:
        movie_data = {
            'title': movie['title'],
            'overview': movie['overview'],
            'release_date': movie['release_date'],
            'genres': ", ".join([genres[genre_id] for genre_id in movie['genre_ids']]),
            'cast': get_cast(movie['id']), 
            'runtime': movie['runtime'],
            'rating': movie['vote_average']
        }
        all_movies.append(movie_data)

# Write data to CSV
with open('notebook/data/raw/tmdb_movies_data.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['title', 'overview', 'release_date', 'genres', 'cast', 'runtime', 'rating']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for movie in all_movies:
        writer.writerow(movie)

print("Movie data saved to 'tmdb_movies_data.csv'")
