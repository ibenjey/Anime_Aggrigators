import sqlite3
<<<<<<< HEAD
# import animeList
=======

>>>>>>> 4a9cba54ddd58eb3e1216766d76ac86a769cfab4


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

<<<<<<< HEAD
### ANIME LIST FUNCTIONS ###
# anime_process()
database_setup(conn)
# anime_list_table(conn)


### CALCULATIONS/VISUALIZATION FUNCTIONS ###

average_popularity_scores(conn)

# avg_anime(conn)
=======

# ... call next student's function
# ...
>>>>>>> 4a9cba54ddd58eb3e1216766d76ac86a769cfab4


<<<<<<< HEAD
# TO DO #
 
 # structure main file to call the rest of the files 
=======

# calling the main function 
def main ():
    anime_info = anime_process()
    cur, conn = database_setup('anime.db')
    anime_list_table(cur, conn, anime_info)

if __name__ == "__main__":
    main()
>>>>>>> 4a9cba54ddd58eb3e1216766d76ac86a769cfab4
