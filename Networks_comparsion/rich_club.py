#从pandas 建立图

import networkx as nx
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

edges = pd.read_csv('/Users/zhangchenhan/PycharmProjects/sanguozhi/sanguozhi_segments/seg5/sanguozhi_seg5_edge.csv')

edges = edges.drop(columns=['weight'])
edges = np.array(edges)
edges = edges.tolist()
print(edges)

G = nx.Graph(edges)

print(len(G.nodes))

rc = nx.rich_club_coefficient(G,normalized=False)
print(rc)
rc = pd.DataFrame({'k':list(rc.keys()), 'p':list(rc.values())})
rc.to_csv('sanguozhi_richclub.csv')
# print(type(G))