import os

from zhconv import convert
from stopwordsiso import stopwords
stpw_s=stopwords("zh")
stpw_t=[]
for i in stpw_s:
    stpw_t.append(convert(i, 'zh-hant'))##從簡體漢字逐字翻譯為繁體漢字


#Write cleaned data
import jieba.posseg as jp, jieba

full_info=[]
words_ls=[]

jieba.add_word('脫歐',1,'n')
jieba.add_word('雨傘',1,'n')
flags = ('n', 'nr', 'ns', 'nt', 'a', 'v', 'd')
##https://www.cnblogs.com/chenbjin/p/4341930.html 
#n	普通名词
#nr	人名
#ns	地名
#nt	机构名	
#v	普通动词
#a	形容词	
#d	副词

t_list = os.listdir('C:/Users/10292/Downloads/news_txt')
i=0
for t in t_list:
    with open(f"C:/Users/10292/Downloads/news_txt/{t}",encoding="utf-8") as f:
        content = ' '.join(f.readlines())
        title=t[:-4]
    ## cut and clean one news article
    with open(f"C:/Users/10292/Downloads/news_txt_cleaned/{t}",'a',encoding="utf-8") as f: 
        words = [w.word for w in jp.cut(content) if w.flag in flags and w.word not in stpw_t]
        f.write(' '.join(words))
    i=i+1
    print(i,t)
    ## track which article is finished
