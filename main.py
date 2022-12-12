import sqlite3
# import animeList


# Have an import for each student's function
from anime_spotify import *
# from animeList import *

from anime_spotifycal import *
# from animeListcal import *

# from student_file_2 import fn_name
# ....
# use for loop to set variable for current row_ at each run there will be 25 items add...and so on 

# Open connection to DB -- pass the connection to each student's fn
conn = sqlite3.connect("anime.db")


# Do each student's functions
### ANIME SPOTIFY FUNCTIONS ###
get_ghibli(conn)

### ANIME LIST FUNCTIONS ###
# anime_process()
database_setup(conn)
# anime_list_table(conn)


### CALCULATIONS/VISUALIZATION FUNCTIONS ###

average_popularity_scores(conn)

# avg_anime(conn)


# TO DO #
 
 # structure main file to call the rest of the files 
