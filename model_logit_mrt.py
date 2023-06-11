# Logistic Regression
# https://medium.com/jameslearningnote/%E8%B3%87%E6%96%99%E5%88%86%E6%9E%90-%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E7%AC%AC3-3%E8%AC%9B-%E7%B7%9A%E6%80%A7%E5%88%86%E9%A1%9E-%E9%82%8F%E8%BC%AF%E6%96%AF%E5%9B%9E%E6%AD%B8-logistic-regression-%E4%BB%8B%E7%B4%B9-a1a5f47017e5

#In[1]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
# 經過研究，sklearn 的 x 跟 y 都是 <class 'pandas.core.frame.DataFrame'>
# 我們既有的 dataframe 已經有 feature_names 所以不用再新增，主要是要切割一下 feature 跟 target


#In[2]
df_x = pd.read_csv("finalprocess_x.csv")
df_y = pd.read_csv("finalprocess_y.csv")

X = df_x
y_mrt = pd.DataFrame(df_y.pop("mrt"))
'''
y_bus = pd.DataFrame(df_y.pop("bus"))
y_car = pd.DataFrame(df_y.pop("car"))
y_motorpri = pd.DataFrame(df_y.pop("motorpri"))
y_motorsha = pd.DataFrame(df_y.pop("motorsha"))
y_bikepri = pd.DataFrame(df_y.pop("bikepri"))
y_bikesha = pd.DataFrame(df_y.pop("bikesha"))
y_walk = pd.DataFrame(df_y.pop("walk"))
y_shuttle = pd.DataFrame(df_y.pop("shuttle"))
'''

# Remove the variables that are not significant (|z| <1.329)
# X = X.drop("", axis=1)
X = X.drop("live_dorm", axis=1)
X = X.drop("live_rent", axis=1)

X = X.drop("own_1280", axis=1)
X = X.drop("own_license", axis=1)
X = X.drop("own_plan_bike", axis=1)
X = X.drop("own_plan_motor", axis=1)

X = X.drop("rent_month", axis=1)
X = X.drop("rent_experience", axis=1)

X = X.drop("dorm_if_out", axis=1)
X = X.drop("home_if_rent", axis=1)
X = X.drop("if_lottery", axis=1)
X = X.drop("consider_cost", axis=1)
X = X.drop("consider_envi", axis=1)
X = X.drop("consider_heal", axis=1)
X = X.drop("consider_conv", axis=1)
X = X.drop("consider_time", axis=1)
X = X.drop("consider_flex", axis=1)
X = X.drop("consider_safe", axis=1)

X = X.drop("prefer_time", axis=1)
X = X.drop("prefer_dist", axis=1)
X = X.drop("prefer_cost", axis=1)



X = X.drop("gender", axis=1)
X = X.drop("income", axis=1)
X = X.drop("familyeco", axis=1)
X = X.drop("job", axis=1)
X = X.drop("pets", axis=1)



print(X.columns)

#In[3]
X_train, X_test, y_train, y_test = train_test_split(X, y_mrt, test_size=0.2, random_state=0)
'''
print(X_train)
print(y_train)
print(X_test)
print(y_test)
print(len(X_train), len(y_train), len(X_test), len(y_test))
'''


#In[4] Skip This
'''
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train, y_train.values.ravel())
'''


#In[5] Run "statsmodels" in python 3.8 3.9 3.10
# https://www.statsmodels.org/stable/install.html
# https://data.library.virginia.edu/logistic-regression-four-ways-with-python/

import statsmodels.formula.api as smf

# Create the formula string 
all_columns = ' + '.join(X.columns[:])
formula = "mrt ~ " + all_columns 
print("Formula: ", formula, "\n")

# Put the training predictors and responses into one DataFrame to be input into the model
trainingdata = pd.concat([X_train,y_train], axis = 1)

# Build the model
log_reg_1 = smf.logit(formula, data=trainingdata).fit()
print(log_reg_1.summary())




# All classes getting classified as 0: This could be potentially because of the data.
# The dataset has all datapoints of class 1 being simultaeously classified as class 0.
# %%
