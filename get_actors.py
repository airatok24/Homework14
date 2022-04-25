import sqlite3


def db_connection(query):
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

def get_actors(name1='Rose McIver', name2='Ben Lamb'):
    query = f"""
    SELECT 
    "cast"
    FROM netflix
    WHERE "cast" LIKE '%{name1}%'
    AND "cast" LIKE '%{name2}%'
    """
    response = db_connection(query)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))
    result = []
    for actor in actors:
        if actor not in [name1, name2]:
            if actors.count(actor) > 2:
                result.append(actor)
    result = set(result)
    print(result)


get_actors()