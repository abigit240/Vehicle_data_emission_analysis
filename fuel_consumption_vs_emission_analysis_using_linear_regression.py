# -*- coding: utf-8 -*-
"""Fuel consumption vs emission analysis using linear regression

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wYpvLnMPYEIm4qUkWCHtpKy5hqnx3UO_
"""

# Commented out IPython magic to ensure Python compatibility.
# @title 1. Importing libraries
import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
# %matplotlib inline

# @title 2. Get the dataset
path= "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillsNetwork/labs/Module%202/data/FuelConsumptionCo2.csv"

import requests

def download(url, filename):
    """Downloads a file from a URL and saves it to a local file.

    Args:
        url (str): The URL of the file to download.
        filename (str): The name of the local file to save the downloaded file to.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)

# Download the file
download(path, "FuelConsumption.csv")
path = "FuelConsumption.csv"

# @title 3. Explore dataset
df = pd.read_csv("FuelConsumption.csv")

# take a look at the dataset
df.head()

# summarize the data
df.describe()

cdf = df[['ENGINESIZE','CYLINDERS','FUELCONSUMPTION_COMB','CO2EMISSIONS']]
cdf.head(9)

# @title FUELCONSUMPTION_COMB vs CO2EMISSIONS


cdf.plot(kind='scatter', x='FUELCONSUMPTION_COMB', y='CO2EMISSIONS', s=32, alpha=.8)
plt.gca().spines[['top', 'right',]].set_visible(False)

viz = cdf[['CYLINDERS','ENGINESIZE','CO2EMISSIONS','FUELCONSUMPTION_COMB']]
viz.hist()
plt.show()

plt.scatter(cdf.FUELCONSUMPTION_COMB, cdf.CO2EMISSIONS,  color='blue')
plt.xlabel("FUELCONSUMPTION_COMB")
plt.ylabel("Emission")
plt.show()

cdf.plot.scatter(x='FUELCONSUMPTION_COMB', y='CO2EMISSIONS', color='blue')

plt.scatter(cdf.ENGINESIZE, cdf.CO2EMISSIONS,  color='blue')
plt.xlabel("Engine size")
plt.ylabel("Emission")
plt.show()

cdf.plot.scatter(x='CYLINDERS',y='CO2EMISSIONS',color='green')

# @title 4. Train-test split to apply linear regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Independent and dependent variables
X = cdf[['ENGINESIZE','CYLINDERS','FUELCONSUMPTION_COMB']]
y = cdf['CO2EMISSIONS']

# Feature scaling
#from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#X_scaled = scaler.fit_transform(X)

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression model
#model = LinearRegression()
#model.fit(X_train, y_train)

# Predict on test data
#y_pred = model.predict(X_test)

# Evaluate the model
#mse = mean_squared_error(y_test, y_pred)
#r2 = r2_score(y_test, y_pred)
#print(f"Mean Squared Error (MSE): {mse}")
#print(f"R-squared (R2): {r2}")

#msk = np.random.rand(len(df)) < 0.8
#train = cdf[msk]
#test = cdf[~msk]

# @title Fit model
from sklearn import linear_model
regr = linear_model.LinearRegression()
train_x = np.asanyarray(X_train[['ENGINESIZE']])
train_y = np.asanyarray(y_train)
regr.fit(train_x, train_y)
# The coefficients
print ('Coefficients: ', regr.coef_)
print ('Intercept: ',regr.intercept_)

plt.scatter(X_train.ENGINESIZE, y_train,  color='blue')
plt.plot(train_x, regr.coef_[0]*train_x + regr.intercept_, '-r') # Changed this line
plt.xlabel("Engine size")
plt.ylabel("Emission")

# @title Evaluation
from sklearn.metrics import r2_score

test_x = np.asanyarray(X_test[['ENGINESIZE']])
test_y = np.asanyarray(y_test)
test_y_ = regr.predict(test_x)

print("Mean absolute error: %.2f" % np.mean(np.absolute(test_y_ - test_y)))
print("Residual sum of squares (MSE): %.2f" % np.mean((test_y_ - test_y) ** 2))
print("R2-score: %.2f" % r2_score(test_y , test_y_) )

# @title Try using Fuel consumption combined
train_x = np.asanyarray(X_train[['FUELCONSUMPTION_COMB']])

test_x = np.asanyarray(X_test[['FUELCONSUMPTION_COMB']])

regr = linear_model.LinearRegression()
train_x = np.asanyarray(X_train[['FUELCONSUMPTION_COMB']])
train_y = np.asanyarray(y_train) #y_train has 1 column only so no need to mention
regr.fit(train_x, train_y)
#ADD CODE
print ('Coefficients: ', regr.coef_)
print ('Intercept: ',regr.intercept_)

#test_x = np.asanyarray(test[['FUELCONSUMPTION_COMB']])
predictions = regr.predict(test_x)

test_y_=predictions
print("Mean absolute error: %.2f" % np.mean(np.absolute(test_y_- test_y)))
print("Residual sum of squares (MSE): %.2f" % np.mean((test_y_ - test_y) ** 2))
print("R2-score: %.2f" % r2_score(test_y , test_y_) )

plt.scatter(X_train.FUELCONSUMPTION_COMB, y_train,  color='blue')
plt.plot(train_x, regr.coef_[0]*train_x + regr.intercept_, '-r') # Changed this line
plt.xlabel("FUELCONSUMPTION_COMB")
plt.ylabel("Emission")