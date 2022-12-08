import requests 
import sqlite3
import os 

# 1: got the url request information
# process the data into a list of tuples with titles, score rating, and populairty 
def anime_process():
    url= 'https://api.jikan.moe/v4/top/anime?page={}'
    anime_info = []
    for i in range(5):
        u = url.format(i)
        response = requests.get(u)
        val = response.json()
        search_result = val['data']
        for anime_data in search_result:
            tup = (anime_data['title'], anime_data['score'], anime_data['popularity'])
            anime_info.append(tup)
    print(anime_info)

# store into sql databases 
def database_setup(anime_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+anime_name)
    cur = conn.cursor()
    return cur, conn 

# set up the table in sql and litmit the data to 25
def anime_list_table(cur, conn, anime_info): 
    cur.execute("CREATE TABLE IF NOT EXISTS anime_list (id INTEGER PRIMARY KEY, name TEXT, score INTEGER, popularity INTEGER)")
    conn.commit()


    count = cur.execute("SELECT max(id) FROM anime_list").fetchone()[0]
    if count == None:
        count = 1
# len(anime_info)+1)
#  count = -1
# for i in range(count+1,min(count+26),len(anime_info)+1)
    for i in range(count+1,count+25):
        anime_id = i
        anime_name = anime_info[i][0]
        anime_score = float(anime_info[i][1])
        anime_pop = float(anime_info[i][2])
        cur.execute('INSERT or IGNORE INTO anime_list (id, name, score, popularity ) VALUES (?, ?, ?, ?)', (anime_id, anime_name, anime_score, anime_pop))
    conn.commit()
    
    # except:
    #     return None


# maybe one for join table due to duplicate strings 
# def anime_name_table(cur, conn, anime_info):
#     cur.execute ("CREATE TABLE IF NOT EXIST anime name")
#     for i in anime_info:
#         name = anime_info[i][0]
#     print(name)

# calling the main function 
def main ():
    anime_info = anime_process()
    cur, conn = database_setup('anime.db')
    anime_list_table(cur, conn, anime_info)

if __name__ == "__main__":
    main()
