from flask import Flask, request, jsonify
from multiprocessing import Process
import requests

# API ключ для OMDb API
OMDB_API_KEY = 'your_omdb_api_key'
OMDB_API_URL = 'http://www.omdbapi.com/'

# Функция для микросервиса информации о фильмах
def create_info_app():
    app = Flask(__name__)

    @app.route('/movie/<title>', methods=['GET'])
    def get_movie_info(title):
        response = requests.get(OMDB_API_URL, params={'t': title, 'apikey': OMDB_API_KEY})
        return jsonify(response.json())

    return app

# Функция для микросервиса рекомендаций
def create_recommend_app():
    app = Flask(__name__)

    movies = [
        {"title": "Inception", "genre": "Sci-Fi", "rating": 8.8},
        {"title": "Interstellar", "genre": "Sci-Fi", "rating": 8.6},
        {"title": "The Godfather", "genre": "Crime", "rating": 9.2}
    ]

    @app.route('/recommend', methods=['GET'])
    def recommend():
        genre = request.args.get('genre')
        rating = float(request.args.get('rating', 0))
        recommendations = [m for m in movies if m['genre'] == genre and m['rating'] >= rating]
        return jsonify(recommendations)

    return app

# Функция для микросервиса отзывов
def create_reviews_app():
    app = Flask(__name__)
    reviews = {
        "Inception": ["Amazing movie!", "Mind-blowing.", "Fantastic visuals!"],
        "Interstellar": ["Great storyline.", "Beautifully shot.", "Deep and emotional."],
    }

    @app.route('/reviews/<title>', methods=['GET'])
    def get_reviews(title):
        return jsonify(reviews.get(title, []))

    @app.route('/reviews/<title>', methods=['POST'])
    def add_review(title):
        review = request.json.get('review')
        if title in reviews:
            reviews[title].append(review)
        else:
            reviews[title] = [review]
        return jsonify({"message": "Review added!"})

    return app

# Запуск микросервиса в отдельном процессе
def run_service(app_factory, port):
    app = app_factory()
    app.run(port=port)

if __name__ == '__main__':
    processes = [
        Process(target=run_service, args=(create_info_app, 5001)),
        Process(target=run_service, args=(create_recommend_app, 5002)),
        Process(target=run_service, args=(create_reviews_app, 5003))
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

