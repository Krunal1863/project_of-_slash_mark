import pandas as pd
import numpy as np
import pickle
# visulization 
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

raw_data = pd.read_csv(r'D:\Github_slash_mark_project\slash_mark_project\minor-4\dataset\transfusion.data')

X = raw_data.drop('whether he/she donated blood in March 2007',axis=1)

y = raw_data['whether he/she donated blood in March 2007']

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=54,test_size=0.25)

X_train.shape,X_test.shape,y_train.shape,y_test.shape

from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train,y_train)

pred = lr.predict(X_test)

from sklearn.metrics import accuracy_score

accuracy_score(y_test,pred)


pickle.dump(lr, open('blood_forcast_lr_model.pkl', 'wb'))