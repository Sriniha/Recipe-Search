from flask import Flask, request, jsonify
from opensearchpy import OpenSearch
import json
import requests
import csv
import pandas as pd

app = Flask(__name__)

# Configure OpenSearch client
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,
    http_auth=('admin', 'Bin2@2305'),
    use_ssl=True,
    verify_certs=False,
    timeout=30,
    max_retries=3,
    retry_on_timeout=True
)

PIXABAY_API_KEY = '45976774-116a10a0a367343d539e54337'
PIXABAY_URL = 'https://pixabay.com/api/'

def get_image_url(query):
    try:
        params = {
            'key': PIXABAY_API_KEY,
            'q': query,
            'image_type': 'photo',
            'per_page': 1
        }
        response = requests.get(PIXABAY_URL, params=params)
        data = response.json()
        if data['hits']:
            return data['hits'][0]['webformatURL']
    except Exception as e:
        print(f"Error fetching image: {e}")
    return "https://www.google.com/url?sa=i&url=https%3A%2F%2Fparniangostar.com%2Fen%2Fproduct%2Fgelory-diode-laser-device&psig=AOvVaw0xMLOu3HCzpT7GY04eSl0d&ust=1726379973222000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNDVptzgwYgDFQAAAAAdAAAAABAd"  # Fallback image

@app.route('/')
def home():
    return "Welcome to the Recipe API!"


@app.route('/api/search', methods=['GET'])
def search_recipes():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    calories = request.args.get('calories')
    dietary = request.args.getlist('dietary')

    must_conditions = [
        {"multi_match": {"query": query, "fields": ["title"]}}
    ]
    
    if calories:
        must_conditions.append({"range": {"calories": {"lte": int(calories)}}})
    for diet in dietary:
        must_conditions.append({"term": {diet: True}})
    
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title"]  # Verify these field names
            }
        },
        "from": (page - 1) * size,
        "size": size
    }
    
    try:
        results = client.search(index="epi_r_index", body=search_body)
        
        recipes = []
        for hit in results['hits']['hits']:
            recipe = hit['_source']
            recipes.append({
                'id': hit['_id'],
                'title': recipe.get('title'),
                'rating': recipe.get('rating'),
                'calories': recipe.get('calories'),
                'protein': recipe.get('protein'),
                'fat': recipe.get('fat'),
                'sodium': recipe.get('sodium')
            })
        
        return jsonify({
            'recipes': recipes,
            'total': results['hits']['total']['value'],
            'page': page,
            'size': size
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filters', methods=['GET'])
def get_filters():
    try:
        
        calories_range = get_calories_range()
        # The 'dietary' field doesn't seem to exist in the original data
        # Instead, we'll use boolean fields for dietary restrictions
        dietary = [
            'vegetarian', 'vegan', 'pescatarian', 'dairy_free', 
            'wheat_gluten_free', 'low_fat', 'low_sodium', 'kosher'
        ]

        filters = {
            'calories_range': calories_range,
            'dietary': dietary
        }
        return jsonify(filters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_calories_range():
    query = {
        "size": 0,
        "aggs": {
            "calories_stats": {
                "stats": {
                    "field": "calories"
                }
            }
        }
    }
    
    results = client.search(index="epi_r_index", body=query)
    stats = results['aggregations']['calories_stats']
    
    return {
        "min": int(stats['min']),
        "max": int(stats['max'])
    }

@app.route('/api/top_rated', methods=['GET'])
def get_top_rated():
    try:
        search_body = {
            "sort": [{"rating": "desc"}],
            "size": 5
        }
        results = client.search(index="epi_r_index", body=search_body)
        
        top_rated = []
        for hit in results['hits']['hits']:
            recipe = hit['_source']
            top_rated.append({
                'id': hit['_id'],
                'title': recipe.get('title'),
                'rating': recipe.get('rating'),
                'image': get_image_url(recipe.get('title'))
            })
        
        return jsonify(top_rated)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    # Define your categories based on your dataset fields
    df = pd.read_csv('Backend/epi_r.csv')
    
    # Select columns that are not nutritional info or metadata
    category_columns = df.columns[6:]
    
    # Count non-zero values in each category column
    category_counts = (df[category_columns] != 0).sum()
    
    # Select categories that appear in at least 1% of recipes
    min_count = len(df) * 0.01
    relevant_categories = category_counts[category_counts >= min_count].index.tolist()
    
    # Sort categories alphabetically
    relevant_categories.sort()
    
    # Get images for each category
    categories_with_images = []
    for category in relevant_categories:
        image_url = get_image_url(category)
        categories_with_images.append({
            'name': category,
            'image': image_url
        })
    
    return jsonify(categories_with_images)

@app.route('/api/popular_recipes', methods=['GET'])
def get_popular_recipes():
    try:
        search_body = {
            "sort": [
                {"rating": "desc"},
                {"_score": "desc"}
            ],
            "size": 10
        }
        results = client.search(index="epi_r_index", body=search_body)
        
        popular_recipes = []
        for hit in results['hits']['hits']:
            recipe = hit['_source']
            popular_recipes.append({
                'id': hit['_id'],
                'title': recipe.get('title'),
                'rating': recipe.get('rating'),
                'calories': recipe.get('calories'),
                'image': get_image_url(recipe.get('title'))
            })
        
        return jsonify(popular_recipes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# def index_recipes():
#     client = OpenSearch(hosts=[{'host': 'localhost', 'port': 9201}])
#     index_name = 'recipes'

#     # Delete the index if it exists
#     if client.indices.exists(index=index_name):
#         client.indices.delete(index=index_name)

#     # Create the index with appropriate mappings
#     index_body = {
#         'mappings': {
#             'properties': {
#                 'title': {'type': 'text'},
#                 'rating': {'type': 'float'},
#                 'calories': {'type': 'float'},
#                 'protein': {'type': 'float'},
#                 'fat': {'type': 'float'},
#                 'sodium': {'type': 'float'},
#                 'tags': {'type': 'keyword'}
#             }
#         }
#     }
#     client.indices.create(index=index_name, body=index_body)

#     # Read and index the recipes from the CSV file
#     with open('epi_r.csv', 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             recipe = {
#                 'title': row['title'],
#                 'rating': float(row['rating']) if row['rating'] else None,
#                 'calories': float(row['calories']) if row['calories'] else None,
#                 'protein': float(row['protein']) if row['protein'] else None,
#                 'fat': float(row['fat']) if row['fat'] else None,
#                 'sodium': float(row['sodium']) if row['sodium'] else None,
#                 'tags': [tag for tag, value in row.items() if value == '1.0' and tag not in ['title', 'rating', 'calories', 'protein', 'fat', 'sodium']]
#             }
#             client.index(index=index_name, body=recipe)

#     print(f"Indexed {client.count(index=index_name)['count']} recipes")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    client = OpenSearch(hosts=[{'host': 'localhost', 'port': 9200}])
    index_name = 'epi_r_index'

    search_body = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title^2', 'tags']
            }
        }
    }

    results = client.search(index=index_name, body=search_body)
    hits = results['hits']['hits']
    recipes = [
        {
            'id': hit['_id'],
            'title': hit['_source']['title'],
            'rating': hit['_source']['rating'],
            'calories': hit['_source']['calories'],
            'tags': hit['_source']['tags']
        }
        for hit in hits
    ]

    return jsonify(recipes)

@app.route('/recipe/<id>', methods=['GET'])
def get_recipe(id):
    client = OpenSearch(hosts=[{'host': 'localhost', 'port': 9200}])
    index_name = 'epi_r_recipes'

    try:
        result = client.get(index=index_name, id=id)
        recipe = result['_source']
        return jsonify(recipe)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    # Index recipes when the app starts
    app.run(debug=True)
