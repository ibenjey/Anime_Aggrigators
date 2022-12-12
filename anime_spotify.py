def get_ghibli(conn):
    
  import os
  import spotipy
  from spotipy.oauth2 import SpotifyClientCredentials
  import json
  import sqlite3
  

  # Tutorial on how to store environmnetal variables
  # https://datagy.io/python-environment-variables/
  # MAC or UNIX, use export
  # For security, this should be done differently on a live program
  os.environ['SPOTIPY_CLIENT_ID']  =  'a253f05c08a14547bf7a270fc76c9f99' 
  os.environ['SPOTIPY_CLIENT_SECRET'] = '612f41bed1804679ac80b23870ef3264'


    
  spotify = spotipy.Spotify(
  client_credentials_manager=SpotifyClientCredentials( ))
    
    # Creates a cursor #
  cur = conn.cursor()
  cur.execute('DROP TABLE IF EXISTS ghibli_tracks')
 
  # Create the composer table first because tracks table will link to it.
  # id will be the primary key and is the spotify id for the artist/composer

  # CREATE composer table ....
  # Create a composers table
  cur.execute("""CREATE TABLE IF NOT EXISTS composers (
    art_id    TEXT PRIMARY KEY,
    name  TEXT,
    popularity  INTEGER
    );
  """) 
  
  # Create the tracks table
  # Update table definition to use composer id instead of composer (name)
  # Composer_id will be a key that links to id in the composer table
  sql = """
  CREATE TABLE ghibli_tracks (
      album_name   TEXT,
      id           TEXT, 
      popularity   INTEGER, 
      release_date TEXT,
      composer_id  TEXT,
      genre        TEXT,
      FOREIGN KEY (composer_id) REFERENCES composers (id)

  )
  """
  cur.execute(sql)

  api_limit = 25
  api_offset = 0
  
  # Within a loop...
  while True:
    
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
      cur.execute("INSERT OR IGNORE INTO composers (id, name, popularity) VALUES (?,?,?)", (composer_id, results2['name'], results2['popularity']))
      conn.commit()

      # Write (INSERT) to the DB table
      sql = "INSERT OR IGNORE INTO ghibli_tracks (album_name, id, popularity, release_date, composer_id, genre  ) VALUES (?,?,?,?,?,?)"
      #print(sql, album_name, id, popularity, release_date, composer_id, genre)
      cur.execute(sql, (album_name, id, popularity, release_date, composer_id, genre))
      conn.commit()
  
    # Check whether 100 records are in the table.
    res = cur.execute("SELECT COUNT(*) FROM ghibli_tracks")
    record_count = cur.fetchone()[0]
    if record_count > 100:
      print(f"{record_count} records created.")
      break
    else:
  
      # If not, increase the offset and loop/search again...
      api_offset += api_limit

  
  cur.close()
  conn.close()




# def make_ghibli_graph():
  
  
## TO DO ##

# limit the load to 25 data entries per run
# write a join statment
# assign primary keys to integer types in both tables
# have to fix the duplicate data in one of my tables since the IDs are strings 