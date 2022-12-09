import sqlite3
import os 
import matplotlib.pyplot as plt
import numpy as np

def database_setup(anime_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+anime_name)
    cur = conn.cursor()
    return cur, conn 

# calculating avg artist popularity #
def average_popularity_score(conn,cur):
    cur.execute( "SELECT * FROM composers ")
    rows = cur.fetchall()
    conn.commit()

    sum = 0 
    for row in rows:
        sum += row[2]
        avg_popularity = sum/len(rows)
    
      
    print("Average popularity score for artists:", round(avg_popularity, 2))

    ### TOP 10 Popularity Ranking ####

    cur.execute("SELECT * FROM ghibli_tracks ORDER BY popularity DESC LIMIT 10")


    ##pie chart popularity avg##

plt.style.use('_mpl-gallery-nogrid')


# make data
x = [1, 2, 3, 4]
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

# plot
fig, ax = plt.subplots()
ax.pie(x, colors=colors, radius=3, center=(4, 4),
       wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()

def main():
    cur, conn = database_setup('anime.db')
    average_popularity_score(conn, cur)

if __name__ == "__main__":
    main()


# TO DO #

# write the outcome into csv file 
