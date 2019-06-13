import csv
import nltk
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from sanguozhi import talks
from matplotlib import pyplot as plt
import pandas as pd

sentences = []
for talk in talks:
    sentences.append(talk['talk'])

# print(sentences)


#提取曹操
cao_sentence = []
cao_alias = ['Cao Cao', 'Mengde', 'Lord Cao', 'Minister Cao']
for sentence in sentences:
    if any(name in sentence for name in cao_alias):
        cao_sentence.append(sentence)

cao_text = '\t'.join(cao_sentence)
cao_tag = nltk.pos_tag(word_tokenize(cao_text))
cao_tag = list(cao_tag)
adj_list = []

for tag in cao_tag:
    if tag[1] == 'JJ':
        adj_list.append(tag[0])
cao_tag = nltk.pos_tag(word_tokenize(cao_text))
print(adj_list)
adj_str = ','.join(adj_list)
adj_freq = nltk.FreqDist(adj_list)
cao_senti_dict = dict(adj_freq.most_common(50))
adj_key = list(cao_senti_dict.keys())
adj_num = list(cao_senti_dict.values())
cao_df = pd.DataFrame({'key':adj_key,'num':adj_num})
cao_df.to_csv('Cao_Cao.csv')
print(cao_df)

#生成曹操词云
cao_wc_pd = pd.read_csv('Cao_Cao_cleaned.csv')
cao_wc_df = pd.DataFrame(cao_wc_pd)
key_list = list(cao_wc_df['key'])
num_list = [int(i) for i in cao_wc_df['num']]
cao_wc_dict = dict(zip(key_list,num_list))
print(cao_wc_dict)

w = WordCloud(background_color='white', width=1440, height=960)
wc = w.generate_from_frequencies(cao_wc_dict)
wc.to_file('Cao_Cao.png')




#提取刘备
liu_sentence = []
liu_alias = ['Liu Bei', 'Lord Liu', 'First Ruler', 'Xuande', 'Imperial Uncle']
for sentence in sentences:
    if any(name in sentence for name in liu_alias):
        liu_sentence.append(sentence)

liu_text = '\t'.join(liu_sentence)
liu_tag = nltk.pos_tag(word_tokenize(liu_text))
liu_tag = list(liu_tag)
adj_list = []
for tag in liu_tag:
    if tag[1] == 'JJ':
        adj_list.append(tag[0])
print(adj_list)
liu_tag = nltk.pos_tag(word_tokenize(liu_text))
adj_str = ','.join(adj_list)
adj_freq = nltk.FreqDist(adj_list)
liu_senti_dict = dict(adj_freq.most_common(50))
adj_key = list(liu_senti_dict.keys())
adj_num = list(liu_senti_dict.values())
liu_df = pd.DataFrame({'key':adj_key,'num':adj_num})
liu_df.to_csv('Liu_Bei.csv')
print(liu_df)

#生成刘备词云
liu_wc_pd = pd.read_csv('Liu_Bei_cleaned.csv')
liu_wc_df = pd.DataFrame(liu_wc_pd)
key_list = list(liu_wc_df['key'])
num_list = [int(i) for i in liu_wc_df['num']]
liu_wc_dict = dict(zip(key_list,num_list))
print(liu_wc_dict)

w = WordCloud(background_color='white', width=1440, height=960)
wc = w.generate_from_frequencies(liu_wc_dict)
wc.to_file('Liu_Bei.png')