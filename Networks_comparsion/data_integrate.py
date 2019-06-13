import pandas as pd

#将两部书相交人物提取出来

sanguo_combine_all = []
for iters in range(1,6):
    print('第%s个时期' % iters)
    #sanguo
    sanguo_pd = pd.read_csv('segments/seg%s/sanguo_seg%s_node.csv' % (iters, iters))
    sanguo_list = list(sanguo_pd['Id'])
    sanguo_list = list(set(sanguo_list))
    print(sanguo_list)
    print(len(sanguo_list))

    #sanguozhi
    sanguozhi_pd = pd.read_csv('segments/seg%s/sanguozhi_seg%s_node.csv' % (iters, iters))
    sanguozhi_list = list(sanguozhi_pd['Id'])
    sanguozhi_list = list(set(sanguozhi_list))
    print(sanguozhi_list)
    print(len(sanguozhi_list))

    sanguo_combine = []
    for i in sanguo_list:
        if i in sanguozhi_list:
            sanguo_combine.append(i)
    print(sanguo_combine)
    print(len(sanguo_combine))
    sanguo_combine_all.append(sanguo_combine)

