import streamlit as st
import h2o
import pandas as pd
from h2o.frame import H2OFrame

# Initialize H2O with explicit settings
try:
    h2o.init(port=54321, max_mem_size="256m", start_h2o=True, strict_version_check=False, min_mem_size="128m")
except Exception as e:
    st.error(f"H2O initialization failed: {e}")
    raise

# Load the trained fraud detection model
model_path = "XGBoost_grid_1_AutoML_1_20250223_170838_model_2"
try:
    model = h2o.load_model(model_path)
except Exception as e:
    st.error(f"Model loading failed: {e}")
    raise

# Streamlit UI
st.title("🔍 Credit Card Fraud Detection")
st.write("Enter transaction details to check for fraud risk.")

def user_input():
    v1 = st.number_input("V1", value=0.0, format="%.2f")
    v2 = st.number_input("V2", value=0.0, format="%.2f")
    v3 = st.number_input("V3", value=0.0, format="%.2f")
    v4 = st.number_input("V4", value=0.0, format="%.2f")

    amount = st.number_input("Transaction Amount", value=50.0, format="%.2f")
    data_dict = {
        "Time": 0.0, "V1": v1, "V2": v2, "V3": v3, "V4": 0.0, "V5": 0.0, "V6": 0.0, "V7": 0.0,
        "V8": 0.0, "V9": 0.0, "V10": 0.0, "V11": 0.0, "V12": 0.0, "V13": 0.0,
        "V14": 0.0, "V15": 0.0, "V16": 0.0, "V17": 0.0, "V18": 0.0, "V19": 0.0,
        "V20": 0.0, "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
        "V26": 0.0, "V27": 0.0, "V28": 0.0, "Amount": amount
    }
    return pd.DataFrame([data_dict])

input_data = user_input()

if st.button("Detect Fraud"):
    try:
        h2o_data = H2OFrame(input_data)
        prediction = model.predict(h2o_data)
        pred_df = prediction.as_data_frame()
        fraud_prob = pred_df["p1"][0]
        fraud_label = 1 if fraud_prob > 0.5 else 0
        st.write("### Prediction Result:")
        st.write(f"Fraud Probability: {fraud_prob:.2%}")
        if fraud_label == 1:
            st.error("🚨 Fraudulent Transaction Detected!")
        else:
            st.success("✅ Transaction is Legitimate.")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
