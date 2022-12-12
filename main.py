import sqlite3



# Have an import for each student's function
from anime_spotify import *
from animeList import *
# from student_file_2 import fn_name
# ....


# Open connection to DB -- pass the connection to each student's fn
conn = sqlite3.connect("anime.db")


# Do each student's functions
get_ghibli(conn)


# ... call next student's function
# ...

# Call any other functions for calculations, graphs, etc.


# calling the main function 
def main ():
    anime_info = anime_process()
    cur, conn = database_setup('anime.db')
    anime_list_table(cur, conn, anime_info)

if __name__ == "__main__":
    main()