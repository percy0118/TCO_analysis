import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
# Load the dataset
file_path = '/IC_cars.csv'
data = pd.read_csv(r'C:\Users\param\Downloads\VI th sem\EL\POME\ml_things\IC_cars.csv')
# Display the first few rows of the dataset to understand its structure
data.head()

# Select relevant columns and handle missing values
data = data.dropna(subset=['second_hand_price'])  # Dropping rows with missing second_hand_price
X = data[['showroom_price', 'no_of_years', 'No_of_kilometers']]
y = data['second_hand_price']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)
# Predict on the test set
y_pred = model.predict(X_test)
# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(mse, r2)


import joblib

# Save the model to a file
joblib_file = "linear_regression_model_ic.pkl"
joblib.dump(model, joblib_file)
