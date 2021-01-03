import re
import requests
import json
from datetime import datetime
from time import sleep
from apiclient.discovery import build


# # APIキー 動画検索とリスト取得
with open('setting/setting.json', "r") as f:
    settings = json.load(f)

YOUTUBE_API_KEY = settings['YOUTUBE_API_KEY']

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


def get_game_video_api(youtube, serch_word, publishedAfter, publishedBefore, pageToken=None):
    """対象期間中に公開されたゲームカテゴリの動画を取得

    Args:
        youtube (obj): youtubeAPI
        serch_word (str): 検索ワード. 
        publishedAfter (str): 公開日時範囲の開始. 
        publishedBefore (str): 公開日時範囲の終了.
        pageToken (str, optional):ページトークン. defalut value:None

    Returns:
        dict: APIの取得結果をそのまま
    """
    search_response_dict = youtube.search().list(
        part='snippet',
        # 検索したい文字列を指定
        q=serch_word,
        # 視聴回数が多い順に取得
        publishedAfter=publishedAfter,
        publishedBefore=publishedBefore,
        order='viewCount',
        relevanceLanguage='ja',
        type='video',
        maxResults=50,
        videoCategoryId=20,
        pageToken=pageToken

    ).execute()

    return search_response_dict


def get_game_video_list(
    youtube,
    serch_word='ゲーム実況',
    publishedAfter=datetime(2020, 1, 1).isoformat()+'Z',
    publishedBefore=datetime(2020, 1, 7).isoformat()+'Z',
):
    """ゲーム動画のリストを取得

    Args:
        youtube (obj): youtube api
        serch_word (str, optional): 検索ワード. Defaults to 'ゲーム実況'.
        publishedAfter (str, optional): 公開日範囲開始. Defaults to datetime(2020, 1, 1).isoformat()+'Z'.
        publishedBefore (str, optional): 公開日範囲終了. Defaults to datetime(2020, 1, 7).isoformat()+'Z'.

    Returns:
        list: ゲーム動画のリスト
    """
    game_list = []
    next_page = None
    while True:
        res_dict = get_game_video_api(
            youtube, serch_word,
            publishedAfter, publishedBefore,
            pageToken=next_page
        )
        print('resultsPerPage', res_dict['pageInfo']['resultsPerPage'])
        game_list += res_dict['items']

        if res_dict['pageInfo']['resultsPerPage'] >= 50:
            next_page = res_dict['nextPageToken']
        else:
            break

    return game_list


def get_game_title_youtube(video_id):
    """動画のページを取得してゲーム名を取得

    Args:
        video_id (str): 動画ID

    Returns:
        str: ゲーム名
    """
    # video_id = search_response['items'][10]['id']['videoId']

    url = 'https://www.youtube.com/watch?v=' + video_id

    res = requests.get(url)
    finder = re.findall(
        r',"title":{"simpleText":".*"},"subtitle"', res.text
    )
    print(finder)
    if len(finder) != 0:
        game_title = finder[0].split('"')[5]
    else:
        game_title = None
    print(game_title)
    return game_title


def get_game_title_list_youtube(video_id_list):
    """ゲーム名をリストで取得

    Args:
        video_id_list (str list): 動画IDのリスト

    Returns:
        (str,str) list: 動画IDとゲーム名のリスト
    """
    game_title_list = []
    for video_id in video_id_list:
        game_title = get_game_title_youtube(video_id)
        game_title_list.append((video_id, game_title))
        sleep(2)
    return game_title_list


def get_game_video_summary_api(youtube, video_id_list, pageToken=None):
    """動画の統計情報等を取得

    Args:
        youtube (obj): youtube api
        video_id_list (str list): 動画IDのリスト
        pageToken (str, optional): ページトークン. Defaults to None.

    Returns:
        dict: API取得結果
    """
    statistics = youtube.videos().list(
        part=['snippet', 'statistics', 'player'],
        id=video_id_list,
        videoCategoryId=20,
        maxResults=50,
        pageToken=pageToken
    ).execute()

    return statistics


def get_game_video_summary_list(youtube, video_id_list):
    """ゲーム動画のリストを取得

    Args:
        youtube (obj): youtube api
        video_id_list (str list, optional): 動画IDのリスト

    Returns:
        list: ゲーム動画の統計情報リスト
    """
    video_summary_list = []
    next_page = None
    n = 50
    video_id_list_list = [
        video_id_list[idx:idx + n]
        for idx in range(0, len(video_id_list), n)
    ]

    for v_list in video_id_list_list:
        res_dict = get_game_video_summary_api(
            youtube, v_list,
            pageToken=next_page
        )
        print('resultsPerPage', res_dict['pageInfo']['resultsPerPage'])
        video_summary_list += res_dict['items']

    return video_summary_list
