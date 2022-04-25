from flask import Flask, jsonify
import sqlite3


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    def db_connection(query):
        connection = sqlite3.connect('netflix.db')
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result

    @app.route('/movie/<title>')
    def search_by_title(title):
        query = f""" 
                SELECT
                title,
                country,
                release_year,
                listed_in AS genre,
                description
                FROM netflix
                WHERE title='{title}'
                ORDER BY release_year DESC
                LIMIT 1
                """
        response = db_connection(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'genre': response[3],
            'description': response[4]
        }
        return jsonify(response_json)

    @app.route('/movie/<int:start>/to/<int:end>')
    def search_by_period(start, end):
        query = f""" 
                SELECT
                title,
                release_year
                FROM netflix
                WHERE release_year BETWEEN {start} and {end}
                LIMIT 100
                """
        response = db_connection(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1],
            })
        return jsonify(response_json)

    @app.route('/rating/<group>')
    def search_by_rating(group):
        levels = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17']
        }
        if group in levels:
            level = '\", \"'.join(levels[group])
            level = f'\"{level}\"'

        else:
            return jsonify([])
        query = f""" 
                    SELECT
                    title,
                    rating,
                    description
                    FROM netflix
                    WHERE rating IN ({level})
                    """
        print(query)
        response = db_connection(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1],
            })
        return jsonify(response_json)

    @app.route('/genre/<genre>')
    def search_by_genre(genre):
        query = f""" 
                    SELECT
                    title,
                    description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10
                """
        response = db_connection(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1]
            })
        return jsonify(response_json)




    # app.run(debug=True)


if __name__ == '__main__':
    main()
