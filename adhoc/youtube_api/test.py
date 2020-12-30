import re
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# # ユーザー認証あり

CLIENT_SECRETS_FILE = 'adhoc/youtube_api/client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


get_authenticated_service()


# # APIキー 動画検索とリスト取得
YOUTUBE_API_KEY = ""

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

search_response = youtube.search().list(
    part='snippet',
    # 検索したい文字列を指定
    q='ゲーム実況',
    # 視聴回数が多い順に取得
    publishedAfter=datetime(2020, 1, 1).isoformat()+'Z',
    publishedBefore=datetime(2020, 1, 7).isoformat()+'Z',
    order='viewCount',
    relevanceLanguage='ja',
    type='video',
    maxResults=50,
    videoCategoryId=20

).execute()


with open('data/test2.json', 'w') as f:
    json.dump(search_response, f, indent=4, ensure_ascii=False)

# # 動画のページを取得してゲーム名を取得
video_id = search_response['items'][10]['id']['videoId']

url = 'https://www.youtube.com/watch?v=' + video_id

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html')

finder = re.findall(
    r',"title":{"simpleText":".*"},"subtitle"', res.text)
print(finder)
geme_title = finder[0].split('"')[5]
print(geme_title)
