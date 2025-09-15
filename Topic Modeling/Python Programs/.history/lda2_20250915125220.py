"""
Script: Topic number search and topic-word export with coherence

Author: Xinxin Wang

Description:
  - Reads raw and cleaned TXT articles, builds dictionary and corpus.
  - Trains LDA models for a range of topic counts and computes UMass coherence.
  - Exports per-topic top words and a CSV of coherence vs. num_topics.

Inputs:
  - Raw TXT files: C:/Users/10292/Downloads/news_txt/{file}.txt
  - Cleaned TXT files: C:/Users/10292/Downloads/news_txt_cleaned/{file}.txt

Outputs:
  - "{num_topics} topics .csv" for each topic count with top words per topic.
  - "coherence.csv" with columns [num_topics, u_mass].

Notes:
  - Requires: gensim, pandas
  - Ensure input directories exist.
"""

import os
import pandas as pd
from gensim import corpora, models
from gensim.models.coherencemodel import CoherenceModel


if __name__ == '__main__':

    ## Read raw and cleaned TXT
    full_info=[]
    words_ls=[]
    t_list = os.listdir('C:/Users/10292/Downloads/news_txt')
    for t in t_list:
        with open(f"C:/Users/10292/Downloads/news_txt/{t}",encoding="utf-8") as f:
            content = ' '.join(f.readlines())
            title=t[:-4]
        with open(f"C:/Users/10292/Downloads/news_txt_cleaned/{t}",encoding="utf-8") as f:
            words = f.readlines()[0].split()
            words_ls.append(words)
        words_ls.append(words)
        full_info.append([title,content,words])

    full_info_df =pd.DataFrame(full_info,columns=['title','content','words'])


    # Build dictionary
    dictionary = corpora.Dictionary(words_ls)

    stopword=['香港','移民','港人','潮']
    stop_ids = [dictionary.token2id[s] for s in stopword if s in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)
    dictionary.compactify()  # Remove gaps caused by the deleted tokens

    # Create BoW corpus from tokenized documents
    corpus = [dictionary.doc2bow(words) for words in words_ls]


    coherence=[]

    for num_topics in range(3,15):
        # Train LDA model; num_topics sets the number of topics
        lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        coherence_u_mass = CoherenceModel(model=lda, texts=words_ls, dictionary=dictionary, coherence='u_mass')

        coherence.append([num_topics,coherence_u_mass.get_coherence()])
        
        # Export top words per topic (100 words)
        result=pd.DataFrame(lda.show_topics(num_topics=num_topics, num_words=100, log=False, formatted=False))
        frame=[]
        for i in range(num_topics):
            frame.append(pd.DataFrame(result[1][i],columns=[f'topic {i+1}',f'topic {i+1} value']))
        topic_result = pd.concat(frame,axis=1)
        topic_result.to_csv(f'{num_topics} topics .csv',encoding="utf-8-sig",index=False)

    coherence_df =pd.DataFrame(coherence,columns=['num_topics','u_mass'])

    coherence_df.to_csv(f'coherence.csv',encoding="utf-8-sig",index=False)

