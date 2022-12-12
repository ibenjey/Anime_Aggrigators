from matplotlib.pyplot import hist, show, title, xlabel, ylabel
from redditanime import DATAFRAME
from sqlite3 import connect
from numpy import mean


def create_cursor():

    conn = connect('anime.db')
    cur = conn.cursor()
    return cur, conn


def make_quote_table(data, cur, conn):

    cur.execute("""CREATE TABLE IF NOT EXISTS Quote 
    (subreddit TEXT, title TEXT PRIMARY KEY, selftext TEXT, upvote_ratio INTEGER)""")

    for _, row in data.iterrows():
        subreddit = row['subreddit']
        title = row['title']
        selftext = row['selftext']
        upvote_ratio = row['upvote_ratio']

        cur.execute("""INSERT OR IGNORE INTO Quote
        (subreddit, title, selftext, upvote_ratio) 
        VALUES (?, ?, ?, ?)""", (subreddit, title, selftext, upvote_ratio))

    conn.commit()


def get_average_title_length(cur):

    cur.execute("""SELECT title from Quote""")
    titles = cur.fetchall()
    lengths = [len(title[0]) for title in titles]
    return mean(lengths)


def plot_ratios(cur):

    cur.execute("""SELECT upvote_ratio FROM Quote""")
    ratios = [ratio[0] for ratio in cur.fetchall()]
    hist(ratios, bins=20)
    xlabel('Quote up-vote ratio')
    ylabel('Number of quotes that have this up-vote ratio')
    title('Distribution of the up-vote ratios', fontweight='bold')

#upvote ratios


if __name__ == '__main__':

    CURSOR, CONNECT = create_cursor()

    make_quote_table(DATAFRAME, CURSOR, CONNECT)
    plot_ratios(CURSOR)
    average_length = get_average_title_length(CURSOR)
    print(f'\nThe average length of the titles is {average_length} characters.')

    show()
