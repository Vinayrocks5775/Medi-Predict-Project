import streamlit as st
import pandas as pd
import numpy as np
import joblib
from fpdf import FPDF
import os
from io import BytesIO
from azure.storage.blob import BlobServiceClient

# --------------------
# 🔐 Load model & encoder from Azure Blob Storage
# --------------------
@st.cache_resource
def load_model_from_blob():
    conn_str = os.environ.get("BLOB_CONN_STR")  # Set this in Azure App Service > Configuration
    if not conn_str:
        st.error("Azure Blob connection string not found.")
        st.stop()

    try:
        blob_service = BlobServiceClient.from_connection_string(conn_str)
        container = blob_service.get_container_client("symptomdata")

        # Download model
        model_blob = container.download_blob("gold/final_symptom_checker_model_all_features.pkl").readall()
        model = joblib.load(BytesIO(model_blob))

        # Download label encoder
        encoder_blob = container.download_blob("gold/label_encoder_all_features.pkl").readall()
        le = joblib.load(BytesIO(encoder_blob))

        return model, le
    except Exception as e:
        st.error(f"Error loading model from blob: {e}")
        st.stop()

model, le = load_model_from_blob()

# --------------------
# 🎯 UI Logic
# --------------------
st.set_page_config(page_title="Symptom Checker", layout="centered")
st.title("🩺 Disease Prediction from Symptoms")

# Sample symptoms (should match model training features)
symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering',
            'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue']  # Replace with all used features

symptom_input = {}
for symptom in symptoms:
    symptom_input[symptom] = st.checkbox(symptom.replace("_", " ").capitalize())

if st.button("🔍 Predict Disease"):
    input_vals = [1 if symptom_input[s] else 0 for s in symptoms]
    X = np.array([input_vals])
    pred = model.predict(X)
    pred_label = le.inverse_transform(pred)[0]

    st.success(f"🩺 Predicted Disease: **{pred_label}**")

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Symptom Checker Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Predicted Disease: {pred_label}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Symptoms provided:", ln=True)
    for s in symptoms:
        if symptom_input[s]:
            pdf.cell(200, 10, txt=f" - {s.replace('_', ' ').capitalize()}", ln=True)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    st.download_button("📄 Download Report (PDF)", data=pdf_output, file_name="prediction_report.pdf")
