import json
import csv
import re
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx

# G=nx.Graph()
# G.add_nodes_from(node)
# G.add_edges_from(edge)
# nx.write_gexf(G,'your_file_name.gexf')

with open('prediction_output/predictions.json','r') as f:
    load_dict = json.load(f)


#删除角色列表中不必要的元素
speaker_list = list(load_dict.values())
speaker_list_cleaned = []
for i in speaker_list:
    if not len(i) <= 3:
        speaker_list_cleaned.append(i)
for i in speaker_list_cleaned:
    if i == 'King':
        speaker_list_cleaned.remove(i)
    elif not ' ' in i:
        speaker_list_cleaned.remove(i)

word = []
counter = {}
for i in speaker_list_cleaned:
    if not i in word:
        word.append(i)
    if not i in counter:
        counter[i] = 0
    else:
        counter[i] += 1
counter_list = sorted(counter.items(), key=lambda  x:x[1], reverse=True)
counter_list_dict = dict(counter_list)



#建立人物关系
# names_dict = counter_list_dict  # 姓名字典
names_list = list(set(speaker_list_cleaned))

for iters in range(1, 6):

    relationships = {}  # 关系字典
    lineNames = []  # 每段内人物关系
    names_appear = []  # 出现人物字典

    # names_dict = list(names_dict.items())
    #
    #
    # for i in names_dict:
    #     if not ' ' in i[0]:
    #         names_dict.remove(i)
    # names_dict = dict(names_dict)
    # print(names_dict)

    for i in names_list:
        if i == 'King':
            names_list.remove(i)
        elif not ' ' in i:
            names_list.remove(i)

    with open('sanguo_segments/seg%s/sanguo_seg%s.txt' % (iters, iters), 'r') as f:
        for line in f.readlines():
            lineNames.append([])
            for i in names_list:
                if i in line:
                    lineNames[-1].append(i)
                    relationships[i] = {}
                    names_appear.append(i)

    for line in lineNames:
        for name1 in line:
            for name2 in line:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None:
                    relationships[name1][name2] = 1
                else:
                    relationships[name1][name2] = relationships[name1][name2] + 1


    #统计本章中人物出现的词频
    def freq_ramking():
        with open('sanguo_segments/seg%s/seg%s_rank.csv' % (iters, iters), 'w') as csvfile_freq_rank:
            csv_writer = csv.writer(csvfile_freq_rank)
            csv_writer.writerow(['character','count'])

            word = []
            counter = {}
            for i in names_appear:
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
        wc.to_file('sanguo_segments/seg%s/seg%s_wordcloud.png' % (iters, iters))
        plt.imshow(wc)
        plt.axis('off')
        # return plt.show()

    freq_ramking()

    #输出人物关系
    #输出node
    with open('sanguo_segments/seg%s/sanguo_seg%s_node.txt' % (iters, iters), 'w') as f:
        f.write("Id Label Weight\r\n")
        for name, times in  counter_list_dict.items():
            f.write(name + " " + name + " " + str(times) + "\r\n")

    list_node = []
    for name, times in counter_list_dict.items():
        list_node.append([name, name, times])

    df1=pd.DataFrame(list_node, columns=['Id', 'Label', 'weight'])
    df1.to_csv('sanguo_segments/seg%s/sanguo_seg%s_node.csv' % (iters, iters), index=False)

    #输出edge
    with open('sanguo_segments/seg%s/sanguo_seg%s_edge.txt' % (iters, iters), 'w') as f:
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
    df2.to_csv('sanguo_segments/seg%s/sanguo_seg%s_edge.csv' % (iters, iters), index=False)
    print('将进行第%s轮' % str(iters+1))
