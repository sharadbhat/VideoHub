from fuzzywuzzy import process


def fuzzy(search_key, videos, video_titles):
    """
    - Returns a list of closest matching video IDs.
    """
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
