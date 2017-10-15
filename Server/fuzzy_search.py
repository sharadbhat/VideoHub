from fuzzywuzzy import process
import pymysql


def fuzzy(search_key):
    db = pymysql.connect(host="localhost", user="root", passwd="shamanmb", db="video")
    cur = db.cursor()

    cur.execute("SELECT video_ID, video_title FROM videos")
    videos = {}
    video_titles = []
    for video in cur.fetchall():
        video_titles.append(video[1])
        videos.update({video[0] : video[1]})

    best_matches = process.extract(search_key, video_titles, limit=10)
    best_match_titles = []
    for match in best_matches:
        best_match_titles.append(match[0])
    best_match_IDs = []
    for title in best_match_titles:
        for ID in videos:
            if title == videos[ID]:
                best_match_IDs.append(ID)

    return best_match_IDs
