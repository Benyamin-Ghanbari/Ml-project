#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#drop Nan and unreal Area 
df = pd.read_csv('home.csv')
df = df.dropna(subset=['Address'])
df = df.drop([df.index[709], df.index[530], df.index[2802]])
df.Area = pd.to_numeric(df['Area'], errors = 'coerce')
df = df.dropna(subset = ['Area'])
#df.head()


# In[3]:


#plotting data , its seems its exponantial
sns.catplot(data=df, x="Area", y="Price", hue = 'Address')


# In[4]:


#encoding
encode= pd.get_dummies(df.Address)
df_x = df[['Area']]
df_y = df[['Price']]
df1= pd.concat([df_x, encode], axis = 1)


# In[5]:


#Create train and test
msk = np.random.rand(len(df))<0.8
train_x = df_x[msk]
train_y = df_y[msk]
test_x = df_x[~msk]
test_y = df_y[~msk]


# In[6]:


# using polynomial for modelling our data 
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
x = np.asanyarray(train_x)
y = np.asanyarray(train_y)
poly = PolynomialFeatures(degree=2)
train_x_poly = poly.fit_transform(x) 
clf = linear_model.LinearRegression()
train_y_ = clf.fit(train_x_poly, y)
                        


# In[7]:


from sklearn.metrics import r2_score
x = np.asanyarray(test_x)
y = np.asanyarray(test_y)
test_x_poly = poly.fit_transform(x)
test_y_ = clf.predict(test_x_poly)
print("R2-score: %.2f" % r2_score(y,test_y_ ) )


# In[ ]:




