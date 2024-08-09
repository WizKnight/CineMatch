import pandas as pd
import ast
import os
import json
from collections import defaultdict

# Load the dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "notebook", "data", "raw", "final_movie_data.csv")
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"File not found: {file_path}")


def extract_from_list_string(s):
    try:
        data_list = ast.literal_eval(s)
        cleaned_data = [item.strip("'") for item in data_list[:5]]
        return cleaned_data
    except (SyntaxError, ValueError):
        return []
    
# Drop rows with missing values
df = df.dropna(subset=['title', 'genres', 'cast'])

# Clean and extract genres
df['genres'] = df['genres'].apply(extract_from_list_string)

# Clean and extract cast (top 5 actors)
df['cast'] = df['cast'].apply(extract_from_list_string)


# Initialize inverted index
inverted_index = defaultdict(set)

# Create the inverted index
for index, row in df.iterrows():
    entities = {
        'PER': row['cast'],
        'GEN': row['genres'],
        'MOV': [row['title']]  # Movie title as a single-item list
    }

    for entity_type, entity_list in entities.items():
        for entity in entity_list:
            inverted_index[entity_type, entity].add(row['title'])
            

# Optionally, save the processed data and inverted index
df.to_csv('notebook/data/processed/tmdb_movies_processed.csv', index=False)
with open('notebook/data/processed/inverted_index.json', 'w') as f:
    json.dump(inverted_index, f)

# Search Function
def search_movies(query):
    query_tokens = query.lower().split()
    results = defaultdict(int)

    for token in query_tokens:
        for (entity_type, entity), movies in inverted_index.items():
            if token in entity:
                for movie in movies:
                    results[movie] += 1

    filtered_results = {movie: count for movie, count in results.items() if count == len(query_tokens)}
    sorted_results = dict(sorted(filtered_results.items(), key=lambda item: item[1], reverse=True))

    return sorted_results


search_results = search_movies("Ryan Reynolds Comedy")
print(search_results)
