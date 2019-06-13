#别名匹配
import pandas as pd
import numpy as np
from pandas import DataFrame as df



def combine_tag_name_alis(data1,data2):
    """
    :param data1: 别名集
    :param data2:标签集
    :return: 合并后的结果集
    """
    # 筛选数据，找到有别名的标签

    data2_list = data2['key'].tolist()
    data1_list = data1.values

    data2_list_tmp = []
    for i in data2_list:
        for j in data1_list:
            if i in j:
                i = i.replace(i, j[0])
        data2_list_tmp.append(i)
    return data2_list_tmp

# 以下是原代码
def combine_tag_name_alis_set(data1,data2):
    """
    :param data1: 别名集
    :param data2:标签集
    :return: 合并后的结果集
    """
    # 筛选数据，找到有别名的标签
    data3 = data1[data1['alias'].isin(data2['key'])]
    data4 = data2[~data2['key'].isin(data3['alias'])]
    #语义相似标签去重
    name1 = list(data3['name'])
    name2 = list(data4['key'])
    name3 = name1+name2
    name4 = list(set(name3))
    return name4

if __name__ == '__main__':

    #  读取别名数据集
    data1 = pd.read_excel('alias_test_database.xlsx')

    #  读取标签数据集
    data2 = pd.DataFrame({'key':['詹皇','小皇帝','小皇帝','内马尔','世界杯','姆巴佩','詹姆斯','姆巴佩','詹姆斯','里奥·梅西','梅西','Lionel Andrés Messi','小老虎','凯文-杜兰特','凯文·杜兰特','james','KK ']})

    #  合并之后的标签集
    name = combine_tag_name_alis(data1, data2)
    name1 = combine_tag_name_alis_set(data1, data2)
    print(name)
    print(name1)