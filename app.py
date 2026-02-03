import streamlit as st
import pandas as pd
import joblib

# ----------------------------
# Load trained model
# ----------------------------
model = joblib.load("compressor_fault_model.pkl")

# ----------------------------
# Rule-based functions (UNCHANGED)
# ----------------------------
def current_status(current):
    if current < 10:
        return "CRITICAL (Belt / coupling / unload fault)"
    elif 25 <= current <= 60:
        return "NORMAL"
    elif 60 < current <= 70:
        return "WARNING"
    elif current > 70:
        return "CRITICAL"
    else:
        return "ABNORMAL"

def temperature_status(temperature):
    if 60 <= temperature <= 90:
        return "NORMAL"
    elif 90 < temperature <= 105:
        return "WARNING"
    elif temperature > 105:
        return "CRITICAL (Overheating)"
    else:
        return "ABNORMAL"

def pressure_status(pressure):
    if 2.8 <= pressure <= 3.2:
        return "NORMAL"
    elif (2.4 <= pressure < 2.8) or (3.2 < pressure <= 3.6):
        return "WARNING"
    else:
        return "CRITICAL"

def dp_status(dp):
    if dp <= 0.2:
        return "NORMAL"
    elif dp <= 0.5:
        return "WARNING (Filter clogging)"
    else:
        return "CRITICAL (Filter choked)"

def run_hours_status(hours):
    if hours <= 2000:
        return "NORMAL"
    elif hours <= 3000:
        return "WARNING"
    else:
        return "CRITICAL (Service required)"

def vibration_status(vibration):
    if vibration <= 4:
        return "NORMAL"
    elif vibration <= 7:
        return "WARNING"
    else:
        return "CRITICAL (High vibration)"

def diagnose_fault(current, temperature, pressure, dp, hours, vibration):
    if current > 60 and pressure < 2.8:
        return "Air leak or Airend wear"
    elif temperature > 90 and dp > 0.2:
        return "Filter choking"
    elif current > 60 and vibration > 4:
        return "Bearing or alignment issue"
    else:
        return "No specific fault detected"

status_map = {0: "NORMAL", 1: "WARNING", 2: "CRITICAL"}

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Compressor Monitoring", layout="centered")
st.title("🔧 Rotary Screw Compressor Diagnostic System")

current = st.number_input("Motor Current (A)", min_value=0.0)
temperature = st.number_input("Oil Temperature (°C)", min_value=0.0)
pressure = st.number_input("Line Pressure (bar)", min_value=0.0)
dp = st.number_input("Differential Pressure (bar)", min_value=0.0)
hours = st.number_input("Running Hours", min_value=0)
vibration = st.number_input("Vibration (mm/s)", min_value=0.0)

if st.button("🔍 Diagnose"):

    user_df = pd.DataFrame([[current, temperature, pressure, dp, hours, vibration]],
        columns=[
            "Motor_Current_A",
            "Oil_Temperature_C",
            "Line_Pressure_bar",
            "Filter_DeltaP_bar",
            "Running_Hours",
            "Vibration_RMS_mm_s"
        ]
    )

    prediction = model.predict(user_df)[0]
    overall_status = status_map[prediction]

    st.markdown("## 📊 Diagnostic Report")
    st.write("Motor Current :", current_status(current))
    st.write("Oil Temperature :", temperature_status(temperature))
    st.write("Line Pressure :", pressure_status(pressure))
    st.write("Filter ΔP :", dp_status(dp))
    st.write("Running Hours :", run_hours_status(hours))
    st.write("Vibration :", vibration_status(vibration))

    st.markdown("---")
    st.write("### 🧠 Overall Machine Status :", overall_status)
    st.write("### 🔍 Likely Fault Cause :", diagnose_fault(
        current, temperature, pressure, dp, hours, vibration
    ))

    if overall_status == "CRITICAL":
        st.error("Immediate maintenance required!")
    elif overall_status == "WARNING":
        st.warning("Monitor machine closely.")
    else:
        st.success("Machine operating normally.")
