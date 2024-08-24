import tkinter as tk
from tkinter import ttk
import joblib

# Load the model from the file
modelev = joblib.load("linear_regression_model_ev.pkl")
modelic=joblib.load("linear_regression_model_ic.pkl")


def calculate_tco_ev(car_price, tax, insurance, electricity_price, daily_distance, years,vehicle_category):
    yearly_distance = daily_distance * 365
    charging_cost = yearly_distance * electricity_price  # Assuming cost per km
    service_charge_per_km = 1.5
    maintenance_cost = yearly_distance * service_charge_per_km * years

    if vehicle_category=="Two-wheeler":
        selling_cost=car_price*0.75
    else:
        a = [[car_price, years, years * yearly_distance]]
        selling_cost = modelev.predict(a)
        selling_cost = selling_cost[0]
    total_cost = car_price + tax + insurance*years + (charging_cost * years) + maintenance_cost - selling_cost
    return total_cost, charging_cost * years, maintenance_cost, selling_cost


def calculate_tco_ice(car_price, tax, insurance, fuel_price, daily_distance, years,vehicle_category):
    yearly_distance = daily_distance * 365
    fuel_cost = yearly_distance * fuel_price  # Assuming cost per km
    service_charge_per_km = 2
    maintenance_cost = yearly_distance * service_charge_per_km * years


    if vehicle_category=="Two-wheeler":
        selling_cost=car_price*0.9
    else:
        a = [[car_price, years, years * yearly_distance]]
        selling_cost = modelic.predict(a)
        selling_cost = selling_cost[0]

    #selling_cost = selling_cost[0]
    #print(selling_cost)
    total_cost = car_price + tax + insurance*years + (fuel_cost * years) + maintenance_cost - selling_cost
    return total_cost, fuel_cost * years, maintenance_cost, selling_cost


def calculate_tax(vehicle_type, vehicle_category, car_price):
    tax = 0

    if vehicle_type == "EV":
        tax = 0.10 * car_price
    elif vehicle_type == "ICE":
        if vehicle_category == "Two-wheeler":
            if car_price <= 50000:
                tax = 0.10 * car_price
            elif 50000 < car_price <= 100000:
                tax = 0.12 * car_price
            else:
                tax = 0.18 * car_price
        elif vehicle_category == "Four-wheeler":
            if car_price <= 500000:
                tax = 0.13 * car_price
            elif 500000 < car_price <= 1000000:
                tax = 0.14 * car_price
            elif 1000000 < car_price <= 2000000:
                tax = 0.17 * car_price
            else:
                tax = 0.18 * car_price

    return tax


def calculate_tco():
    car_price = float(entry_car_price.get())
    years = int(entry_years.get())
    daily_distance = float(entry_daily_distance.get())
    fuel_price = float(entry_fuel_price.get())
    vehicle_type = var_vehicle_type.get()
    vehicle_category = var_vehicle_category.get()

    tax = calculate_tax(vehicle_type, vehicle_category, car_price)

    if vehicle_type == "EV":
        insurance = 3000 if vehicle_category == "Two-wheeler" else 6000
        total_cost, charging_cost, maintenance_cost, selling_cost = calculate_tco_ev(car_price, tax, insurance,
                                                                                     fuel_price, daily_distance, years,vehicle_category)
        fuel_cost = charging_cost
    else:
        insurance = 5000 if vehicle_category == "Two-wheeler" else 10000
        total_cost, fuel_cost, maintenance_cost, selling_cost = calculate_tco_ice(car_price, tax, insurance, fuel_price,
                                                                                  daily_distance, years,vehicle_category)
        charging_cost = 0

    # Update the GUI with detailed results
    label_result.config(text=f"Total Cost of Ownership: ₹{total_cost:.2f}")
    label_fuel_cost.config(text=f"Fuel/Electricity Cost: ₹{fuel_cost:.2f}")
    label_insurance.config(text=f"Insurance Cost: ₹{insurance*years:.2f}")
    label_maintenance.config(text=f"Maintenance Cost: ₹{maintenance_cost:.2f}")
    #label_selling_cost.config(text=f"Reselling Value: ₹{selling_cost:.2f}")


# Create the main window
root = tk.Tk()
root.title("TCO Calculator")

# Vehicle type
var_vehicle_type = tk.StringVar(value="EV")
ttk.Label(root, text="Vehicle Type:").grid(column=0, row=0)
ttk.Radiobutton(root, text="Electric Vehicle", variable=var_vehicle_type, value="EV").grid(column=1, row=0)
ttk.Radiobutton(root, text="ICE Vehicle", variable=var_vehicle_type, value="ICE").grid(column=2, row=0)

# Vehicle category (Two-wheeler or Four-wheeler)
var_vehicle_category = tk.StringVar(value="Four-wheeler")
ttk.Label(root, text="Vehicle Category:").grid(column=0, row=1)
ttk.Radiobutton(root, text="Two-wheeler", variable=var_vehicle_category, value="Two-wheeler").grid(column=1, row=1)
ttk.Radiobutton(root, text="Four-wheeler", variable=var_vehicle_category, value="Four-wheeler").grid(column=2, row=1)

# Car price
ttk.Label(root, text="Vehicle Cost (₹):").grid(column=0, row=2)
entry_car_price = ttk.Entry(root)
entry_car_price.grid(column=1, row=2)

# Fuel/Electricity price per km
ttk.Label(root, text="Fuel/Electricity Price (₹/km):").grid(column=0, row=3)
entry_fuel_price = ttk.Entry(root)
entry_fuel_price.grid(column=1, row=3)

# Number of years to own
ttk.Label(root, text="Years to Own:").grid(column=0, row=4)
entry_years = ttk.Entry(root)
entry_years.grid(column=1, row=4)

# Daily distance
ttk.Label(root, text="Daily Distance (km):").grid(column=0, row=5)
entry_daily_distance = ttk.Entry(root)
entry_daily_distance.grid(column=1, row=5)

# Calculate button
calculate_button = ttk.Button(root, text="Calculate TCO", command=calculate_tco)
calculate_button.grid(column=1, row=6)

# Result labels
label_result = ttk.Label(root, text="")
label_result.grid(column=1, row=7)

label_fuel_cost = ttk.Label(root, text="")
label_fuel_cost.grid(column=1, row=8)

label_insurance = ttk.Label(root, text="")
label_insurance.grid(column=1, row=9)

label_maintenance = ttk.Label(root, text="")
label_maintenance.grid(column=1, row=10)

label_selling_cost = ttk.Label(root, text="")
label_selling_cost.grid(column=1, row=11)

root.mainloop()
