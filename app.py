import streamlit as st
from utils.randForest_utils import predict_gallstone, play_audio, show_health_tips, top_risk_factors, download_report


st.set_page_config(
    page_title="Gallstone Predict | Machine Learning",
    page_icon=":material/network_intelligence:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "## **Get this on [Github](https://github.com/nothappenhere/gallstone-predict-streamlit.git)!**",
    },
)


# Streamlit UI
st.title("Aplikasi Prediksi Gallstone dengan RandomForest")

st.write(
    """
Selamat datang di **Aplikasi Prediksi Gallstone** — sebuah alat bantu berbasis web yang dirancang untuk mendukung tenaga medis dan peneliti dalam memprediksi risiko *gallstone* (batu empedu) secara cepat dan akurat.

### :material/priority: Apa yang bisa Anda lakukan dengan aplikasi ini?
Dengan aplikasi ini, Anda dapat:

- Memasukkan data klinis dan hasil pemeriksaan biometrik pasien, seperti:
  - Usia, jenis kelamin
  - Riwayat penyakit penyerta (*comorbidities*) seperti CAD, DM, hipotiroidisme, dll.
  - Komposisi tubuh (tinggi badan, berat badan, BMI, TBFR, VFA, dsb)
  - Hasil laboratorium (kolesterol, glukosa, enzim hati, CRP, dll)

- Melakukan prediksi risiko *gallstone* secara otomatis menggunakan model **Random Forest** berbasis *machine learning* yang telah dilatih dengan data aktual.

- Melihat hasil prediksi secara instan melalui antarmuka yang sederhana dan interaktif menggunakan Streamlit.

### :material/target: Tujuan Aplikasi
Aplikasi ini bertujuan untuk:
- Membantu pengambilan keputusan medis berbasis data,
- Meningkatkan efisiensi skrining awal terhadap risiko *gallstone*,
- Mendukung penelitian dan pengembangan lebih lanjut di bidang kesehatan.

> ⚠️ **Catatan:** Aplikasi ini bersifat sebagai alat bantu (*decision support system*), bukan pengganti diagnosis medis resmi. Mohon tetap konsultasikan hasil prediksi dengan tenaga medis profesional.
"""
)


# UI
st.divider()
st.title("Prediksi Gallstone Status dengan RandomForest")

with st.container(border=True):
    vertical_divider = """
                  <div class="divider-vertical-line"></div>
                  <style>
                      .divider-vertical-line {
                          border-left: 2px solid rgba(49, 51, 63, 0.2);
                          height: 70px;
                          margin: auto;
                      }
                  </style>
              """

    st.subheader(":material/demography: Demografi & Riwayat Penyakit:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0]:
            Age = st.number_input(
                "Age", help="Usia (tahun)", min_value=0, max_value=100
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2]:
            Gender = st.selectbox(
                "Gender",
                ("Laki-laki", "Perempuan"),
                help="Jenis kelamin",
                index=None,
                placeholder="Jenis kelamin?",
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            CAD = st.selectbox(
                "Coronary Artery Disease (CAD)",
                ("Ya", "Tidak"),
                help="Riwayat penyakit arteri koroner",
                index=None,
                placeholder="Riwayat penyakit arteri koroner?",
            )
    with st.container(height=100, border=True):
        row2 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row2[0]:
            Hypothyroidism = st.selectbox(
                "Hypothyroidism",
                ("Ya", "Tidak"),
                help="Hipotiroidisme",
                index=None,
                placeholder="Hipotiroidisme?",
            )
        with row2[1]:
            st.html(vertical_divider)
        with row2[2]:
            Hyperlipidemia = st.selectbox(
                "Hyperlipidemia",
                ("Ya", "Tidak"),
                help="Kadar lemak tinggi dalam darah",
                index=None,
                placeholder="Kadar lemak tinggi dalam darah?",
            )
        with row2[3]:
            st.html(vertical_divider)
        with row2[4]:
            DM = st.selectbox(
                    "Diabetes Mellitus (DM)",
                    ("Ya", "Tidak"),
                    help="Diabetes",
                    index=None,
                    placeholder="Diabetes?",
                )

    st.divider()

    st.subheader(":material/straighten: Ukuran Tubuh:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0]:
            Weight = st.number_input(
                "Weight", help="Berat badan (kg)", min_value=0, max_value=150
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2]:
            Height = st.number_input(
                "Height", help="Tinggi badan (cm)", min_value=0, max_value=200
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            BMI_val = Weight / ((Height/100)**2) if Weight or Height != 0 else 0.0
            BMI = st.number_input(
                "Body Mass Index (BMI)",
                help="Indeks massa tubuh",
                value= BMI_val,
                min_value=0.0,
            )

    st.divider()

    st.subheader(":material/accessibility_new: Komposisi Tubuh:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0]:
            TBFR = st.number_input(
                "Total Body Fat Ratio (TBFR)",
                help="Rasio lemak tubuh (%)",
                min_value=0,
                max_value=50,
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2]:
            VFA = st.number_input(
                "Visceral Fat Area (VFA)",
                help=" Luas lemak viseral",
                min_value=0,
                max_value=50,
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            # 1. Definisikan sekali saja opsi HFA
            HFA_OPTIONS = (
                "Tidak ada penumpukan lemak",
                "Tingkat 1 (ringan)",
                "Tingkat 2 (sedang)",
                "Tingkat 3 (parah)",
                "Tingkat 4 (sangat parah)",
            )
            
            HFA = st.selectbox(
                "Hepatic Fat Accumulation (HFA)",
                HFA_OPTIONS,
                help="Akumulasi lemak hati",
                index=None,
                placeholder="Akumulasi lemak hati?",
            )

    st.divider()

    st.subheader(":material/genetics: Indikator Biokimia:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0]:
            Glucose = st.number_input(
                "Glucose",
                help="Kadar glukosa",
                min_value=0,
                max_value=300,
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2]:
            TC = st.number_input(
                "Total Cholesterol (TC)",
                help="Kolesterol total",
                min_value=0,
                max_value=300,
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            LDL = st.number_input(
                "Low Density Lipoprotein (LDL)",
                help="LDL (kolesterol jahat)",
                min_value=0,
                max_value=300,
            )
    with st.container(height=100, border=True):
        row2 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row2[0]:
            HDL = st.number_input(
                "High Density Lipoprotein (HDL)",
                help=" HDL (kolesterol baik)",
                min_value=0,
                max_value=100,
            )
        with row2[1]:
            st.html(vertical_divider)
        with row2[2]:
            Triglyceride = st.number_input(
                "Triglyceride",
                help="Trigliserida",
                min_value=0,
                max_value=300,
            )
        with row2[3]:
            st.html(vertical_divider)
        with row2[4]:
            AST = st.number_input(
                "Aspartat Aminotransferaz (AST)",
                help="Enzim hati (fungsi hati)",
                min_value=0,
                max_value=150,
            )
    with st.container(height=100, border=True):
        row3 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row3[0]:
            ALT = st.number_input(
                "Alanin Aminotransferaz (ALT)",
                help="Enzim hati (fungsi hati)",
                min_value=0,
                max_value=150,
            )
        with row3[1]:
            st.html(vertical_divider)
        with row3[2]:
            ALP = st.number_input(
                "Alkaline Phosphatase (ALP)",
                help="Enzim hati (fungsi hati)",
                min_value=0,
                max_value=150,
            )
        with row3[3]:
            st.html(vertical_divider)
        with row3[4]:
            CRP = st.selectbox(
                "C-Reactive Protein (CRP)",
                ("Ada inflamasi", "Tidak ada inflamasi"),
                help="Penanda inflamasi",
                index=None,
                placeholder="Penanda inflamasi?",
            )

    submitted = st.button(
        ":material/planner_review: Prediksi", type="primary", use_container_width=True
    )

    if submitted:
        # 1. Buat kamus (mapping) → lebih mudah di‑maintain
        mapping_hfa = {label: idx for idx, label in enumerate(HFA_OPTIONS)}
        # 2. Ambil nilai numeriknya; kalau user belum memilih, mapping_hfa.get() akan mengembalikan None
        hfa_value = mapping_hfa.get(HFA)
        
        input_values = [
            Age,
            1 if Gender == "Perempuan" else 0,
            1 if CAD == "Ya" else 0,
            1 if Hypothyroidism == "Ya" else 0,
            1 if Hyperlipidemia == "Ya" else 0,
            1 if DM == "Ya" else 0,
            Height,
            Weight,
            BMI,
            TBFR,
            VFA,
            hfa_value,
            Glucose,
            TC,
            LDL,
            HDL,
            Triglyceride,
            AST,
            ALT,
            ALP,
            1 if CRP == "Ada inflamasi" else 0,
        ]
        
        # if None in input_values:
        #     st.divider()
        #     st.warning(":warning: Semua kolom wajib diisi sebelum melakukan prediksi.")
        # else:
        result = predict_gallstone(input_values)
        result_str = "positif" if result == 1 else "negatif"
        result_clr = "inverse" if result == 1 else "normal"
        
        col1, col2 = st.columns(spec=2, vertical_alignment="center")
        col1.metric(
            label="Gallstone Status",
            value=result_str.capitalize(),
            delta="Hasil Prediksi",
            delta_color=result_clr,
            border=True,
        )
        
        if result_str == "positif":
            ucapan = f"Hasil menunjukkan kemungkinan adanya batu empedu. Disarankan untuk konsultasi lebih lanjut ke fasilitas layanan kesehatan."
            col2.error(ucapan)
            
            col2.download_button(
                label="Download hasil diganosis",
                data=download_report(result_str, input_values),
                file_name="laporan_gallstone.txt",
                on_click="ignore",
                type="primary",
                icon=":material/download:",
                use_container_width=True,
            )
            
            # Ucapkan dengan gTTS dalam Bahasa Indonesia
            play_audio(ucapan, autoplay=True)

            col1, col2 = st.columns(2)
            with col1.container(border=True):
                st.markdown(f"""
                    ### :material/stethoscope: Ringkasan Diagnosa
                    - **Status:** `{result_str.capitalize()}`
                    - **Usia:** {Age} tahun
                    - **Jenis Kelamin:** {Gender}
                    - **BMI:** {BMI:.2f}
                    - **Kadar Glukosa:** {Glucose} mg/dL
                """)

            with col2.container(border=True):
                st.markdown(top_risk_factors(input_values))
        else:
            ucapan = f"Tidak ditemukan tanda-tanda batu empedu. Tetap jaga kesehatan dan pola makan seimbang!"
            col2.info(ucapan)
            
            # Ucapkan dengan gTTS dalam Bahasa Indonesia
            play_audio(ucapan, autoplay=True)

        st.divider()
        
        st.markdown("### :material/lightbulb_2: Saran Kesehatan Berdasarkan Data Anda")
        show_health_tips(input_values)
