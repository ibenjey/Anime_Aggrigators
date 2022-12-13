from matplotlib.pyplot import show, subplots
from numpy import mean, round
from sqlite3 import connect
from pandas import read_csv


def create_cursor():

    conn = connect('anime')
    cur = conn.cursor()
    return cur, conn


def make_quote_table(data, cur, conn):

    cur.execute("""CREATE TABLE IF NOT EXISTS Quote 
    (subreddit TEXT, title TEXT PRIMARY KEY, selftext TEXT, upvote_ratio INTEGER)""")

    for _, row in data.iterrows():
        title = row['title']
        selftext = row['selftext']
        upvote_ratio = row['upvote_ratio']

        cur.execute("""INSERT OR IGNORE INTO Quote
        (title, selftext, upvote_ratio) 
        VALUES (?, ?, ?)""", (title, selftext, upvote_ratio))

    conn.commit()


def get_average_ratio(cur):

    cur.execute("""SELECT upvote_ratio from Quote""")
    ratios = [ratio[0] for ratio in cur.fetchall()]
    return mean(ratios)


def get_average_title_length(cur):

    cur.execute("""SELECT title from Quote""")
    titles = cur.fetchall()
    lengths = [len(title[0]) for title in titles]
    return mean(lengths)


def plot_hist(cur):

    cur.execute("""SELECT upvote_ratio FROM Quote""")
    ratios = [ratio[0] for ratio in cur.fetchall()]

    cur.execute("""SELECT title FROM Quote""")
    titles = [len(ratio[0]) for ratio in cur.fetchall()]

    fig, (ax1, ax2) = subplots(1, 2)

    ax1.hist(ratios, bins=20, color='red')
    ax1.set_xlabel('Quote up-vote ratio')
    ax1.set_ylabel('Number of quotes that have this up-vote ratio')
    ax1.set_title('Distribution of the up-vote ratios', fontweight='bold')

    ax2.hist(titles, bins=20, color='blue')
    ax2.set_xlabel('Quote title length')
    ax2.set_ylabel('Number of quotes that have this title length')
    ax2.set_title('Distribution of the titles length', fontweight='bold')




if __name__ == '__main__':

    CURSOR, CONNECT = create_cursor()
    DATAFRAME = read_csv('items.csv')

    make_quote_table(DATAFRAME, CURSOR, CONNECT)
    plot_hist(CURSOR)
    average_ratio = get_average_ratio(CURSOR)
    average_length = get_average_title_length(CURSOR)
    print(f'\nThe average length of the titles is {round(average_length, 2)} characters.')
    print(f'\nThe average up-vote ratio is {round(100 * average_ratio, 2)}%.')

    show()
