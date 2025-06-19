# **Prediksi Batu Empedu (*Gallstone*) dengan Streamlit**

Proyek ini adalah aplikasi berbasis **Machine Learning** dan **Streamlit** yang digunakan untuk **memprediksi kemungkinan seseorang menderita penyakit Batu Empedu (*Gallstone*)** berdasarkan berbagai parameter kesehatan.

Aplikasi ini dapat memberikan:
- Prediksi status *positif* atau *negatif* Batu Empedu (*Gallstone*),
- Visualisasi hasil prediksi dengan indikator warna,
- Rekomendasi/saran kesehatan berdasarkan input pengguna.

## Fitur Utama
- Input data klinis seperti usia, jenis kelamin, komorbiditas, data antropometri, hingga nilai lab, dll
- Prediksi otomatis dengan model **RandomForest** yang telah dilatih sebelumnya
- Tampilan interaktif menggunakan **Streamlit**
- Saran kesehatan otomatis ditampilkan berdasarkan nilai input
- Model sudah ditraining dan di-*deploy* di lokal

## Teknologi & Library
- Python `3.10+`
- [Streamlit](https://streamlit.io/) – untuk UI berbasis web
- [RandomForest](https://en.wikipedia.org/wiki/Random_forest) – model prediktif
- [Scikit-Learn](https://scikit-learn.org/) – untuk preprocessing
- [Pandas](https://pandas.pydata.org/) – untuk manipulasi data
- [Joblib](https://joblib.readthedocs.io/) – untuk load model dan scaler

## Instalasi
1. Pastikan Python `3.10` atau lebih tinggi sudah terinstall.
2. Clone repository ini:
```bash
git clone https://github.com/nothappenhere/gallstone-predict-streamlit.git
cd gallstone-predict-streamlit
```
4. Buat dan aktifkan virtual environment:
```bash
python -m venv py-randforest-env312

source py-randforest-env312/bin/activate  # (Linux/Mac)
py-randforest-env312\Scripts\activate     # (Windows)
```
5. Install semua library yang dibutuhkan dengan menjalankan perintah berikut:
```bash
pip install -r requirements.txt
```

## Penggunanaan
1. Jalankan aplikasi dengan perintah berikut di terminal:
```bash
streamlit run app.py
```
2. Buka browser dan akses aplikasi di http://localhost:8501/.
3. Isi form yang disediakan.
4. Klik tombol "Prediksi" untuk memulai proses prediksi.

## Lisensi
Proyek ini menggunakan lisensi MIT License. Anda bebas untuk menggunakan, memodifikasi, dan mendistribusikan ulang proyek ini sesuai dengan ketentuan lisensi.