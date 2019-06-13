import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from scipy.stats import norm
from collections import Counter
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import powerlaw


csv_data = pd.read_csv('/Users/zhangchenhan/Desktop/sanguo_network/sanguozhiiiiiiiiiiiiiiiiiiiiiiiiiiiiii/sanguozhi_topo_features.csv')
data = list(csv_data.Degree)
data = dict(Counter(data))
X = list(data.keys())
Y = list(data.values())
# X = np.array(X)
# Y = np.array(Y)

df = pd.DataFrame({'X':X, 'Y':Y})
df.to_csv('sanguozhi_powerlaw.csv')



# regr = linear_model.LinearRegression()
# regr.fit(X,Y) #拟合
#
# print('Coefficients: \n', regr.coef_,)
# print("Intercept:\n",regr.intercept_)
# print("Residual sum of squares: %.8f" % np.mean((regr.predict(X) - Y) ** 2)) #残差平方和

results = powerlaw.fit(X)
print(results)
#可视化
# plt.title('power_law')
# plt.scatter(X, Y, color='black')
# plt.plot(X, regr.predict(X), color='blue',linewidth=3)
# plt.show()