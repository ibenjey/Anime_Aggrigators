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
    
    # Artist name
    
    # Find the artist-id associated with the name
    
    # Then we can look up all of the "tracks" with that artist-id
    # search(q, limit=10, offset=0, type='track', market=None)
    #results = spotify.search("Joe Hisaishi", limit=10, type="artist")
    
    # results = spotify.search('Joe Hisaishi',
    #                          type="artist",
    #                          offset=api_offset,
    #                          limit=api_limit)

    #print(results)
    #res = json.dumps(results)
    #print(json.dumps(results,indent=4))
    # print(results.keys())
    # tracks = results['tracks']
    #print(tracks.keys())
  '''
  BEFORE LOOP:
  Connect to db
  Create a cursor
  Drop old tables
  Create new table with updated definition
  
  '''
   
    # Creates a cursor #
  cur = conn.cursor()
  #Drop old tables
  cur.execute('DROP TABLE IF EXISTS ghibli_tracks')
  # Also drop composer table XXXXXXXXXXX
  
  # Create the composer table first because tracks table will link to it.
  # id will be the primary key and is the spotify id for the artist/composer

  # CREATE composer table ....
  # Create a composers table
  cur.execute("""CREATE TABLE IF NOT EXISTS composers (
    id    TEXT PRIMARY KEY,
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
      id           TEXT PRIMARY KEY,
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
      popularity = track['popularity']  # popularity   INTEGER,
      release_date = track['album']['release_date']  # release_date TEXT,
      composer_id = track['artists'][0]['id']  # composer     TEXT,
      #genre = track['artists'][0]['genres']  # genre    TEXT,
  
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
      #print("GENRE", genre)

      # BEFORE DOING tracks table insert, search for composer by artist id and get relevant information.
      results2 = spotify.artist(composer_id)  # ??????
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


######### CALCULATIONS ############ 
    def average_popularity_score(conn,cur):
      cur.execute( "SELECT * FROM composers ")
      rows = cur.fetchall()
      conn.commit()

      sum = 0 
      for row in rows:
        sum =+ row[2]
        avg_popularity = sum/len(rows)
      
      print("Average popularity score for artists:", round (avg_popularity, 2))

    




  '''

  
  
  count = 1
  for thing in tracks['items']:
    #print(thing.keys())
    #print(thing['album'].keys())
    print(count, thing['album']['name'])
    print()
    count += 1
  
      On each pass through the loop:
  
      Come up with a way to avoid duplicates...
  
      1) Create a query string: "INSERT INTO tablename ... data"
      2) Execute the query
      3) Commit the query 
      
      '''
  '''
  close the cursor ????
  close the DB connection.
  
  
  
  
  artist_id = results['artists']['items'][0]['id']
  print(artist_id)
  
  ghibli_uri = 'spotify:artist:' + artist_id
  #spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
  
  results = spotify.artist_albums(ghibli_uri, album_type='album')
  
  albums = results['items']
  while results['next']:
      results = spotify.next(results)
      albums.extend(results['items'])
  
  for album in albums:
      print(album['name'])
  '''
  '''
  Access and store at least 100 items in your database from each API/website (10 points) in at least one table per API/website. For at least one API you must have two tables that share a key (20 points). You must not have duplicate data in your database! Do not split data from one table into two! Also, there should be only one final database!
  ● You must limit how much data you store from an API into the database each time you execute your code to 25 or fewer items (60 points). The data must be stored in a SQLite database. This means that you must run the code that stores the data multiple times to gather at least 100 items total without duplicating existing data or changing it.
  '''

 

  
  cur.close()
  conn.close()




def make_ghibli_graph():
  
  "SELECT * FROM ghibli_tracks ORDER BY popularity DESC LIMIT 10"
