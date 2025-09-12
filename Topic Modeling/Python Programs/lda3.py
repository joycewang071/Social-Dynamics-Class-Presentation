import os
import pandas as pd
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel
import numpy as np

num_topics=6


## read txt and cleaned txt
full_info=[]
words_ls=[]
t_list = os.listdir('C:/Users/10292/Downloads/news_txt')
for t in t_list:
    with open(f"C:/Users/10292/Downloads/news_txt_cleaned/{t}",encoding="utf-8") as f:
        words = f.readlines()[0].split()
    words_ls.append(words)



dictionary = corpora.Dictionary(words_ls)
stopword=['香港','移民','港人','潮']
stop_ids = [dictionary.token2id[s] for s in stopword if s in dictionary.token2id]
dictionary.filter_tokens(stop_ids)
dictionary.compactify()  
corpus = [dictionary.doc2bow(words) for words in words_ls]


lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
coherence_u_mass = CoherenceModel(model=lda, texts=words_ls, dictionary=dictionary, coherence='u_mass')


# 打印所有主题，每个主题显示100个词
result=pd.DataFrame(lda.show_topics(num_topics=num_topics, num_words=100, log=False, formatted=False))
frame=[]
for i in range(num_topics):
    frame.append(pd.DataFrame(result[1][i],columns=[f'topic {i+1}',f'topic {i+1} value']))
topic_result = pd.concat(frame,axis=1)
topic_result.to_csv(f'{num_topics} topics .csv',encoding="utf-8-sig",index=False)




train_vecs = []
max_vecs=[]

for i in range(len(corpus)):
    top_topics = lda.get_document_topics(corpus[i], minimum_probability=0.0)
    topic_vec = [top_topics[i][1] for i in range(num_topics)]
    max_vecs.append([t_list[i],np.argmax(topic_vec)+1,max(topic_vec)])
    train_vecs.append(topic_vec)

max_vecs_df =pd.DataFrame(max_vecs,columns=['title','dominant_topic','contribution'])


for i in range(1,num_topics+1):
    max_vecs_df.groupby('dominant_topic').get_group(i).sort_values(by=['contribution'],ascending=False).to_csv(f'ranked articles for the dominant topic {i}.csv',encoding="utf-8-sig",index=False)

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud

for t in range(lda.num_topics):
    plt.figure()
    plt.imshow(WordCloud(background_color="white",
    font_path='simhei.ttf').fit_words(dict(lda.show_topic(t, 100))))
    plt.axis("off")
    plt.title("Topic #" + str(t+1))
    plt.show()

import shutil
import os
n_list = os.listdir('C:/Users/10292/Downloads/news')
for i in range(num_topics):
    if not os.path.exists(f'C:/Users/10292/Downloads/topic {i+1}'):
        os.makedirs(f'C:/Users/10292/Downloads/topic {i+1}')
for i in range(len(max_vecs)):
    shutil.move(f'C:/Users/10292/Downloads/news_txt - Copy/{t_list[i]}', 
                f'C:/Users/10292/Downloads/topic {max_vecs[i][1]}/{t_list[i]}')


