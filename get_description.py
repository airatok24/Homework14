import sqlite3


def db_connection(query):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result


def get_description(type_film='Movie', release_year=2016, genre='Dramas'):
    query = f"""
        SELECT 
        title,
        description,
        "type"
        FROM netflix
        WHERE "type"='{type_film}'
        AND release_year='{release_year}'
        AND listed_in LIKE '%{genre}%'
        """
    response = db_connection(query)
    response_json = []
    for film in response:
        response_json.append({'title': film[0], 'description': film[1], 'type': film[2]})
    print(response_json)


get_description()
