from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection function
def create_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="spotify_final_database",
        user="postgres",
        password="ApoBill"
    )

# Function to ensure the "default_user" exists
def ensure_default_user():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Check if the default_user exists
        cursor.execute("SELECT 1 FROM APP_USER WHERE username = 'default_user';")
        user_exists = cursor.fetchone()

        # If not, insert the default user
        if not user_exists:
            cursor.execute("""
                INSERT INTO APP_USER (username, email, Birthday) 
                VALUES ('default_user', 'default@example.com', '2000-01-01');
            """)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

# Function to ensure an artist exists in the APP_USER table
def ensure_artist_exists(artist_name):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Check if artist exists
        cursor.execute("SELECT COUNT(*) FROM APP_USER WHERE username = %s;", (artist_name,))
        exists = cursor.fetchone()[0]

        # Insert artist if not exists
        if not exists:
            cursor.execute("INSERT INTO APP_USER (username, email, Birthday) VALUES (%s, %s, %s);",
                           (artist_name, f"{artist_name}@example.com", "2000-01-01"))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

# Get all playlists with their songs
def get_playlists_with_songs():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT 
                p.playlist_id, p.name, 
                s.song_id, s.song_name, s.artist
            FROM Playlist p
            LEFT JOIN songlist sl ON p.playlist_id = sl.playlist_id
            LEFT JOIN Song s ON sl.song_id = s.song_id
            ORDER BY p.playlist_id;
        """)

        rows = cursor.fetchall()

        playlists = {}
        for row in rows:
            playlist_id, playlist_name, song_id, song_name, artist = row
            if playlist_id not in playlists:
                playlists[playlist_id] = {
                    'id': playlist_id,
                    'name': playlist_name,
                    'songs': []
                }
            if song_id:  # Only add songs if song_id is not None
                playlists[playlist_id]['songs'].append({
                    'id': song_id,
                    'name': song_name or 'No Name',  # Handle missing song_name
                    'artist': artist or 'Unknown Artist'  # Handle missing artist
                })

        return list(playlists.values())

    finally:
        cursor.close()
        connection.close()

# Add a new playlist
def add_playlist_to_db(playlist_name):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Ensure default_user exists
        ensure_default_user()
        default_user_name = "default_user"

        cursor.execute("""
            INSERT INTO Playlist (user_name, name) 
            VALUES (%s, %s) 
            RETURNING playlist_id, name;
        """, (default_user_name, playlist_name))

        new_playlist = cursor.fetchone()
        connection.commit()
        return new_playlist
    finally:
        cursor.close()
        connection.close()

# API to add a playlist
@app.route('/api/playlists', methods=['POST'])
def add_playlist():
    data = request.get_json()

    playlist_name = data.get('name')
    if not playlist_name:
        return jsonify({'error': 'Playlist name is required'}), 400

    try:
        new_playlist = add_playlist_to_db(playlist_name)
        return jsonify({'message': 'Playlist created successfully!', 'playlist': {
            'id': new_playlist[0],
            'name': new_playlist[1],
        }}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to create playlist: {str(e)}'}), 500

# API to delete a playlist
@app.route('/api/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Get all song IDs in the playlist
        cursor.execute("SELECT song_id FROM songlist WHERE playlist_id = %s;", (playlist_id,))
        song_ids = [row[0] for row in cursor.fetchall()]

        # Delete associated songs from the songlist
        cursor.execute("DELETE FROM songlist WHERE playlist_id = %s;", (playlist_id,))

        # Delete the songs themselves if they are not in any other playlist
        for song_id in song_ids:
            cursor.execute("SELECT COUNT(*) FROM songlist WHERE song_id = %s;", (song_id,))
            count = cursor.fetchone()[0]
            if count == 0:  # Only delete the song if it is not in any other playlist
                cursor.execute("DELETE FROM Song WHERE song_id = %s;", (song_id,))

        # Finally, delete the playlist
        cursor.execute("DELETE FROM Playlist WHERE playlist_id = %s;", (playlist_id,))
        connection.commit()

        return jsonify({'message': 'Playlist and its songs deleted successfully!'}), 200

    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to delete playlist: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

# Add a song to the database
def add_song_to_db(song_name, artist, duration, release_date, playlist_id=None, user_id="default_user"):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        # Ensure the artist exists in the APP_USER table
        ensure_artist_exists(artist)

        # Insert the new song into the Song table
        cursor.execute("""
            INSERT INTO Song (song_name, artist, duration, ReleaseDate) 
            VALUES (%s, %s, %s, %s) 
            RETURNING song_id, song_name, artist, duration, ReleaseDate;
        """, (song_name, artist, duration, release_date))
        new_song = cursor.fetchone()
        song_id = new_song[0]  # Extract the newly inserted song_id

        # If a playlist_id is provided, insert the song into the songlist table
        if playlist_id:
            cursor.execute("""
                INSERT INTO songlist (song_id, playlist_id, user_id) 
                VALUES (%s, %s, %s);
            """, (song_id, playlist_id, user_id))

        # Commit the transaction
        connection.commit()
        return new_song
    except Exception as e:
        # Rollback in case of an error
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

# API to add a song
@app.route('/api/songs', methods=['POST'])
def add_song():
    data = request.json

    song_name = data.get('song_name')
    artist = data.get('artist')
    duration = data.get('duration')
    release_date = data.get('release_date')
    playlist_id = data.get('playlist_id')

    if not all([song_name, artist, duration, release_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_song = add_song_to_db(song_name, artist, duration, release_date, playlist_id)
        return jsonify({'message': 'Song added successfully!', 'song': {
            'id': new_song[0],
            'name': new_song[1],
            'artist': new_song[2],
            'duration': str(new_song[3]),
            'release_date': str(new_song[4])
        }}), 201
    except Exception as e:
        return jsonify({'error': f'Failed to add song: {str(e)}'}), 500

# API to delete a song
@app.route('/api/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        # Remove the song from all playlists
        cursor.execute("DELETE FROM songlist WHERE song_id = %s;", (song_id,))
        # Delete the song itself
        cursor.execute("DELETE FROM Song WHERE song_id = %s;", (song_id,))
        connection.commit()
        return jsonify({'message': 'Song deleted successfully!'}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to delete song: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

# API to get all playlists
@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    try:
        playlists = get_playlists_with_songs()
        return jsonify({'playlists': playlists})
    except Exception as e:
        return jsonify({'error': f'Failed to fetch playlists: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
