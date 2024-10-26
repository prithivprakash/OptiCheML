**Haber-Bosch Process Optimization Using AI/ML**

**Project Overview**

This project focuses on optimizing the Haber-Bosch process for ammonia synthesis by implementing machine learning models to:
- Predict key process outcomes, such as ammonia conversion rates.
- Detect potential faults in real-time to ensure safe and efficient operation.
- Provide parameter adjustment recommendations to maximize yield.
- Estimate energy harvesting potential from process byproducts, aiming to improve energy efficiency and sustainability.

By combining Support Vector Machine (SVM) models for fault detection and conversion rate prediction with energy harvesting technologies, this project provides a comprehensive solution for enhancing ammonia production processes in the chemical engineering domain.

**Motivation**

Traditional optimization methods in chemical engineering require extensive experimental setups and simulations, which can be time-consuming and costly. Leveraging AI/ML models allows for:
- Real-time predictions and fault detection.
- Higher process efficiency.
- Reduced environmental impact through byproduct energy harvesting.

This project was developed as part of a chemical engineering hackathon, with an extended goal of utilizing byproducts for sustainable energy generation.


**Project Structure**

```
├── data/                    # Directory for storing input data files
├── models/                  # Pre-trained SVM models for fault detection and conversion rate
│   ├── svc1.joblib          # Support Vector Classifier model for fault detection
│   └── svr1.joblib          # Support Vector Regressor model for conversion rate prediction
├── scaler1.joblib           # StandardScaler object for feature scaling
├── main.py                  # Main Streamlit application file
├── requirements.txt         # List of dependencies
└── README.md                # Project documentation
```

**Key Components**

1. *Fault Detection & Conversion Rate Prediction*
- **Fault Detection (SVC)**: A Support Vector Classifier is trained to predict faults based on historical data of process parameters.
- **Conversion Rate Prediction (SVR)**: A Support Vector Regressor estimates the ammonia yield from given parameters like temperature, pressure, and catalyst age.

2. *Energy Harvesting from Byproducts*
- The system predicts various byproducts generated during ammonia synthesis, such as:
  - Water (H₂O)
  - Unreacted nitrogen (N₂) and hydrogen (H₂)
  - Methane (CH₄)
  - Carbon dioxide (CO₂)
  - Heat released
- It calculates the electric energy potential from these byproducts using thermoelectric conversion for heat, and combustion or fuel cells for methane and hydrogen.

3. *User Interface with Streamlit*
   - A simple and interactive UI built using Streamlit allows users to:
     - Input process parameters (temperature, pressure, etc.).
     - View fault detection results and parameter adjustment suggestions.
     - See predicted byproducts and energy harvesting estimates.

**Usage**

1. **Input Process Parameters**: Use the sidebar sliders to enter values for temperature, pressure, H₂/N₂ ratio, catalyst age, and space velocity.
2. **Fault Detection**: The system predicts whether the current input values indicate a safe or fault condition.
3. **Conversion Rate & Parameter Adjustment Suggestions**: If a fault is detected, the application will suggest corrective actions. Otherwise, it displays the predicted ammonia yield.
4. **Byproduct Prediction & Energy Harvesting**: For safe operations, the system calculates byproduct quantities and estimates the potential electric energy that can be harvested.


## **Dependencies**

The project uses the following key libraries:
- `streamlit` for the user interface
- `numpy` for numerical calculations
- `joblib` for loading pre-trained models
- `scikit-learn` for machine learning models

All dependencies are listed in `requirements.txt`.


## **License**

This project is licensed under the MIT License.


## **Acknowledgments**

This project was developed as part of a hackathon challenge in the chemical engineering domain, conducted by Sri Venkateshwara College of Engineering. Special thanks to the fellow participants for their guidance and support.


## **Contact**

For any inquiries or collaboration requests, feel free to reach out to [Prithiv Prakash A](mailto:aprithiv2004@gmail.com).  
