import json
from datetime import datetime
from lib.mylib.youtube_api import get_game_video_list
from lib.mylib.youtube_api import get_game_title_list_youtube
from lib.mylib.youtube_api import get_game_video_summary_list
from lib.mylib.youtube_api import set_youtube_api
from lib.mylib.out_csv import csv_writer


def get_youtube_data(
    serch_word='ゲーム実況',
    publishedAfterDt=datetime(2020, 1, 1).date(),
    publishedBeforeDt=datetime(2020, 10, 1).date(),
    get_dt=datetime(2021, 1, 1).date()
):
    """youtubeのゲーム動画を取得して出力

    Args:
        serch_word (str, optional): 検索ワード. Defaults to 'ゲーム実況'.
        publishedAfterDt (date, optional): 動画公開日範囲開始. Defaults to datetime(2020, 1, 1).date().
        publishedBeforeDt (date, optional): 動画公開日範囲終了. Defaults to datetime(2020, 1, 1).date().
        get_dt (date, optional): 情報取得日. Defaults to datetime(2021, 1, 1).date().
    """
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

    video_id_list = [
        video['id']['videoId']
        for video in video_list
    ]
    print(len(video_id_list))

    video_sumamry_list = get_game_video_summary_list(youtube, video_id_list)
    with open(f'data/{get_dt_str}_youtube_video_summary_list.json', 'w') as f:
        json.dump(video_sumamry_list, f, indent=4, ensure_ascii=False)

    game_title_list = get_game_title_list_youtube(video_id_list)
    csv_writer(
        f'data/{get_dt_str}_youtube_game_title_list.csv',
        game_title_list, ['video_id', 'game_title']
    )


get_youtube_data()
