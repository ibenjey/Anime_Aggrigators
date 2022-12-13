import sqlite3
import os
import csv
import matplotlib.pyplot as plt
import numpy as np


def database_setup(anime_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+anime_name)
    cur = conn.cursor()
    return cur, conn 

f = open('anime_avg.csv', "w")
writer = csv.writer(f)

 # calculating the top ten score and popularity got the info from database table
def avg_anime(cur, conn):
    cur.execute("SELECT * FROM anime_list ORDER BY id LIMIT 10")
    rows=cur.fetchall()
    conn.commit()

    sum = 0 
    for row in rows:
        sum += row[2]
        avg_top = round(sum /len(rows),2)

    for pop in rows:
        sum += pop[3]
        top_pop = round(sum / len(rows))
# calculating the top ten score and popularity 

# calculating the top bottom score and popularity 
    cur.execute("SELECT * FROM anime_list ORDER BY id DESC LIMIT 10")
    bottom_ten = (cur.fetchall())
    conn.commit()

    sum = 0 
    for bottom in bottom_ten:
        sum += bottom[2]
        avg_bot = round(sum /len(bottom_ten), 2)

    sum = 0 
    for bottom in bottom_ten:
        sum += bottom[3]
        pop_bot = round(sum /len(bottom_ten))

    header = ['Group', 'Average Score', 'Average Popularity']
    writer.writerow(header)
    row_1 = ['Top 10', avg_top, top_pop ]
    row_2 = ['Bottom 10', avg_bot, pop_bot]
    writer.writerow(row_1)
    writer.writerow(row_2)
    
def top_anime_popularity(cur, conn):
    cur.execute("SELECT * FROM anime_list ORDER by popularity")
    pop = cur.fetchall()
    conn.commit()
    
    t_pop = 0 
    for sum_t in pop:
        t_pop += sum_t[3]
    
    cur.execute("SELECT * FROM anime_list ORDER by popularity DESC LIMIT 10")
    high_pop = cur.fetchall()
    conn.commit()

    sum_pop = 0 
    for sum in high_pop:
        sum_pop += sum[3]
        sum_avg = (sum_pop/t_pop)
        total = round((sum_avg),3) * 100
    print(total)

    cur.execute("SELECT * FROM anime_list ORDER by popularity ASC LIMIT 10")
    low_pop = cur.fetchall()

    conn.commit()

    l_pop = 0 
    for sum in low_pop:
        l_pop += sum[3]
        l_avg = (l_pop/t_pop)
        l_total = round((l_avg),3) * 100 
    print(l_total)
        

    header = ['percentage']
    writer.writerow(header)
    row1 = ['highest 10', total]
    row2 = ['lowest 10', l_total]
    writer.writerow(row1)
    writer.writerow(row2)


# visiualization on average scores and popularity of top ten and bottom ten ranking
def visual():
    bar_1 = plt.subplot2grid((3,3), (0,0), rowspan=4)
    bar_2 = plt.subplot2grid((3,3), (0,2), rowspan=3)

    bar1_y = [9, 8.56]
    bar2_y = [410, 910]
    bar_colors = ['tab:purple', 'tab:cyan']
    bar1_colors = ['tab:olive', 'tab:brown']
    bar1_x = ['top ten', 'bottom ten']
    bar2_x = ['top pop', 'bottom pop']
 
    bar_1.bar(bar1_x, bar1_y, color = bar_colors)
    bar_1.set_title('Score')
    bar_1.set_xlabel('anime score')
    bar_1.set_ylabel('Averages of top ten and bottom ten scores')

    bar_2.bar(bar2_x, bar2_y, color = bar1_colors)
    bar_2.set_title("popularity")
    bar_2.set_xlabel('anime popularity')
    bar_2.set_ylabel('Averages of top and bottom ten popularity')

    
    plt.tight_layout()
    plt.show()

def visual_2():



    y = np.array([47.8, 0.4])
    mylabels = ['highest pop percent', 'lowest pop percent']
    plt.pie(y, labels= mylabels)
    plt.show()

def main():
    cur, conn = database_setup('anime.db')
    avg_anime(cur, conn)
    top_anime_popularity(cur, conn)
    visual()
    visual_2()
if __name__ == "__main__":
    main()
