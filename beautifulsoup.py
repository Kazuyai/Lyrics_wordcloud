import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

'''
アーティスト番号を入力する
'''
# アーティスト番号
ARTIST_NUM = 126


# サイトURL
SITE_URL = "https://www.uta-net.com"
# 曲一覧ページURL
default_url = SITE_URL + "/artist/" + str(ARTIST_NUM)

result_df = pd.DataFrame(columns=['曲名', '作詞', '作曲', '発売日', '表示回数', '歌詞'])

res = requests.get(default_url)
soup = BeautifulSoup(res.content, "html.parser")

# 全ページ数を調べる
page_text = soup.find('div', class_ = "col-7 col-lg-3 text-start text-lg-end d-none d-lg-block").text
page_count = page_text[page_text.find("全") + 1]

# 全ページ分調べる
for page_num in range(int(page_count)):
    page_url = default_url + "/0/" + str(page_num + 1)
    res = requests.get(page_url)
    soup = BeautifulSoup(res.content, "html.parser")

    # 現在のページに載っている曲のURLを全て取得する
    links = soup.find_all('td', class_ = "sp-w-100 pt-0 pt-lg-2")
    
    # 現在のページに載っている曲の情報を取得する
    for link in links:
        # 曲のURLを取得
        music_url = SITE_URL + link.a.get('href')
        
        res = requests.get(music_url)
        soup = BeautifulSoup(res.content, "html.parser")

        # 曲名、作詞、作曲、発売日、表示回数を取得する
        name = soup.find('h2').text
        detail = soup.find('p', class_ = "detail").text
        writer = re.search(r'作詞：(.+)', detail).group(1)
        composer = re.search(r'作曲：(.+)', detail).group(1)
        release_date = re.search(r'\d{4}/\d{2}/\d{2}', detail).group()
        impressions = re.search(r'この曲の表示回数：(.*)回', detail).group(1)
        
        # 歌詞を取得
        lyrics = soup.find(id = "kashi_area").text.replace('\n', '').replace('　', '')
        
        add_row = pd.DataFrame([[name, writer, composer, release_date, impressions, lyrics]], columns=result_df.columns)
        result_df = pd.concat([result_df, add_row], axis=0, ignore_index=True)

        # サーバへの負荷を軽減するため待機
        time.sleep(1)
    

# 書き込む
with open("Result.csv", mode="w", encoding="shift-jis", errors="ignore", newline="") as f:
    result_df.to_csv(f)