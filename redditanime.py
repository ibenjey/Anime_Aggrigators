from pandas import concat, DataFrame
from requests.auth import HTTPBasicAuth
from requests import get, post


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

DATAFRAME = DataFrame()
last_id = 't3_zhvbn4'
#last_id references where we were when we left off
for _ in range(4):
#I used the '_' in 'for _ in range(4)' because the iterator is not used in the loop so we do not need to create a new variable.

    res = get('https://oauth.reddit.com/r/anime/new', headers=headers, params={'limit': 25, 'after': last_id})
    res.json()

    for i, post in enumerate(res.json()['data']['children']):
        data = {'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score']}
        line = DataFrame([data])
        DATAFRAME = concat([DATAFRAME, line])
        last_id = post['kind'] + '_' + post['data']['id']

#last id loops the data for fresh results

DATAFRAME.reset_index(inplace=True, drop=True)
