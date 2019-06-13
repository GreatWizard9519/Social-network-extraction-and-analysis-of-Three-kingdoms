import json
import csv
import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx
from Alias_match import combine_tag_name_alis
from Alias_match import combine_tag_name_alis_set

import copy

# G=nx.Graph()
# G.add_nodes_from(node)
# G.add_edges_from(edge)
# nx.write_gexf(G,'your_file_name.gexf')

with open('prediction_output/predictions.json','r') as f:
    load_dict = json.load(f)


#删除角色列表中不必要的元素,数据清理
speaker_list = list(load_dict.values())
speaker_list_cleaned = []
for i in speaker_list:
    if '“' not in i and '”' not in i and len(i) <= 30 and i not in ['he','she','they','his','her','we','They','He','the','The','People','and','one','men'] and not len(i) == 1:
        speaker_list_cleaned.append(i)

count = 0
for i in speaker_list_cleaned:
    if 'asked' in i:
        speaker_list_cleaned[count] = speaker_list_cleaned[count].replace(' asked','')
    count += 1

# print('speaker_list_cleaned:', speaker_list_cleaned)
# print(len(speaker_list_cleaned))

#别名替换
data1 = pd.read_excel('alias_database.xlsx')  # 别名集
alias = list(data1['alias'])
speaker_list_cleaned_dict = {'key': speaker_list_cleaned}
# print(speaker_list_cleaned_dict)
data2 = pd.DataFrame(speaker_list_cleaned_dict)  # 标签集
name = combine_tag_name_alis_set(data1, data2)
name_tmp = []
for i in name:
    if ' ' in i:
        name_tmp.append(i)
name = name_tmp
# print('别名替换后:',name)
alias = list(set(name+alias))
# print('alias',alias)
alias_cleaned = []
for i in alias:
    if '“' not in i and '”' not in i and len(i) <= 30 and i not in ['he','she','they','his','her','we','They','He','the','The','People','and','one','men'] and not len(i) == 1:
        alias_cleaned.append(i)

# print('alias_cleaned',alias_cleaned)



# word = []
# counter = {}
# for i in speaker_list_cleaned:
#     if not i in word:
#         word.append(i)
#     if not i in counter:
#         counter[i] = 0
#     else:
#         counter[i] += 1
# counter_list = sorted(counter.items(), key=lambda x:x[1], reverse=True)
# counter_list_dict = dict(counter_list)



#建立人物关系
# names_dict = counter_list_dict  # 姓名字典
# names_list = list(set(speaker_list_cleaned))
relationships = {}  # 关系字典
lineNames = []  # 每段内人物关系
names_appear = []  # 出现人物字典

# names_dict = list(names_dict.items())
#
# names_dict = dict(names_dict)


#一共把文章分为5段逐一分析
for iters in range(1,6):
    relationships = {}  # 关系字典
    lineNames = []  # 每段内人物关系
    names_appear = []  # 出现人物字典

    with open('sanguozhi_segments/seg%s/sanguozhi_seg%s.txt' % (iters, iters),'r') as f:
        for line in f.readlines():
            for i in alias_cleaned:
                if i in line:
                    names_appear.append(i)
    print(names_appear)
    print(len(names_appear))
    data1 = pd.read_excel('alias_database.xlsx')  # 别名集
    names_appear_dict = {'key': names_appear}
    data2 = pd.DataFrame(names_appear_dict)  # 标签集
    names_appear = combine_tag_name_alis(data1, data2)
    # print('names_appear', names_appear)
    names_appear_tmp = []
    print(len(names_appear))
    for i in names_appear:
        if ' ' in i:
            names_appear_tmp.append(i)
    names_appear = names_appear_tmp
    print(len(names_appear))
    names_rank = copy.copy(names_appear)
    # print('rank',names_rank)


    with open('sanguozhi_segments/seg%s/sanguozhi_seg%s.txt' % (iters, iters), 'r') as f:
        for line in f.readlines():
            lineNames.append([])
            for i in alias_cleaned:
                if i in line:
                    if iters == 1 and i == 'Sima Yi':
                        continue
                    lineNames[-1].append(i)
                    relationships[i] = {}


    # print('lineNames',lineNames)
    lineNames_tmp = []
    for i in lineNames:
        i_dict = {'key':i}
        data2 = pd.DataFrame(i_dict)
        i = combine_tag_name_alis(data1, data2)
        if iters <= 2 and ('Sima Yi' in i or 'Xu Shu' in i or 'Ma Chao' in i or 'Zhao Yun' in i):
            continue
        if iters == 3 and ('Sima Yi' in i or 'Ma Chao' in i):
            continue
        if iters == 4 and ('Sima Yi' in i):
            continue
        else:
            lineNames_tmp.append(i)
    lineNames = lineNames_tmp
    if 'Sima Yi' not in lineNames:
        print('true')

    #寻找edge，人物关系
    for line in lineNames:
        print(line)
        for name1 in line:
            if name1 == 'Sima Yi':
                print('wocao')
            for name2 in line:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None:
                    relationships[name1][name2] = 1
                else:
                    relationships[name1][name2] = relationships[name1][name2] + 1
    # print('relationships',relationships)


    #统计本章中人物出现的词频
    def freq_ramking():
        with open('sanguozhi_segments/seg%s/seg%s_rank.csv' % (iters, iters),'w') as csvfile_freq_rank:
            csv_writer = csv.writer(csvfile_freq_rank)
            csv_writer.writerow(['character', 'count'])

            word = []
            counter = {}
            for i in names_rank:
                if not i in word:
                    word.append(i)
                if not i in counter:
                    counter[i] = 0
                else:
                    counter[i] += 1
            counter_list = sorted(counter.items(), key=lambda x: x[1], reverse=True)
            global counter_list_dict
            counter_list_dict = dict(counter_list)
            csv_writer.writerows(counter_list)
            # print(counter_list)
        w = WordCloud(background_color='white', width=1440, height=960)
        wc = w.generate_from_frequencies(counter_list_dict)
        wc.to_file('sanguozhi_segments/seg5/seg5_wordcloud.png')
        plt.imshow(wc)
        plt.axis('off')
        # return plt.show()
    freq_ramking()
    #输出人物关系
    #输出node
    with open('sanguozhi_segments/seg%s/sanguozhi_seg%s_node.txt' % (iters, iters), 'w') as f:
        f.write("Id Label Weight\r\n")
        for name, times in counter_list_dict.items():
            f.write(name + " " + name + " " + str(times) + "\r\n")

    list_node = []
    for name, times in counter_list_dict.items():
        list_node.append([name, name, times])

    df1=pd.DataFrame(list_node, columns=['Id', 'Label', 'weight'])
    df1.to_csv('sanguozhi_segments/seg%s/sanguozhi_seg%s_node.csv' % (iters, iters), index=False)

    #输出edge
    with open('sanguozhi_segments/seg%s/sanguozhi_seg%s_edge.txt' % (iters, iters),'w') as f:
        f.write('Source Target Weight\r\n')
        for name, edges in relationships.items():
            for v,w in edges.items():
                if w > 3 :
                    f.write(name + '' + v + '' + str(w) + '\r\n')

    list_edge = []
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                list_edge.append([name, v, str(w)])

    df2 = pd.DataFrame(list_edge, columns=['Source', 'Target', 'weight'])
    df2.to_csv('sanguozhi_segments/seg%s/sanguozhi_seg%s_edge.csv' % (iters, iters), index=False)
    print('要进行到第%s轮了',(str(iters+1)))