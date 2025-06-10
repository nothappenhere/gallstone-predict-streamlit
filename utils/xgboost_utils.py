import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model, scaler, dan kolom
model = joblib.load("xgb_model.joblib")
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
        return f":material/dangerous:  Prediction failed: {str(e)}"


def show_health_tips(input_values):
    (
        Age,
        Gender,
        Comorbidity,
        CAD,
        Hypothyroidism,
        Hyperlipidemia,
        DM,
        Height,
        Weight,
        BMI,
        TBW,
        ECW,
        ICW,
        ECF_TBW,
        TBFR,
        LM,
        Protein,
        VFR,
        BM,
        MM,
        Obesity,
        TFC,
        VFA,
        VMA,
        HFA,
        Glucose,
        TC,
        LDL,
        HDL,
        Triglyceride,
        AST,
        ALT,
        ALP,
        Creatinine,
        GFR,
        CRP,
        HGB,
        VitaminD,
    ) = input_values

    # Body Mass Index (BMI): Indeks massa tubuh
    if BMI < 18.5:
        st.info(
            f""":information_source: *Body Mass Index* (BMI) rendah || (BMI Anda: {BMI}). 
            
            Pastikan Anda mengonsumsi cukup kalori dan nutrisi seimbang."""
        )
    elif BMI > 24.9:
        st.warning(
            f""":warning: *Body Mass Index* (BMI) di atas normal || (BMI Anda: {BMI}). 
            
            Pertimbangkan pola makan sehat dan olahraga rutin."""
        )

    # Glucose: Kadar glukosa
    if Glucose > 125:
        st.warning(
            f""":warning: *Glucose* (Kadar glukosa) tinggi || (Glukosa Anda: {Glucose}). 
            
            Waspadai risiko diabetes. Kurangi asupan gula dan karbohidrat sederhana."""
        )
    elif Glucose < 70:
        st.info(
            f""":information_source: *Glucose* (Kadar glukosa) rendah || (Glukosa Anda: {Glucose}). 
            
            Pastikan makan teratur, terutama sarapan."""
        )

    # Total Cholesterol (TC): Kolesterol total
    if TC > 200:
        st.warning(
            f""":warning: *Total Cholesterol* (TC) tinggi || (Total Kolesterol Anda: {TC}). 
            
            Kurangi makanan berlemak jenuh dan perbanyak serat."""
        )

    # Low Density Lipoprotein (LDL): LDL (kolesterol jahat)
    if LDL > 130:
        st.warning(
            f""":warning: *Low Density Lipoprotein* (kolesterol jahat) tinggi || (LDL Anda: {LDL}). 
            
            Tingkatkan konsumsi makanan berlemak sehat seperti alpukat dan ikan."""
        )

    # High Density Lipoprotein (HDL): HDL (kolesterol baik)
    if HDL < 40:
        st.info(
            f""":information_source: *High Density Lipoprotein* (kolesterol baik) rendah || (HDL Anda: {HDL}). 
            
            Olahraga teratur dan konsumsi lemak sehat dapat membantu meningkatkannya."""
        )

    # Triglyceride: Trigliserida
    if Triglyceride > 150:
        st.warning(
            f""":warning: *Triglyceride* (Trigliserida) tinggi || (Trigliserida Anda: {Triglyceride}). 
            
            Kurangi gula dan alkohol, serta perbanyak aktivitas fisik."""
        )

    # Enzim Hati
    if AST > 40 or ALT > 40 or ALP > 120:
        st.warning(
            """:warning: Enzim hati tinggi. 
            
            Hindari alkohol dan konsultasikan dengan dokter jika berlanjut."""
        )

    # Creatinine: Fungsi ginjal
    if Creatinine > 1.2:
        st.warning(
            f""":warning: *Creatinine* (Fungsi ginjal) tinggi || (Fungsi ginjal Anda: {Creatinine}). 
            
            Perhatikan asupan protein dan hidrasi yang cukup."""
        )

    # Glomerular Filtration Rate (GFR): Laju filtrasi glomerulus (fungsi ginjal)
    if GFR < 60:
        st.warning(
            f""":warning: *Glomerular Filtration Rate* (GFR) rendah || (Fungsi ginjal Anda: {GFR}). 
            
            Ginjal mungkin tidak berfungsi optimal. Konsultasikan ke dokter."""
        )

    # C-Reactive Protein (CRP): Penanda inflamasi (0 = tidak ada, 1 = ada inflamasi)
    if CRP > 3:
        st.info(
            f""":information_source: *C-Reactive Protein* (CRP) tinggi || (Penanda inflamasi Anda {CRP}). 

            Bisa mengindikasikan peradangan. Jaga pola makan anti-inflamasi."""
        )

    # Hemoglobin (HGB): Kadar hemoglobin
    if HGB < 12:
        st.info(
            f""":information_source: *Hemoglobin* (HGB) rendah || (Kadar hemoglobin Anda: {HGB}). 
            
            Pastikan konsumsi zat besi cukup seperti daging merah dan sayuran hijau."""
        )

    # Vitamin D: Kadar vitamin D
    if VitaminD < 30:
        st.info(
            f""":information_source: Vitamin D rendah || (Kadar vitamin D Anda: {VitaminD}). 
            
            Perbanyak paparan sinar matahari pagi atau konsumsi suplemen jika perlu."""
        )
