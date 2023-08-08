#!usr/bin/python3
""Counts words""
import requests

def count_words(subreddit, word_list, after=None, counts={}):
    if not word_list:
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Reddit Keyword Counter"}

    params = {"limit": 100}
    if after:
        params["after"] = after

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()["data"]
        children = data["children"]

        for child in children:
            title = child["data"]["title"].lower()
            for word in word_list:
                if title.count(word) > 0:
                    if word in counts:
                        counts[word] += title.count(word)
                    else:
                        counts[word] = title.count(word)

        after = data["after"]
        if after:
            count_words(subreddit, word_list, after, counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
    else:
        print("Error:", response.status_code)
