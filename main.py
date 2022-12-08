import sqlite3
import animeList


# Have an import for each student's function
from anime_spotify import *
# from student_file_2 import fn_name
# ....


# Open connection to DB -- pass the connection to each student's fn
conn = sqlite3.connect("anime.db")


# Do each student's functions
get_ghibli(conn)
# ... call next student's function
# ...

# Call any other functions for calculations, graphs, etc.
# make_ghibli_graph()

