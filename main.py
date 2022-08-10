from flask import Flask, jsonify
from functions import get_by_title, add_by_querry, get_rating, get_genre, all_actors, get_picture

app = Flask(__name__)


@app.route('/movie/<title>/', methods=['GET'])
def search_by_title(title):
    result = get_by_title(title)
    return jsonify(result)


@app.route('/movie/<first_year>/<second_year>')
def get_movies_by_years(first_year, second_year):
    result = add_by_querry(first_year, second_year)
    return jsonify(result)


@app.route('/rating/<rating_category>')
def get_rating_by_category(rating_category):
    result = get_rating(rating_category)
    return jsonify(result)


@app.route('/genre/<genre>')
def get_movies_by_genres(genre):
    result = get_genre(genre)
    return jsonify(result)


@app.route('/actors/<name1>/<name2>')
def get_movies_by_actors(name1, name2):
    result = all_actors(name1, name2)
    return jsonify(result)

@app.route('/films/<type>/<year>/<genre>')
def get_movies_by_different_functions(type, year, genre):
    result = get_picture(type, year, genre)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
