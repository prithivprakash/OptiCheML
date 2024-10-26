import streamlit as st
import numpy as np
import joblib

# Load the trained models
fault_model = joblib.load('svc1.joblib')
conversion_model = joblib.load('svr1.joblib')

# Load the StandardScaler used during training
scaler = joblib.load("scaler1.joblib")

# Suggest parameter adjustments if a fault is detected
def suggest_parameter_adjustment(temperature, pressure, h2_n2_ratio, catalyst_age, space_velocity):
    adjustments = []
    
    if temperature > 530 or temperature < 400:
        adjustments.append("Adjust the temperature in the range between 400°C to 530°C")
    if pressure < 160 or pressure > 300:
        adjustments.append("Adjust the pressure in the range between 160 atm and 300 atm")
    if h2_n2_ratio < 2.6 or h2_n2_ratio > 3.4:
        adjustments.append("Adjust H2/N2 ratio to be between 2.6 and 3.4")
    if catalyst_age > 900:
        adjustments.append("Replace or regenerate the catalyst (age > 900 hours)")
    
    return adjustments if adjustments else ["No specific adjustments needed"]

# Predict byproducts based on reaction parameters and conversion rate
def predict_byproducts(temperature, pressure, h2_n2_ratio, catalyst_age, space_velocity):
    WATER_COEFFICIENT = 0.02  # Example coefficient for water byproduct
    UNREACTED_N2_H2_COEFFICIENT = 0.1  # Example coefficient for unreacted gases
    METHANE_COEFFICIENT = 0.005  # Example coefficient for methane
    CO2_COEFFICIENT = 0.01  # Example coefficient for CO2
    HEAT_RELEASE_COEFFICIENT = 500  # Example heat release per unit ammonia production (kJ)

    base_conversion = (temperature - 400) / 150 * 0.4 + (pressure - 150) / 150 * 0.6
    conversion = np.clip(base_conversion, 0, 1)

    conversion *= (1 + (h2_n2_ratio - 3) * 0.1)  # Effect of H2/N2 ratio on conversion
    conversion *= (1 - catalyst_age / 2000)  # Effect of catalyst age
    conversion *= (1 + (space_velocity - 20000) / 20000 * 0.1)  # Effect of space velocity

    ammonia_production = conversion * space_velocity / 10000  # Ammonia production based on input

    water_byproduct = ammonia_production * WATER_COEFFICIENT  
    unreacted_n2_h2 = ammonia_production * UNREACTED_N2_H2_COEFFICIENT  
    methane_byproduct = ammonia_production * METHANE_COEFFICIENT  
    co2_byproduct = ammonia_production * CO2_COEFFICIENT  
    heat_release = ammonia_production * HEAT_RELEASE_COEFFICIENT  

    byproducts = {
        'Ammonia Production (kg)': ammonia_production,
        'Water (H₂O) Byproduct (kg)': water_byproduct,
        'Unreacted N₂ & H₂ (kg)': unreacted_n2_h2,
        'Methane (CH₄) Byproduct (kg)': methane_byproduct,
        'CO₂ Byproduct (kg)': co2_byproduct,
        'Heat Released (kJ)': heat_release
    }

    return byproducts

# Calculate electric energy from the byproducts
def calculate_electric_energy(byproducts):
    # Conversion efficiencies
    THERMOELECTRIC_EFFICIENCY = 0.10  # 10% efficiency for thermoelectric systems
    METHANE_ENERGY_CONTENT = 50 * 1e6  # 50 MJ/kg
    METHANE_EFFICIENCY = 0.40  # 40% efficiency for methane to electricity
    H2_ENERGY_CONTENT = 120 * 1e6  # 120 MJ/kg
    H2_EFFICIENCY = 0.50  # 50% efficiency for H2 to electricity

    # Convert the byproducts into usable energy (in kWh)
    heat_energy_kWh = byproducts['Heat Released (kJ)'] * 1e-3 * THERMOELECTRIC_EFFICIENCY / 3600
    methane_energy_kWh = byproducts['Methane (CH₄) Byproduct (kg)'] * METHANE_ENERGY_CONTENT * METHANE_EFFICIENCY / 3600 / 1e3
    unreacted_n2_h2_energy_kWh = byproducts['Unreacted N₂ & H₂ (kg)'] * H2_ENERGY_CONTENT * H2_EFFICIENCY / 3600 / 1e3

    total_energy_kWh = heat_energy_kWh + methane_energy_kWh + unreacted_n2_h2_energy_kWh

    return total_energy_kWh

# Streamlit interface for user inputs
st.title("Haber-Bosch Fault Detection, Byproduct Prediction, and Energy Harvesting")

st.header("Input Parameters")
temperature = st.sidebar.slider('Temperature (°C)', min_value=300.0, max_value=550.0, step=1.0, value=450.0)
pressure = st.sidebar.slider('Pressure (atm)', min_value=100.0, max_value=300.0, step=1.0, value=200.0)
h2_n2_ratio = st.sidebar.slider('H2/N2 Ratio', min_value=1.5, max_value=3.5, step=0.1, value=3.0)
catalyst_age = st.sidebar.slider('Catalyst Age (hours)', min_value=0, max_value=1000, step=10, value=500)
space_velocity = st.sidebar.slider('Space Velocity (h^-1)', min_value=10000, max_value=30000, step=100, value=20000)

# Organize the input data into an array
input_data = np.array([[temperature, pressure, h2_n2_ratio, catalyst_age, space_velocity]])

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Predict if there's a fault
fault_prediction = fault_model.predict(input_data_scaled)[0]
conversion_rate = conversion_model.predict(input_data_scaled)[0]

# Display fault detection results
if fault_prediction == 1:
    st.error("Fault detected in the process!")
    
    st.subheader("Suggested Adjustments:")
    adjustments = suggest_parameter_adjustment(temperature, pressure, h2_n2_ratio, catalyst_age, space_velocity)
    for adj in adjustments:
        st.write(f"- {adj}")
else:
    st.success("No fault detected in the process!")
    st.write(f"Predicted Conversion Rate: {conversion_rate:.2f}")

    # If no fault, predict the byproducts and energy harvesting potential
    st.subheader("Byproducts and Energy Harvesting:")
    
    byproducts = predict_byproducts(temperature, pressure, h2_n2_ratio, catalyst_age, space_velocity)
    
    st.subheader("Predicted Byproducts:")
    for key, value in byproducts.items():
        st.write(f"{key}: {value:.2f}")

    # Calculate and display electric energy produced from byproducts
    electric_energy_kWh = calculate_electric_energy(byproducts)
    st.success(f"Estimated Electric Energy from Byproducts: {electric_energy_kWh:.2f} kWh")