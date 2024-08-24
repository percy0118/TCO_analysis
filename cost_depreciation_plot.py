import pandas as pd
import matplotlib.pyplot as plt

# Load the first dataset (Internal Combustion Cars)
file_path_1 = r'C:\Users\param\Downloads\VI th sem\EL\POME\IC_cars.csv'  # Replace with your first file path
data_1 = pd.read_csv(file_path_1)

# Load the second dataset (Electric Vehicles)
file_path_2 = r'C:\Users\param\Downloads\VI th sem\EL\POME\EV_cars.csv'  # Replace with your second file path
data_2 = pd.read_csv(file_path_2)

# Define the specific mileage values
mileage_values = 80000

# Define the specific car names
car_names = ['Tiago', 'Tigor', 'Nexon', 'C3', 'XUV 3XO', 'Astor']  # Replace with the car names you are interested in

# Filter the data for the specific car and mileage values
data_1_filtered = data_1[(data_1['No_of_kilometers'] == mileage_values) & (data_1['car-name'].isin(car_names))]
data_2_filtered = data_2[(data_2['No_of_kilometers'] == mileage_values) & (data_2['car-name'].isin(car_names))]

# Calculate average second-hand price ratios (second_hand_price/showroom_price) grouped by number of years used
avg_ic_prices = data_1_filtered.groupby('no_of_years').apply(
    lambda x: (x['second_hand_price'] / x['showroom_price']).mean())
avg_ev_prices = data_2_filtered.groupby('no_of_years').apply(
    lambda x: (x['second_hand_price'] / x['showroom_price']).mean())

# Plot the average second-hand price ratios
plt.figure(figsize=(10, 5))
plt.plot(avg_ic_prices.index, avg_ic_prices.values, label=f'IC Cars-{mileage_values} km', color='green')
plt.plot(avg_ev_prices.index, avg_ev_prices.values, label=f'EV Cars-{mileage_values} km', color='red')

# Customize the plot
plt.xlabel('Number of Years Used')
plt.ylabel('Average Second-hand Price Ratio')
plt.title('Average Price vs Number of Years Used for Selected Cars')
plt.legend()
plt.grid(True)
plt.show()
