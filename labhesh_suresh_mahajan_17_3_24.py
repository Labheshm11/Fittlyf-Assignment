# -*- coding: utf-8 -*-
"""Labhesh Suresh Mahajan_17/3/24.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TE8JdhKddJACXQsSlFbb9Tguz6udEGWZ

# Checklist
"""

import pandas as pd

data = {'Section':['Section1', 'Q1', 'Q2', 'Q3',"Section2","Q1","Q2","Q3"],
        'Completion':["Completed","Completed","Completed","Completed","","Completed","Completed","Completed"],
        }

# Create DataFrame
df = pd.DataFrame(data)

# Print the output.
print(df)

from google.colab import files
uploaded=files.upload()

"""# Section 1

## solution for question 1
"""

funnel=pd.read_excel("WorkerFunnel.xlsx")
funnel

"""**After a thorough exploration about the dataset I got to know about the duplicate values present in the dataset,I identified that and took some proactive measures and steps to drop that duplicate values,as they were of no use.I kept the first occurence of the value and removed the 2nd respectively.This method surely helps to improve the efficiency**"""

funnel.drop_duplicates(inplace=True)

funnel
#the final dataframe(funnel) has been displayed without duplicate values values

"""**here i'm checking the null values present in the respective column**"""

funnel.isnull().sum()

funnel["Actual Productivity"].describe()

"""**I noticed there were 30 null values in the Actual Productivity column out of the 1161 entries which eventually sums to 2.58% of missing values..which isn't too much;to handle these NaN values I replaced them with mode..which seemed to be the most practical solution to me as it wont mess up the data**."""

funnel["Actual Productivity"].fillna(funnel["Actual Productivity"].mode()[0], inplace=True)

funnel.isnull().sum()
# the missing values are filled

funnel.shape

"""# solution for Q2"""

import numpy as np

"""here I have used the numpy library to compare the values of 2 columns and to get the result"""

funnel["Target Achieved"]=np.where(funnel["Actual Productivity"]>funnel["Targeted Productivity"],"Yes","No")

funnel

"""# Solution for Q2a"""

funnel["Target Achieved"].unique()

import matplotlib.pyplot as plt
import seaborn as sns

funnel["No. of Workers"].dtype

funnel["No. of Workers"].groupby(funnel["Quarter"]).sum()

"""
**The below graph represents the target achieved by workers over quarterly phases.The mean number of workers who were able to achieve the targets were slightly less than 38(estimation) but the one who were notb able to achive the target are nearly equal to 27.This graph helps us to understand that the no.of workers(who were able to achieve the target in quarterly phases)..this will surely help us to predict that what will be the best time (to hire workers) for the work to be completed with yes**"""

sns.barplot(data=funnel, x="Quarter", y="No. of Workers", hue="Target Achieved",estimator=np.mean,errorbar=("ci",0)).set(title="Workers achieved target over quaterly phase")

"""# Solution for Q2b"""

import statsmodels.api as sm

funnel

funnel['Date'] = pd.to_datetime(funnel['Date'])

funnel

funnel[["Actual Productivity"]].plot()

"""# Check for stationarity"""

from statsmodels.tsa.stattools import adfuller
def ad_test(funnel):
  dftest=adfuller(funnel,autolag="AIC")
  print("1. ADF ",dftest[0])
  print("2. P value ",dftest[1])
  print("3. Num of lags ",dftest[2])
  print("4. Num of observations used for ADF Regression and critical value calculation:  ",dftest[3])
  print("5. Critical Values: ")
  for key,val in dftest[4].items():
    print("\t",key,":",val)

ad_test(funnel["Actual Productivity"])

"""# The probability is less than 0.05 so we can conclude that the dataset is stationary"""


from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

stepwise_fit=auto_arima(funnel["Actual Productivity"],trace=True,supress_warnings=True)
stepwise_fit.summary()

"""split data into training and testing"""

print(funnel.shape)

train=funnel.iloc[:-30]
test=funnel.iloc[-30:]
print(train.shape,test.shape)



import statsmodels.tsa.arima.model as sm_arima
from statsmodels.tsa.arima_model import ARIMA
model = sm_arima.ARIMA(train["Actual Productivity"], order=(1, 0, 5))
model = model.fit()
model.summary()

start=len(train)
end=len(train)+len(test)-1
pred=model.predict(start=start,end=end,typ="levels")
print(pred)

pred.plot(legend=True)
test["Actual Productivity"].plot(legend=True)

funnel["Actual Productivity"].mean()

from sklearn.metrics import mean_squared_error
from math import sqrt
rmse=sqrt(mean_squared_error(pred,test["Actual Productivity"]))
print(rmse)


import statsmodels.tsa.arima.model as smt
model2 = smt.ARIMA(funnel["Actual Productivity"], order=(1, 0, 5))
model2 = model2.fit()
funnel.tail()

index_future_dates=pd.date_range(start="2015-11-03",end="2015-12-03")

pred=model2.predict(start=len(funnel),end=len(funnel)+30,typ="levels").rename("ARIMA Predictions")

pred.index = index_future_dates[:31]
print(pred)

pred.plot(figsize=(12,5),legend=True)

"""# Rolling Averages"""

sns.lineplot(data=funnel,x="Date",y="Actual Productivity")

funnel["Rolling_30"]=funnel["Actual Productivity"].rolling(window=30,min_periods=1).mean()
funnel["Rolling_50"]=funnel["Actual Productivity"].rolling(window=50,min_periods=1).mean()
funnel["Rolling_100"]=funnel["Actual Productivity"].rolling(window=100,min_periods=1).mean()
funnel["Rolling_120"]=funnel["Actual Productivity"].rolling(window=120,min_periods=1).mean()

funnel.plot.line(x="Date",y=["Rolling_30","Rolling_50","Rolling_100","Rolling_120"],legend="auto")

"""# Q2c"""

funnel.columns

X=funnel.iloc[:,0:1]
y=funnel.iloc[:,-1]

y

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=2)

from sklearn.linear_model import LinearRegression

lr=LinearRegression()

lr.fit(X_train,y_train)

# Convert the 'Date' column to a string for compatibility with LinearRegression
funnel['Date'] = funnel['Date'].astype(str)

X_train, X_test, y_train, y_test = train_test_split(funnel["Targeted Productivity"], funnel["Actual Productivity"], test_size=0.2, random_state=2)

lr = LinearRegression()
lr.fit(X_train.values.reshape(-1, 1), y_train)

plt.scatter(funnel["Targeted Productivity"], funnel["Actual Productivity"])
plt.plot(X_train, lr.predict(X_train.values.reshape(-1, 1)), color="red")
plt.show()

from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_percentage_error,mean_absolute_error

# Reshape X_test to a 2D array using numpy
X_test = np.array(X_test).reshape(-1, 1)

# Predict using the reshaped X_test
y_pred = lr.predict(X_test)

y_pred

y_test.values

"""# MAE"""

print("MAE",mean_absolute_error(y_test,y_pred))

"""# MSE"""

print("MSE",mean_squared_error(y_test,y_pred))

"""# MAPE"""

print("MAPE",mean_absolute_percentage_error(y_test,y_pred))

"""# RMSE"""

print("RMSE",np.sqrt(mean_squared_error(y_test,y_pred)))

"""# R2 Score"""

print("RMSE",r2_score(y_test,y_pred))

"""# Section 2

# Q1
"""

uploaded1=files.upload()

abtest=pd.read_excel("ABTest.xlsx")
abtest

abtest.isnull().sum()

abtest.columns

abtest.isnull().sum()
abtest.columns

abtest["Device"].value_counts()

abtest["Device"].unique()

abtest["Date"].unique()

clicks_by_device = abtest.groupby("Device")[["Clicks"]].sum()
print(clicks_by_device)

# Group the data by Date and Device
grouped_data = abtest.groupby(["Date", "Device"])["Clicks"].sum().reset_index()

# Create a pivot table with clicks as values and devices as columns
clicks_by_date_device = grouped_data.pivot(index="Date", columns="Device", values="Clicks")

# Print the clicks_by_date_device DataFrame
print(clicks_by_date_device)

import matplotlib.pyplot as plt

# Plot the total clicks for each device over time
clicks_by_date_device.plot(kind="line", figsize=(10, 6))

# Add a title and labels
plt.title("Total Clicks by Device and Date")
plt.xlabel("Date")
plt.ylabel("Clicks")

# Show the plot
plt.show()

abtest.columns

import scipy.stats as stats

# Function to calculate click-through rate (CTR)
def calculate_ctr(clicks, visitors):
    return clicks / visitors

# Function to perform hypothesis test
def perform_hypothesis_test(control_clicks, control_visitors, exp_clicks, exp_visitors):
    # Calculate CTR for control and experimental groups
    control_ctr = calculate_ctr(control_clicks, control_visitors)
    exp_ctr = calculate_ctr(exp_clicks, exp_visitors)

    # Perform hypothesis test (two-sample t-test assuming equal variances)
    t_stat, p_value = stats.ttest_ind_from_stats(control_ctr, np.sqrt(control_ctr*(1-control_ctr)), control_visitors,
                                                 exp_ctr, np.sqrt(exp_ctr*(1-exp_ctr)), exp_visitors,
                                                 equal_var=True)

    return t_stat, p_value

# Function to calculate required sample size
def calculate_sample_size(MDE, alpha, power, control_ctr, exp_ctr):
    pooled_var = (control_ctr * (1 - control_ctr) + exp_ctr * (1 - exp_ctr)) / 2
    Z_alpha_2 = stats.norm.ppf(1 - alpha/2)
    Z_beta = stats.norm.ppf(power)
    sample_size = (2 * pooled_var * (Z_alpha_2 + Z_beta)**2) / MDE**2
    return sample_size



control_clicks = 100
control_visitors = 1000
exp_clicks = 120
exp_visitors = 1000
MDE = 0.05
alpha = 0.05
power = 0.80

# hypothesis test
t_stat, p_value = perform_hypothesis_test(control_clicks, control_visitors, exp_clicks, exp_visitors)

# Calculate required sample size
control_ctr = calculate_ctr(control_clicks, control_visitors)
exp_ctr = calculate_ctr(exp_clicks, exp_visitors)
required_sample_size = calculate_sample_size(MDE, alpha, power, control_ctr, exp_ctr)

# Check if actual sample size is sufficient
actual_sample_size = control_visitors + exp_visitors
is_sufficient_sample = "Yes" if actual_sample_size >= required_sample_size else "No"

# Output results
print("Hypothesis Test Results:")
print("T-statistic:", t_stat)
print("P-value:", p_value)
print("\nRequired Sample Size:", required_sample_size)
print("Actual Sample Size:", actual_sample_size)
print("Sufficient Sample Size to conclude the test?", is_sufficient_sample)

"""# Q3"""

import scipy.stats as stats

def test_hypothesis(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
  """
  This function is designed to assess whether the treatment group's conversion rate is higher than that of the control group.
   It takes inputs such as the number of visitors and conversions for both groups, along with a desired confidence level for the statistical test.

It then compares the conversion rates of both groups and determines which one is better based on the specified confidence level.
If the treatment group's conversion rate is statistically significantly higher, it returns "Experiment Group is Better."
 If the control group's conversion rate is significantly higher, it returns "Control Group is Better."
  If there's not enough evidence to determine a significant difference, it returns "Indeterminate."
  """

  # Calculate the conversion rates for each group.
  control_rate = control_conversions / control_visitors
  treatment_rate = treatment_conversions / treatment_visitors

  # Calculate the z-score for the difference in conversion rates.
  z_score = (treatment_rate - control_rate) / (
      (control_rate * (1 - control_rate) / control_visitors + treatment_rate * (1 - treatment_rate) / treatment_visitors)**0.5)

  # Determine the critical value based on the desired confidence level.
  if confidence_level == 90:
    critical_value = 1.645
  elif confidence_level == 95:
    critical_value = 1.96
  elif confidence_level == 99:
    critical_value = 2.576
  else:
    raise ValueError("Invalid confidence level.")

  # Compare the z-score to the critical value.
  if z_score > critical_value:
    return "Experiment Group is Better"
  elif z_score < -critical_value:
    return "Control Group is Better"
  else:
    return "Indeterminate"

result = test_hypothesis(1000, 50, 1000, 70, 95)
print(result)

"""# Q4"""

!pip install streamlit
import streamlit as st

import streamlit as st

def perform_hypothesis_test(sample_size, mean, standard_deviation, alpha):
  """
This function conducts a hypothesis test and calculates the p-value based on the provided sample size,
sample mean, sample standard deviation, and significance level (alpha).
The p-value indicates the probability of observing the data or more extreme results under the assumption that the null hypothesis is true.
 The lower the p-value, the stronger the evidence against the null hypothesis.
  """
  from scipy.stats import ztest
  return ztest(sample_size, mean, standard_deviation, value=0, alternative="two-sided")[1]

st.title("Hypothesis Test App")

# Get user input
sample_size = st.number_input("Enter the sample size:")
mean = st.number_input("Enter the sample mean:")
standard_deviation = st.number_input("Enter the sample standard deviation:")
alpha = st.number_input("Enter the significance level (alpha):")

# Perform the hypothesis test and display the result
if st.button("Perform Hypothesis Test"):
  p_value = perform_hypothesis_test(sample_size, mean, standard_deviation, alpha)
  st.write("The p-value is:", p_value)
  if p_value < alpha:
    st.write("Reject the null hypothesis.")
  else:
    st.write("Fail to reject the null hypothesis.")

