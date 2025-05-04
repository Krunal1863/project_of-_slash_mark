import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

data = pd.read_csv('D:\Github_slash_mark_project\slash_mark_project\Deploy\minor-2\data\kc_house_data.csv')



x = data.drop(columns = {'id','price','date','condition',
'waterfront',
'view',
'grade',
'sqft_basement',
'yr_renovated',
'lat',
'long',
'zipcode',
'sqft_living15',
'sqft_lot15',
'sqft_above'})


y = data['price']


x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=2)

# standardize the data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)


from sklearn import ensemble
clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2,
          learning_rate = 0.1)
clf.fit(x_train, y_train)
clf.score(x_test,y_test)

model = XGBRegressor()

model.fit(x_train,y_train)

train_data_prediction = model.predict(x_train)
score_1 = metrics.r2_score(y_train,train_data_prediction)
# score_2 = metrics.mean_absolute_error(y_train,train_data_prediction)

test_data_prediction = model.predict(x_test)
score_2 = metrics.r2_score(y_test,test_data_prediction)
# score_2 = metrics.mean_absolute_error(y_train,train_data_prediction)

pickle.dump(model, open('house_xgboost_model.pkl', 'wb'))