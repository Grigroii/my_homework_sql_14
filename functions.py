import json
import sqlite3


def get_value_from_db(sql):
    with sqlite3.connect('netflix.db', check_same_thread=False) as con:
        con.row_factory = sqlite3.Row
        result = con.execute(sql).fetchall()
        return result


def get_by_title(title):
    sql = f"""
                    SELECT title,country,release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC
                    LIMIT 1
                    """

    my_list = []

    for item in get_value_from_db(sql=sql):
        if title in item:
            my_list.append(dict(item))
    return my_list



def add_by_querry(first_year, second_year):
    sql = f"""
        SELECT title, release_year 
        FROM netflix
        WHERE release_year BETWEEN '{first_year}' AND '{second_year}'
        ORDER BY release_year
        LIMIT 100
        """

    my_list = []
    for item in get_value_from_db(sql=sql):
        my_list.append(dict(item))
    return my_list


def get_rating(rating_category):
    RATING_CATEGORIES = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17']
    }

    sql = """
          SELECT title, rating, description 
          FROM netflix
          WHERE rating in ('G', 'PG', 'PG-13', 'R', 'NC-17')
          LIMIT 100
          """

    rating_list = []
    for item in get_value_from_db(sql=sql):
        _dict = dict(item)
        rating = _dict['rating']
        if rating in RATING_CATEGORIES.get(rating_category, []):
            rating_list.append(_dict)
    return rating_list


def get_genre(genre):
    sql = f"""
          SELECT title,description FROM netflix
          WHERE listed_in LIKE '%{genre}%'
          ORDER BY release_year DESC
          LIMIT 10
          """

    my_list = []
    for item in get_value_from_db(sql=sql):
        my_list.append(dict(item))
    return my_list


def all_actors(name1, name2):
    sql = f"""
          SELECT "cast" FROM netflix
          WHERE "cast" != '' AND "cast" LIKE '%{name1}%' AND "cast" LIKE '%{name2}%'
          """

    result = []

    names_dict = {}
    for item in get_value_from_db(sql=sql):
        names = set(dict(item).get('cast').split(',')) - {name1, name2}

        for name in names:
            names_dict[str(name).strip()] = names_dict.get(str(name).strip(), 0) + 1

    for key, value in names_dict.items():
        if value >= 2:
            result.append(key)
    return result


def get_picture(typ, year, genre):
    sql = f'''
          SELECT title, description, listed_in
          FROM netflix
          WHERE type = '{typ}'
          AND release_year = '{year}'
          AND listed_in = '{genre}'
          '''
    result = []

    for item in get_value_from_db(sql=sql):
        result.append(dict(item))

    return json.dumps(result, ensure_ascii=False, indent=4)

# print(get_picture('Movie','2021','Documentaries'))
