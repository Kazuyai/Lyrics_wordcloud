from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# ファイルの読み込み
df_file = pd.read_csv("Result.csv", encoding='cp932')

# 歌詞を取り出す
lyrics = df_file['歌詞'].tolist()

t = Tokenizer()

results = []

# 全ての歌詞を調べる
for l in lyrics:
    tokens = t.tokenize(l)
    
    r = []
    
    for tok in tokens:
        if tok.base_from == '*':
            word = tok.surface
        else:
            word = tok.base_form

        ps = tok.part_of_speech

        hinshi = ps.split(',')[0]

        if hinshi in ['名詞', '形容詞', '動詞', '副詞']:
            r.append(word)

    rl = (' '.join(r)).strip()
    results.append(rl)
    
    result = [i.replace('\u3000','') for i in results]

# 全ての単語を空白で結合する
text = " ".join(result)

# フォントパスの指定
fpath = 'C:/Windows/Fonts/UDDigiKyokashoN-R.ttc'

# マスク画像の読み込み
image_mask = np.array(Image.open('mask.png'))

# 除去する単語の指定
stop_words = ['ん', 'の', 'ちゃう', 'それ', 'いく', 'する', 'いる', 'ある', 'なる', 'てる', 'ない', 'よう', 'れる', 'いい', 'そう', 'こと', 'まま']

wordcloud = WordCloud(
    width=800, 
    height=600, 
    background_color='white', 
    mask=image_mask, 
    prefer_horizontal=1,
    font_path=fpath, 
    stopwords=set(stop_words)
).generate(text)

# 画像を保存する
wordcloud.to_file('./wordcloud.png')

# 画像を表示する
plt.imshow(wordcloud,interpolation="bilinear")
plt.axis("off")
plt.show()