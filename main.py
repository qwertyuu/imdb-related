import json
import re
from multiprocessing.pool import ThreadPool

import requests
from bs4 import BeautifulSoup as Soup

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


def get_relateds(data):
    index, tt = data
    print(f"getting {tt=} {index=}")
    a = requests.get(f"https://www.imdb.com/title/{tt}/?ref_=nv_sr_srsg_0", headers=headers)
    related_tree = []

    soup = Soup(a.content, features="lxml")
    elems = soup.select('[data-testid="MoreLikeThis"] [data-testid="shoveler-items-container"] > div')
    print(len(elems))

    for elem in elems:
        href = elem.select_one('a.ipc-lockup-overlay.ipc-focusable').get("href")
        tts = re.findall('tt[0-9]+', href)
        assert len(tts) == 1, "Oops, wtf"
        related_tree.append(tts[0])
    return tt, related_tree


with ThreadPool(100) as pool:
    # execute tasks, block until all completed
    with open("movielist.txt", "r") as fp:
        movies_list_tts = fp.read().split("\n")
    print(movies_list_tts)
    movielists = pool.map(get_relateds, list(enumerate(movies_list_tts)))
    print(json.dumps(movielists))
