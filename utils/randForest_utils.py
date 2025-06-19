import streamlit as st
import pandas as pd
import joblib
import io
from gtts import gTTS
import datetime


# Load model, scaler, dan kolom
model = joblib.load("randomForest_model.joblib")
scaler = joblib.load("scaler.joblib")
columns = joblib.load("columns.joblib")


def predict_gallstone(input_data):
    try:
        # Buat DataFrame dari input
        df = pd.DataFrame([input_data], columns=columns)
        # Scaling
        scaled_data = pd.DataFrame(scaler.transform(df), columns=columns)
        # Prediksi
        prediction = model.predict(scaled_data)[0]

        st.divider()
        return int(prediction)
    except Exception as e:
        return f"Prediction failed: {str(e)}"


def play_audio(text, autoplay=True):
    tts = gTTS(text, lang="id")
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp.read(), format="audio/mp3", autoplay=autoplay)


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
            f""":information_source: *Body Mass Index* (BMI) rendah (*underweight*) || (BMI Anda: {BMI:.2f}). 
            
            Pastikan Anda mengonsumsi cukup kalori dan nutrisi seimbang."""
        )
    elif BMI > 24.9:
        st.warning(
            f""":warning: *Body Mass Index* (BMI) di atas normal (*overweight*) || (BMI Anda: {BMI:.2f}). 
            
            Pertimbangkan pola makan sehat dan olahraga rutin."""
        )

    # Glucose: Kadar glukosa
    if Glucose > 125:
        st.warning(
            f""":warning: *Glucose* (Kadar glukosa) tinggi || (Glucose Anda: {Glucose}). 
            
            Waspadai risiko diabetes. Kurangi asupan gula dan karbohidrat sederhana."""
        )
    elif Glucose < 70:
        st.info(
            f""":information_source: *Glucose* (Kadar glukosa) rendah || (Glucose Anda: {Glucose}). 
            
            Pastikan makan teratur, terutama sarapan."""
        )

    # Total Cholesterol (TC): Kolesterol total
    if TC > 200:
        st.warning(
            f""":warning: *Total Cholesterol* (Total Kolesterol) tinggi || (TC Anda: {TC}). 
            
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
            f""":warning: *Triglyceride* (Trigliserida) tinggi || (Triglyceride Anda: {Triglyceride}). 
            
            Kurangi gula dan alkohol, serta perbanyak aktivitas fisik."""
        )

    # Enzim Hati
    if AST > 40 or ALT > 40 or ALP > 120:
        st.warning(
            f""":warning: Enzim hati tinggi || (Enzim hati Anda: {AST, ALT, ALP}). 
            
            Hindari alkohol dan konsultasikan dengan dokter jika berlanjut."""
        )

    # C-Reactive Protein (CRP): Penanda inflamasi (0 = tidak ada, 1 = ada inflamasi)
    if CRP > 3:
        st.info(
            f""":information_source: *C-Reactive Protein* (Penanda inflamasi) tinggi || (CRP Anda: {CRP}). 

            Bisa mengindikasikan peradangan. Jaga pola makan anti-inflamasi."""
        )


def top_risk_factors(input_values):
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

    risks = []

    if BMI > 25:
        risks.append(("BMI", f"{BMI:.2f}", "Indeks Massa Tubuh (BMI) di atas normal (*overweight*)"))
    if Glucose > 125:
        risks.append(("Glukosa", Glucose, "Kadar gula darah tinggi"))
    if LDL > 130:
        risks.append(("LDL", LDL, "Kolesterol jahat tinggi"))
    if CRP == 1:
        risks.append(("CRP", "Ada inflamasi", "Terdapat tanda peradangan"))
    if Age >= 40:
        risks.append(("Usia", Age, "Usia di atas 40 tahun merupakan faktor risiko"))
    if Gender == 1:
        risks.append(("Jenis Kelamin", "Perempuan", "Perempuan lebih berisiko"))

    top_risks = risks[:6]

    markdown = "### :material/troubleshoot: Faktor Risiko Tertinggi\n"
    for label, value, reason in top_risks:
        markdown += f"- **{label}:** {value} :material/keyboard_double_arrow_right: {reason}\n"

    return markdown


def download_report(result_str, input_values):
    (
        Age, Gender, CAD, Hypothyroidism, Hyperlipidemia, DM,
        Height, Weight, BMI, TBFR, VFA, HFA, Glucose, TC,
        LDL, HDL, Triglyceride, AST, ALT, ALP, CRP
    ) = input_values

    gender_str = "Perempuan" if Gender == 1 else "Laki-laki"
    inflamasi_str = "Ya" if CRP == 1 else "Tidak"
    rekomendasi = (
        "Hasil menunjukkan kemungkinan adanya batu empedu.\nDisarankan untuk konsultasi lebih lanjut ke fasilitas layanan kesehatan."
        if result_str == "positif"
        else "Tidak terdeteksi batu empedu. Tetap jaga pola makan, berat badan ideal, dan lakukan pemeriksaan berkala."
    )
    
    return f"""
===========================================
      LAPORAN HASIL PREDIKSI GALLSTONE
===========================================

📅 Tanggal Pemeriksaan : {datetime.date.today().strftime('%d %B %Y')}
🩺 Status Prediksi     : {result_str.upper()}

-------------------------------------------
            Informasi Pasien
-------------------------------------------
- Usia                 : {Age} tahun
- Jenis Kelamin        : {gender_str}
- Tinggi Badan         : {Height} cm
- Berat Badan          : {Weight} kg
- BMI                  : {BMI:.2f}
- Riwayat CAD          : {"Ya" if CAD else "Tidak"}
- Hypothyroidism       : {"Ya" if Hypothyroidism else "Tidak"}
- Hyperlipidemia       : {"Ya" if Hyperlipidemia else "Tidak"}
- Diabetes Mellitus    : {"Ya" if DM else "Tidak"}

-------------------------------------------
          Indikator Klinis Utama
-------------------------------------------
- TBFR (Total Body Fat Ratio)     : {TBFR} %
- VFA (Visceral Fat Area)         : {VFA}
- HFA (Hepatic Fat Accumulation)  : {HFA}
- Glukosa                         : {Glucose} mg/dL
- Total Kolesterol (TC)           : {TC} mg/dL
- LDL (Kolesterol jahat)          : {LDL} mg/dL
- HDL (Kolesterol baik)           : {HDL} mg/dL
- Trigliserida                    : {Triglyceride} mg/dL
- AST/ALT/ALP (Enzim hati)        : {AST}/{ALT}/{ALP}
- CRP (C-Reactive Protein)        : {inflamasi_str}

-------------------------------------------
          Rekomendasi & Catatan
-------------------------------------------
{rekomendasi}


+-----------------------------------------------------------------------------------------------------------------------+
| ⚠️ Catatan: Laporan ini bersifat prediktif dan tidak menggantikan diagnosa dari dokter atau tenaga medis profesional. |
+-----------------------------------------------------------------------------------------------------------------------+
"""