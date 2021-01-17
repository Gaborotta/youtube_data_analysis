import os
import json
from datetime import datetime
from youtube_api import get_game_video_list
from youtube_api import set_youtube_api
from google.cloud import firestore


# Project ID is determined by the GCLOUD_PROJECT environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/gaborotta/key/youtube-api-08e93f0db6eb.json'
db = firestore.Client()

doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})

doc_ref = db.collection(u'users').document(u'aturing')
doc_ref.set({
    u'first': u'Alan',
    u'middle': u'Mathison',
    u'last': u'Turing',
    u'born': 1912
})

users_ref = db.collection(u'users')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')


def get_youtube_video_list():
    """youtubeのゲーム動画を取得して出力

    Args:
        serch_word (str, optional): 検索ワード. Defaults to 'ゲーム実況'.
        publishedAfterDt (date, optional): 動画公開日範囲開始. Defaults to datetime(2020, 1, 1).date().
        publishedBeforeDt (date, optional): 動画公開日範囲終了. Defaults to datetime(2020, 1, 1).date().
        get_dt (date, optional): 情報取得日. Defaults to datetime(2021, 1, 1).date().
    """

    serch_word = 'ゲーム実況'
    publishedAfterDt = datetime.today().date()
    publishedBeforeDt = publishedAfterDt
    get_dt = publishedAfterDt

    get_dt_str = get_dt.strftime('%Y%m%d')
    youtube = set_youtube_api()

    tdt = publishedAfterDt
    publishedAfter = datetime(
        tdt.year, tdt.month, tdt.day, 0, 0, 0).isoformat()+'Z'
    tdt = publishedBeforeDt
    publishedBefore = datetime(
        tdt.year, tdt.month, tdt.day, 23, 59, 59).isoformat()+'Z'
    print(publishedAfter, publishedBefore)
    video_list = get_game_video_list(
        youtube,
        serch_word=serch_word,
        publishedAfter=publishedAfter,
        publishedBefore=publishedBefore
    )
    print(len(video_list))

    with open(f'data/{get_dt_str}_youtube_video_list.json', 'w') as f:
        json.dump(video_list, f, indent=4, ensure_ascii=False)
