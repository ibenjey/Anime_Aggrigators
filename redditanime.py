import pandas as pd
from pandas import concat, DataFrame
from requests.auth import HTTPBasicAuth
from requests import get, post
import os

CLIENT_ID = 'ybzSQ_p5Df4YV9nR1A302g'
SECRET_KEY = 'jjQ9y93ltDGLnPoAViXgREeb7WHZgQ'

auth = HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {'grant_type': 'password',
        'username': 'josephquick',
        'password': '220586Jq$'}
headers = {'User-Agent': 'MyAPI/0.0.1'}

res = post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}



def add_items(n_items=25):

    dataframe = pd.read_csv('items.csv')
    if dataframe.shape[0] == 0:
        last_id = 't3_zhvbn4'
    else:
        last_id = dataframe.iloc[-1, -1]

    res = get('https://oauth.reddit.com/r/anime/new', headers=headers, params={'limit': n_items, 'after': last_id})
    res.json()

    for i, post in enumerate(res.json()['data']['children']):
        data = {'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score'],
                'id': post['kind'] + '_' + post['data']['id']}
        line = DataFrame([data])
        dataframe = concat([dataframe, line])
    dataframe.reset_index(inplace=True, drop=True)
    dataframe.to_csv('items.csv')


if __name__ == '__main__':

    add_items()
