  
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sqlite3


os.environ['SPOTIPY_CLIENT_ID']  =  'a253f05c08a14547bf7a270fc76c9f99' 
os.environ['SPOTIPY_CLIENT_SECRET'] = '612f41bed1804679ac80b23870ef3264'


  
spotify = spotipy.Spotify(
client_credentials_manager=SpotifyClientCredentials( ))
conn = sqlite3.connect("anime.db")
  # Creates a cursor #
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS composers (
  id    INTEGER PRIMARY KEY,
  spot_id TEXT UNIQUE,
  name  TEXT,
  popularity  INTEGER
  );
""") 

# Create the tracks table
# Update table definition to use composer id instead of composer (name)
# Composer_id will be a key that links to id in the composer table
sql = """
CREATE TABLE IF NOT EXISTS ghibli_tracks (
    album_name   TEXT,
    id           TEXT UNIQUE, 
    popularity   INTEGER, 
    release_date TEXT,
    composer_id  INTEGER,
    genre        TEXT,
    FOREIGN KEY (composer_id) REFERENCES composers (id)

)
"""
cur.execute(sql)

api_limit = 50
api_offset = 0

# Get starting record count
res = cur.execute("SELECT COUNT(*) FROM ghibli_tracks")
starting_count = res.fetchone()[0]
print("Starting record count:",starting_count)
records_added = 0



# Within a loop...
while records_added < 25:
  
  # Execute the API search
  results = spotify.search('Ghibli',
                            offset=api_offset,
                            limit=api_limit,
                            type="track")

  # Process the results -- saving to the DB
  for track in results['tracks']['items']:

    # Get the specific info from the API results
    album_name = track['album']['name']
    id = track['album']['id']
    popularity = track['popularity']  
    release_date = track['album']['release_date']  
    composer_id = track['artists'][0]['id']  
    

    # Find the artist's id
    artist_id = track['artists'][0]['id']
    # Perform a second spotify search for artist using that id.
    artist_results = spotify.artist(artist_id)
    # Pull genre information from the response
    # Only keep first genre from list
    genre = artist_results.get('genres',[])
    if len(genre) > 0:
        genre = genre[0]
    else:
        genre = ""


    # BEFORE DOING tracks table insert, search for composer by artist id and get relevant information.
    results2 = spotify.artist(composer_id)  
    # INSERT composer information into composer table
    print(results2)

    # Check whether composer is already in the composers table.
    # If so, use that id to link to the upcoming track record.
    results3 = cur.execute("SELECT id FROM composers WHERE spot_id = ?",[results2["id"]])
    rows = results3.fetchall()
    print(rows)

    if len(rows) == 0:
      # Nothing was found. Do the insert.
      # Otherwise, insert the new composer
      cur.execute("INSERT OR IGNORE INTO composers (spot_id,name,popularity) VALUES (?,?,?)", (results2['id'], results2['name'], results2['popularity']))
      conn.commit()
      cur.execute("select last_insert_rowid()")
      composer_id = cur.fetchone()[0]

    else:
      # get the id
      #print(rows)
      composer_id = rows[0][0]
    

    # Write (INSERT) to the DB table
    sql = "INSERT OR IGNORE INTO ghibli_tracks (album_name, id, popularity, release_date, composer_id, genre  ) VALUES (?,?,?,?,?,?)"
    #print(sql, album_name, id, popularity, release_date, composer_id, genre)
    cur.execute(sql, (album_name, id, popularity, release_date, composer_id, genre))
    conn.commit()

    # Check whether 100 records are in the table.
    res = cur.execute("SELECT COUNT(*) FROM ghibli_tracks")
    record_count = cur.fetchone()[0]
    if record_count - starting_count == 25:
      print(f"25 records created.")
      records_added = 25
      break

  # Test whether we've run out of relevant records at the API
  if len(results['tracks']['items']) < api_limit:
    print("OUT OF RELEVANT RECORDS AT API. STOPPING API QUERIES.")
    break
  
  # # If not, increase the offset and loop/search again...
  api_offset += api_limit


cur.close()
conn.close()




