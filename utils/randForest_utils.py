import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model, scaler, dan kolom
model = joblib.load("randomForest_model.joblib")
scaler = joblib.load("scaler.joblib")
columns = joblib.load("columns.joblib")


def predict_gallstone(input_data):
    try:
        # Buat DataFrame dari input
        df = pd.DataFrame([input_data], columns=columns)

        # Scaling
        scaled_data = scaler.transform(df)

        # Prediksi
        prediction = model.predict(scaled_data)[0]

        st.divider()
        return int(prediction)
    except Exception as e:
        return f"Prediction failed: {str(e)}"


def show_health_tips(input_values):
    (
        Age,
        Gender,
        CAD,
        Hypothyroidism,
        Hyperlipidemia,
        DM,
        Height,
        Weight,
        BMI,
        TBFR,
        VFA,
        HFA,
        Glucose,
        TC,
        LDL,
        HDL,
        Triglyceride,
        AST,
        ALT,
        ALP,
        CRP,
    ) = input_values

    # Body Mass Index (BMI): Indeks massa tubuh
    if BMI < 18.5:
        st.info(
            f""":information_source: *Body Mass Index* (BMI) rendah ~ (BMI Anda: {BMI}). 
            
            Pastikan Anda mengonsumsi cukup kalori dan nutrisi seimbang."""
        )
    elif BMI > 24.9:
        st.warning(
            f""":warning: *Body Mass Index* (BMI) di atas normal ~ (BMI Anda: {BMI}). 
            
            Pertimbangkan pola makan sehat dan olahraga rutin."""
        )

    # Glucose: Kadar glukosa
    if Glucose > 125:
        st.warning(
            f""":warning: *Glucose* (Kadar glukosa) tinggi ~ (Glukosa Anda: {Glucose}). 
            
            Waspadai risiko diabetes. Kurangi asupan gula dan karbohidrat sederhana."""
        )
    elif Glucose < 70:
        st.info(
            f""":information_source: *Glucose* (Kadar glukosa) rendah ~ (Glukosa Anda: {Glucose}). 
            
            Pastikan makan teratur, terutama sarapan."""
        )

    # Total Cholesterol (TC): Kolesterol total
    if TC > 200:
        st.warning(
            f""":warning: *Total Cholesterol* (TC) tinggi ~ (Total Kolesterol Anda: {TC}). 
            
            Kurangi makanan berlemak jenuh dan perbanyak serat."""
        )

    # Low Density Lipoprotein (LDL): LDL (kolesterol jahat)
    if LDL > 130:
        st.warning(
            f""":warning: *Low Density Lipoprotein* (kolesterol jahat) tinggi ~ (LDL Anda: {LDL}). 
            
            Tingkatkan konsumsi makanan berlemak sehat seperti alpukat dan ikan."""
        )

    # High Density Lipoprotein (HDL): HDL (kolesterol baik)
    if HDL < 40:
        st.info(
            f""":information_source: *High Density Lipoprotein* (kolesterol baik) rendah ~ (HDL Anda: {HDL}). 
            
            Olahraga teratur dan konsumsi lemak sehat dapat membantu meningkatkannya."""
        )

    # Triglyceride: Trigliserida
    if Triglyceride > 150:
        st.warning(
            f""":warning: *Triglyceride* (Trigliserida) tinggi ~ (Trigliserida Anda: {Triglyceride}). 
            
            Kurangi gula dan alkohol, serta perbanyak aktivitas fisik."""
        )

    # Enzim Hati
    if AST > 40 or ALT > 40 or ALP > 120:
        st.warning(
            """:warning: Enzim hati tinggi. 
            
            Hindari alkohol dan konsultasikan dengan dokter jika berlanjut."""
        )

    # C-Reactive Protein (CRP): Penanda inflamasi (0 = tidak ada, 1 = ada inflamasi)
    if CRP > 3:
        st.info(
            f""":information_source: *C-Reactive Protein* (CRP) tinggi ~ (Penanda inflamasi Anda {CRP}). 

            Bisa mengindikasikan peradangan. Jaga pola makan anti-inflamasi."""
        )
