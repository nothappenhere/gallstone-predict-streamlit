import streamlit as st
from utils.xgboost_utils import predict_gallstone, show_health_tips


st.set_page_config(
    page_title="Machine Learning",
    page_icon=":material/network_intelligence:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "## **Get this on [Github](https://github.com/nothappenhere/gallstone-xgboost-streamlit.git)!**",
    },
)


# Streamlit UI
st.title("Aplikasi Prediksi Gallstone dengan XGBoost")
st.write(
    """
Aplikasi ini dirancang untuk membantu tenaga medis atau peneliti dalam memprediksi kemungkinan seseorang mengalami *gallstone* (batu empedu) berdasarkan data medis dan biometrik.

Dengan aplikasi ini, pengguna dapat:
- Memasukkan data klinis dan hasil pemeriksaan tubuh pasien, seperti usia, jenis kelamin, komorbiditas, kadar kolesterol, kadar gula darah, dan komposisi tubuh.
- Melakukan prediksi risiko gallstone secara otomatis menggunakan model *machine learning* **XGBoost** yang telah dilatih sebelumnya.
- Melihat hasil prediksi secara langsung dan praktis melalui antarmuka berbasis web menggunakan Streamlit.

Aplikasi ini bertujuan untuk mendukung pengambilan keputusan secara cepat dan berbasis data.
"""
)


# UI
st.divider()
st.title("Prediksi Gallstone Status dengan XGBoost")

with st.form("prediction_form"):
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
        with row1[0].container(height=350, border=False):
            Age = st.number_input("Age", help="Usia (tahun)", min_value=0, max_value=100)
        with row1[1]:
            st.html(vertical_divider)
        with row1[2].container(height=350, border=False):
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
            Comorbidity = st.selectbox(
                "Comorbidity",
                ("Ya", "Tidak"),
                help="Apakah pasien memiliki komorbiditas (penyakit penyerta)",
                index=None,
                placeholder="Apakah pasien memiliki komorbiditas (penyakit penyerta)?",
            )
    with st.container(height=100, border=True):
        row2 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row2[0].container(height=350, border=False):
            CAD = st.selectbox(
                "Coronary Artery Disease (CAD)",
                ("Ya", "Tidak"),
                help="Riwayat penyakit arteri koroner",
                index=None,
                placeholder="Riwayat penyakit arteri koroner?",
            )
        with row2[1]:
            st.html(vertical_divider)
        with row2[2].container(height=350, border=False):
            Hypothyroidism = st.selectbox(
                "Hypothyroidism",
                ("Ya", "Tidak"),
                help="Hipotiroidisme",
                index=None,
                placeholder="Hipotiroidisme?",
            )
        with row2[3]:
            st.html(vertical_divider)
        with row2[4]:
            Hyperlipidemia = st.selectbox(
                "Hyperlipidemia",
                ("Ya", "Tidak"),
                help="Kadar lemak tinggi dalam darah",
                index=None,
                placeholder="Kadar lemak tinggi dalam darah?",
            )
    with st.container(height=100, border=True):
        row3 = st.columns([10.9])
        with row3[0].container(height=350, border=False):
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
        with row1[0].container(height=350, border=False):
            Height = st.number_input(
                "Height", help="Tinggi badan (cm)", min_value=0, max_value=250
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2].container(height=350, border=False):
            Weight = st.number_input(
                "Weight", help="Berat badan (kg)", min_value=0, max_value=200
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            BMI = st.number_input(
                "Body Mass Index (BMI)",
                help="Indeks massa tubuh",
                min_value=0,
                max_value=100,
            )

    st.divider()

    st.subheader(":material/water_drop: Komposisi Cairan Tubuh:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0].container(height=350, border=False):
            TBW = st.number_input(
                "Total Body Water (TBW)",
                help="Total cairan tubuh",
                min_value=0,
                max_value=100,
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2].container(height=350, border=False):
            ECW = st.number_input(
                "Extracellular Water (ECW)",
                help="Cairan di luar sel",
                min_value=0,
                max_value=100,
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            ICW = st.number_input(
                "Intracellular Water (ICW)",
                help="Cairan di dalam sel",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row2 = st.columns([10.9])
        with row2[0].container(height=350, border=False):
            ECF_TBW = st.number_input(
                "Extracellular Fluid / Total Body Water (ECF/TBW)",
                help="Rasio cairan ekstraseluler terhadap cairan total",
                min_value=0,
                max_value=100,
            )

    st.divider()

    st.subheader(":material/accessibility_new: Komposisi Tubuh:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0].container(height=350, border=False):
            TBFR = st.number_input(
                "Total Body Fat Ratio (TBFR)",
                help="Rasio lemak tubuh (%)",
                min_value=0,
                max_value=100,
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2].container(height=350, border=False):
            LM = st.number_input(
                "Lean Mass (LM)",
                help="Massa tanpa lemak (%)",
                min_value=0,
                max_value=100,
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            Protein = st.number_input(
                "Body Protein Content (Protein)",
                help="Kandungan protein tubuh (%)",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row2 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row2[0].container(height=350, border=False):
            VFR = st.number_input(
                "Visceral Fat Rating (VFR)",
                help="Penilaian lemak viseral",
                min_value=0,
                max_value=100,
            )
        with row2[1]:
            st.html(vertical_divider)
        with row2[2].container(height=350, border=False):
            BM = st.number_input(
                "Bone Mass (BM)",
                help="Massa tulang",
                min_value=0,
                max_value=100,
            )
        with row2[3]:
            st.html(vertical_divider)
        with row2[4]:
            MM = st.number_input(
                "Muscle Mass (MM)",
                help="Massa otot",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row3 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row3[0].container(height=350, border=False):
            Obesity = st.number_input(
                "Obesity",
                help="Tingkat obesitas (%)",
                min_value=0,
                max_value=100,
            )
        with row3[1]:
            st.html(vertical_divider)
        with row3[2].container(height=350, border=False):
            TFC = st.number_input(
                "Total Fat Content (TFC)",
                help="Kandungan lemak total",
                min_value=0,
                max_value=100,
            )
        with row3[3]:
            st.html(vertical_divider)
        with row3[4]:
            VFA = st.number_input(
                "Visceral Fat Area (VFA)",
                help=" Luas lemak viseral",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row4 = st.columns([8.0, 0.2, 8.0])
        with row4[0].container(height=350, border=False):
            VMA = st.number_input(
                "Visceral Muscle Area (VMA)",
                help="Luas otot viseral (Kg)",
                min_value=0,
                max_value=100,
            )
        with row4[1]:
            st.html(vertical_divider)
        with row4[2].container(height=350, border=False):
            HFA = st.number_input(
                "Hepatic Fat Accumulation (HFA)",
                help="Akumulasi lemak hati",
                min_value=0,
                max_value=100,
            )

    st.divider()

    st.subheader(":material/genetics: Indikator Biokimia:")
    with st.container(height=100, border=True):
        row1 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row1[0].container(height=350, border=False):
            Glucose = st.number_input(
                "Glucose",
                help="Kadar glukosa",
                min_value=0,
                max_value=100,
            )
        with row1[1]:
            st.html(vertical_divider)
        with row1[2].container(height=350, border=False):
            TC = st.number_input(
                "Total Cholesterol (TC)",
                help="Kolesterol total",
                min_value=0,
                max_value=100,
            )
        with row1[3]:
            st.html(vertical_divider)
        with row1[4]:
            LDL = st.number_input(
                "Low Density Lipoprotein (LDL)",
                help="LDL (kolesterol jahat)",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row2 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row2[0].container(height=350, border=False):
            HDL = st.number_input(
                "High Density Lipoprotein (HDL)",
                help=" HDL (kolesterol baik)",
                min_value=0,
                max_value=100,
            )
        with row2[1]:
            st.html(vertical_divider)
        with row2[2].container(height=350, border=False):
            Triglyceride = st.number_input(
                "Triglyceride",
                help="Trigliserida",
                min_value=0,
                max_value=100,
            )
        with row2[3]:
            st.html(vertical_divider)
        with row2[4]:
            AST = st.number_input(
                "Aspartat Aminotransferaz (AST)",
                help="Enzim hati (fungsi hati)",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row3 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row3[0].container(height=350, border=False):
            ALT = st.number_input(
                "Alanin Aminotransferaz (ALT)",
                help="Enzim hati (fungsi hati)",
                min_value=0,
                max_value=100,
            )
        with row3[1]:
            st.html(vertical_divider)
        with row3[2].container(height=350, border=False):
            ALP = st.number_input(
                "Alkalinehosphatase (ALP)",
                help="Enzim hati (fungsi hati)",
                min_value=0,
                max_value=100,
            )
        with row3[3]:
            st.html(vertical_divider)
        with row3[4]:
            Creatinine = st.number_input(
                "Creatinine",
                help="Fungsi ginjal",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row4 = st.columns([8.0, 0.2, 8.0, 0.2, 8.0])
        with row4[0].container(height=350, border=False):
            GFR = st.number_input(
                "Glomerular Filtration Rate (GFR)",
                help="Laju filtrasi glomerulus (fungsi ginjal)",
                min_value=0,
                max_value=100,
            )
        with row4[1]:
            st.html(vertical_divider)
        with row4[2].container(height=350, border=False):
            CRP = st.selectbox(
                "C-Reactive Protein (CRP)",
                ("Ada inflamasi", "Tidak ada inflamasi"),
                help="Penanda inflamasi",
                index=None,
                placeholder="Penanda inflamasi?",
            )
        with row4[3]:
            st.html(vertical_divider)
        with row4[4]:
            HGB = st.number_input(
                "Hemoglobin (HGB)",
                help="Kadar hemoglobin",
                min_value=0,
                max_value=100,
            )
    with st.container(height=100, border=True):
        row5 = st.columns([10.9])
        with row5[0].container(height=350, border=False):
            VitaminD = st.number_input(
                "Vitamin D",
                help="Kadar vitamin D",
                min_value=0,
                max_value=100,
            )

    submitted = st.form_submit_button(
        ":material/planner_review: Prediksi", type="primary"
    )

    if submitted:
        input_values = [
            Age,
            1 if Gender == "Laki-laki" else 0,
            1 if Comorbidity == "Ya" else 0,
            1 if CAD == "Ya" else 0,
            1 if Hypothyroidism == "Ya" else 0,
            1 if Hyperlipidemia == "Ya" else 0,
            1 if DM == "Ya" else 0,
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
            1 if CRP == "Ada inflamasi" else 0,
            HGB,
            VitaminD,
        ]

        result = predict_gallstone(input_values)
        result_str = "positif" if result == 1 else "negatif"
        result_clr = "inverse" if result == 1 else "normal"

        st.metric(
            label="Gallstone Status",
            value=result_str.capitalize(),
            delta="Hasil Prediksi",
            delta_color=result_clr,
            border=True,
        )

        if result_str == "positif":
            st.error("Hasil menunjukkan kemungkinan adanya batu empedu.")
        else:
            st.info("Tidak terdeteksi kemungkinan batu empedu.")

        st.markdown("### 💡 Saran Kesehatan Berdasarkan Data Anda")
        show_health_tips(input_values)
