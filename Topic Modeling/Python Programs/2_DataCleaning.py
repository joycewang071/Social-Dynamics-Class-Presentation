"""
Script: Chinese text cleaning and tokenization for topic modeling

Author: Xinxin Wang

Description:
  - Loads raw TXT articles and generates cleaned tokenized files using jieba.
  - Converts Chinese stopwords from Simplified to Traditional and removes them.
  - Keeps tokens whose POS tags are within a selected set (n, nr, ns, nt, a, v, d).

"""

import os

from zhconv import convert
from stopwordsiso import stopwords
stpw_s=stopwords("zh")
stpw_t=[]
for i in stpw_s:
    stpw_t.append(convert(i, 'zh-hant'))## Translate stopwords from Simplified Chinese to Traditional Chinese


# Write cleaned data
import jieba.posseg as jp, jieba

full_info=[]
words_ls=[]

jieba.add_word('脫歐',1,'n')
jieba.add_word('雨傘',1,'n')
flags = ('n', 'nr', 'ns', 'nt', 'a', 'v', 'd')
## Reference: https://www.cnblogs.com/chenbjin/p/4341930.html 
# n  common noun
# nr proper noun (person)
# ns proper noun (location)
# nt organization name
# v  verb
# a  adjective
# d  adverb

t_list = os.listdir('C:/Users/10292/Downloads/news_txt')
i=0
for t in t_list:
    with open(f"C:/Users/10292/Downloads/news_txt/{t}",encoding="utf-8") as f:
        content = ' '.join(f.readlines())
        title=t[:-4]
    ## Cut and clean a single news article
    with open(f"C:/Users/10292/Downloads/news_txt_cleaned/{t}",'a',encoding="utf-8") as f: 
        words = [w.word for w in jp.cut(content) if w.flag in flags and w.word not in stpw_t]
        f.write(' '.join(words))
    i=i+1
    print(i,t)
    ## Track which article is finished
