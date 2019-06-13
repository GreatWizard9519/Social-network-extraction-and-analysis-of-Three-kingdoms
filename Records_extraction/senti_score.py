
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import sentiwordnet as swn
from sentiment_extraction import cao_tag, liu_tag



#曹操情感得分

# cao_wordlist = cao_tag
# total_score = 0.0
# netScore = 0.0
# count = 0
# for word in cao_wordlist:
#     if word[1] == 'JJ':
#         try:
#             wordSet = swn.senti_synsets(word[0])
#
#             # filter non-matching value
#             wordSet = [testWord for testWord in wordSet]
#
#             posScore = np.nanmean([word.pos_score() for word in wordSet])
#             negScore = np.nanmean([word.neg_score() for word in wordSet])
#             netScore = posScore - negScore
#             if np.isnan(netScore):
#                 continue
#             else:
#                 count += 1
#                 total_score += netScore
#         except IndexError:
#             continue
#         else:
#             continue
#
# aver_score = total_score/count
# aver_score = float(aver_score)
# print(aver_score)


# 刘备情感得分

liu_wordlist = liu_tag
total_score = 0.0
netScore = 0.0
count = 0
for word in liu_wordlist:
    if word[1] == 'JJ':
        try:
            wordSet = swn.senti_synsets(word[0])

            # filter non-matching value
            wordSet = [testWord for testWord in wordSet]
            print(wordSet)
            posScore = np.nanmean([word.pos_score() for word in wordSet])
            negScore = np.nanmean([word.neg_score() for word in wordSet])
            netScore = posScore - negScore
            if np.isnan(netScore):
                continue
            else:
                count += 1
                total_score += netScore
        except IndexError:
            continue
        else:
            continue

aver_score = total_score / count
aver_score = float(aver_score)
print(aver_score)


