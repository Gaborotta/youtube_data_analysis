import json
from datetime import datetime
from lib.mylib import youtube_api

# # テスト


serch_word = 'ゲーム実況'
publishedAfter = datetime(2020, 1, 1, 0, 0, 0).isoformat()+'Z'
publishedBefore = datetime(2020, 2, 1, 23, 59, 59).isoformat()+'Z'
video_list = get_game_video_list(
    youtube,
    serch_word=serch_word,
    publishedAfter=publishedAfter,
    publishedBefore=publishedBefore
)
print(len(video_list))

with open('data/test2.json', 'w') as f:
    json.dump(video_list, f, indent=4, ensure_ascii=False)

# game_title = get_game_title_youtube(game_list[1]['id']['videoId'])
video_id_list = [
    video['id']['videoId']
    for video in video_list
]
print(len(video_id_list))

game_title_list = get_game_title_list_youtube(video_id_list)

url = 'https://www.youtube.com/watch?v=' + 'YUpIpEOtYBE'

dic = get_game_video_summary_list(youtube, video_id_list)
