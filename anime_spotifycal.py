import sqlite3
import os 
import matplotlib.pyplot as plt
import numpy as np
import csv

def database_setup(anime_name):
    _path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(_path+'/'+anime_name)
    cur = conn.cursor()
    return cur, conn 

### writing calculations to text file ####
f = open('spotify_data.csv', "w")
writer = csv.writer(f)

# calculating avg artist popularity #
def average_popularity_scores(conn,cur):
    cur.execute( "SELECT * FROM composers ")
    rows = cur.fetchall()
    conn.commit()

    sum = 0 
    for row in rows:
        sum += row[3]
        avg_popularity = sum/len(rows)
    
     
    print("Average popularity score for artists:", round(avg_popularity, 2))

    ### TOP 10 Popularity Ranking ####
  
    cur.execute("SELECT * FROM ghibli_tracks ORDER BY popularity DESC LIMIT 10")
    rows = cur.fetchall()

    conn.commit()

    sum = 0 
    for row in rows:
        sum += row[2]
        avg_row_top = sum /len(rows)

    print("Average of top 10 popularity scores", round(avg_row_top,2))

    ## BOTTOM 10 popularity ranking ##

    cur.execute("SELECT * FROM ghibli_tracks ORDER BY popularity ASC LIMIT 10")
    rows = cur.fetchall()
   
    conn.commit()

    sum = 0 
    for row in rows:
        sum += row[2]
        avg_row = sum /len(rows)
    print(avg_row)
    print("Average of lower 10 popularity scores", round(avg_row,2))
    
    ## writes cvs ##
    header = ["Group", "Average Album Popularity"]
    writer.writerow(header)
    row_1 = ['Top 10 pop', avg_row_top]
    row_2 = ['Bottom 10 pop', avg_row]
    writer.writerow(row_1)
    writer.writerow(row_2)
   
def avg_album_pop_vis():
    x = ['Top 10, Bottom 10']
    top_int = [61.7]
    bottom_int = [20.6]

    x_axis = np.arange(len(x))

    plt.bar(x_axis - 0.02,top_int, 0.04, label = 'Top Average')
    plt.bar(x_axis + 0.02, bottom_int, 0.04, label = 'Bottom Average')

    plt.xticks(x_axis, x)
    plt.xlabel("Compared Popularity Averages")
    plt.ylabel("Score Integers")
    plt.title("Average Ghibli Album Scores")
    plt.legend()
    plt.show()

   
   
   
  #### JOINING ghibli_tracks table with composers table and writing a scatter plot to see a correlation ####
def plot_release_dates(conn,cur):
    #cur.execute("SELECT release_date FROM ghibli_tracks ORDER BY release_date limit 100")
    cur.execute('''
    SELECT release_date, composers.popularity
    FROM ghibli_tracks 
    LEFT JOIN composers ON ghibli_tracks.composer_id = composers.id
    ORDER BY release_date limit 50
    ''')
    rows = cur.fetchall()
    y = []
    for row in rows:
        print(row)
        y.append(row[1])

    x = list(range(0,len(rows)))
    plt.scatter(x, y)
    plt.xlabel("Release Dates Past to Present")
    plt.ylabel("Popularity Scores")
    plt.title("Popularity Scores Plotted by the Release Dates")
    plt.show()
    

   


def main():
    cur, conn = database_setup('anime.db')
    average_popularity_scores(conn, cur)
    plot_release_dates(conn,cur)
    avg_album_pop_vis()


if __name__ == "__main__":
    main()


# TO DO #

# write the outcome into csv file 
#write calculation that pulls from both composers and ghibli table. 