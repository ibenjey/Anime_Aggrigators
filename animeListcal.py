import sqlite3
import os
from statistics import mean 

def database_setup(anime_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+anime_name)
    cur = conn.cursor()
    return cur, conn 

 # calculating the top ten score and popularity 
def avg_anime(cur, conn):
    cur.execute("SELECT * FROM anime_list ORDER BY id LIMIT 10")
    rows=cur.fetchall()
    conn.commit()

    sum = 0 
    for row in rows:
        sum += row[2]
        avg_row = sum /len(rows)

    print("Top ten anime score:", round(avg_row,2))

    for pop in rows:
        sum += pop[3]
        avg_sum = sum / len(rows)
    print("Top ten anime popularity:", round(avg_sum,2))
# calculating the top ten score and popularity 

# calculating the top bottom score and popularity 
    cur.execute("SELECT * FROM anime_list ORDER BY id DESC LIMIT 10")
    bottom_ten = (cur.fetchall())
    conn.commit()

    sum = 0 
    for bottom in bottom_ten:
        sum += bottom[2]
        avg_bottom = sum /len(bottom_ten)
    print("Bottom ten anime score:" , round(avg_bottom,2))

    sum = 0 
    for bottom in bottom_ten:
        sum += bottom[3]
        avg_bottom = sum /len(bottom_ten)
    print("Bottom ten anime popularity:" , round(avg_bottom,2))



    # sum = 0
    # for bottom in bottom_ten:
    #     sum += int(bottom[2])
    #     bottom_avg = mean(sum)
    # print(bottom_avg)




def main():
    cur, conn = database_setup('anime.db')
    avg_anime(cur, conn)

if __name__ == "__main__":
    main()
