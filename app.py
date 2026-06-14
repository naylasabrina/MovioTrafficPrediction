import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# ==========================================
# 1. PENGATURAN HALAMAN & KONFIGURASI
# ==========================================
st.set_page_config(
    page_title="Movio - Traffic Prediction App",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inisialisasi Session State (PENTING untuk History & Navigasi)
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

if 'history_manual' not in st.session_state:
    st.session_state.history_manual = []

if 'history_csv' not in st.session_state:
    st.session_state.history_csv = []

# ==========================================
# 2. CUSTOM CSS FIXED TOTAL (ANTI BLANK PUTIH)
# ==========================================
st.markdown("""
    <style>
    /* Sembunyikan Sidebar Asli */
    [data-testid="stSidebarCollapseButton"], [data-testid="stSidebar"] {
        display: none !important;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Background Utama Aplikasi */
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15103c 40%, #0b1136 100%);
        color: #f3f4f6;
    }
    
    /* Navbar Container */
    .nav-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .brand-title {
        background: linear-gradient(90deg, #c084fc 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
    }
    
    /* Banner Selamat Datang */
    .welcome-banner {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 50%, #2563eb 100%);
        padding: 40px;
        border-radius: 16px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .welcome-banner h1 {
        font-weight: 800;
        margin-bottom: 15px;
        color: white !important;
    }
    
    /* Perbaikan Jarak Judul ke Konten & Antar Section */
    .sub-title {
        color: #f3f4f6;
        font-weight: 700;
        margin-top: 50px !important;    
        margin-bottom: 25px !important; 
        border-left: 4px solid #c084fc;
        padding-left: 12px;
    }

    /* HTML Grid Card Dashboard Sama Tinggi */
    .dashboard-grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 25px;
        margin-bottom: 25px;
    }
    .dashboard-grid-2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 25px;
        margin-bottom: 25px;
    }
    .feature-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 30px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 100%; 
    }
    .feature-card h4 {
        color: #c084fc !important;
        margin-top: 0;
        font-weight: 700;
        margin-bottom: 15px;
    }
    .feature-card p {
        color: #cbd5e1 !important;
        font-size: 14px;
        line-height: 1.7;
        margin: 0;
    }
    .use-card {
        border-left: 4px solid #6366f1;
        background: rgba(99, 102, 241, 0.05);
    }
    
    /* Box Hasil Prediksi */
    .result-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        color: white;
        margin-top: 25px;
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.3);
    }
    .bg-heavy { background: linear-gradient(90deg, #dc2626, #ef4444); }
    .bg-high { background: linear-gradient(90deg, #ea580c, #f97316); }
    .bg-normal { background: linear-gradient(90deg, #2563eb, #3b82f6); }
    .bg-low { background: linear-gradient(90deg, #16a34a, #10b981); }

    /* Teks Global Form & Dropdown */
    label, p, span, .stMetric {
        color: #f3f4f6 !important;
    }

    /* =======================================================
       FILE UPLOADER & TEKS KECIL POJOK KANAN
       ======================================================= */
    div[data-testid="stFileUploader"] section {
        background-color: rgba(255, 255, 255, 0.03) !important;
        background-image: none !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    div[data-testid="stFileUploader"] *, 
    div[data-testid="stFileUploaderDropzoneInstructions"] *,
    div[data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #cbd5e1 !important;
    }
    
    div[data-testid="stFileUploader"] button {
        background-color: #1e1b4b !important;
        color: #f3f4f6 !important;
        border: 1px solid #4338ca !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #2e2a72 !important;
        border-color: #c084fc !important;
        color: #ffffff !important;
    }

    /* =======================================================
       PERBAIKAN REDESIGN TOTAL TOMBOL NAVIGASI
       ======================================================= */
    div.stButton > button[kind="secondary"] {
        background-color: #1e1b4b !important;
        color: #f3f4f6 !important;
        border: 1px solid #4338ca !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #2e2a72 !important;
        border-color: #c084fc !important;
        color: #ffffff !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #7c3aed 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #9061f9 0%, #6366f1 100%) !important;
        color: #ffffff !important;
    }

    div.stFormSubmitButton > button,
    div.stDownloadButton > button,
    div.stButton > button[key*="btn_utama_aksi"] {
        background: linear-gradient(90deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
        width: 100% !important;
        display: block !important;
    }
    
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover,
    div.stButton > button[key*="btn_utama_aksi"]:hover {
        background: linear-gradient(90deg, #c084fc 0%, #818cf8 50%, #60a5fa 100%) !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.6) !important;
        transform: translateY(-2px);
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. FUNGSI LOAD MODEL & PREDIKSI
# ==========================================
@st.cache_resource
def load_all_models():
    models = {
        'Decision Tree': joblib.load('dt_modelJb_DT-HPO.joblib'),
        'k-NN': joblib.load('knn_modelJb_KNN-HPO.joblib'),
        'SVM': joblib.load('svm_modelJb_SVM-HPO.joblib')
    }
    freq_encoders = {
        'Decision Tree': joblib.load('dt_day_freq.joblib'),
        'k-NN': joblib.load('knn_day_freq.joblib'),
        'SVM': joblib.load('svm_day_freq.joblib')
    }
    scalers = {
        'k-NN': joblib.load('knn_scaler.joblib'),
        'SVM': joblib.load('knn_scaler.joblib')
    }
    return models, freq_encoders, scalers

try:
    models, freq_encoders, scalers = load_all_models()
except Exception as e:
    st.error(f"⚠️ Gagal memuat file .joblib: {e}")

def execute_prediction(df_raw, model_name):
    df_processed = df_raw.copy()
    
    # 1. Pastikan 'Hour' sudah ada
    if 'Hour' not in df_processed.columns:
        if 'Time' in df_processed.columns:
            df_processed['Time'] = df_processed['Time'].astype(str).str.strip()
            try:
                df_processed['Hour'] = pd.to_datetime(df_processed['Time'], format='%I:%M:%S %p').dt.hour
            except Exception:
                try:
                    df_processed['Hour'] = pd.to_datetime(df_processed['Time'], format='%H:%M:%S').dt.hour
                except Exception:
                    try:
                        df_processed['Hour'] = df_processed['Time'].str.split(':').str[0].astype(int)
                    except Exception:
                        df_processed['Hour'] = 12
        else:
            df_processed['Hour'] = 12

    # 2. Lakukan Encoding Hari (Sesuai dengan kolom yang dibaca model)
    day_mapping = freq_encoders[model_name]
    df_processed['Day of the week_freq_encode'] = df_processed['Day of the week'].map(day_mapping).fillna(0)
    
    # 3. URUTAN KOLOM FIX (PENTING: Harus sama persis dengan saat training model)
    features_ordered = [
        'CarCount', 
        'BikeCount', 
        'BusCount', 
        'TruckCount', 
        'Total', 
        'Day of the week_freq_encode', 
        'Hour'
    ]
    
    # Pilih hanya kolom yang diperlukan dan urutkan
    df_features = df_processed[features_ordered].copy()
    
    # 4. Konversi ke Numpy Array
    X_input = df_features.values
    
    # 5. Scaling (Wajib untuk k-NN dan SVM)
    if model_name in ['k-NN', 'SVM']:
        scaler = scalers[model_name]
        X_input = scaler.transform(X_input)
    
    # 6. Prediksi
    model = models[model_name]
    predictions = model.predict(X_input)
    
    return predictions

# ==========================================
# 4. NAVBAR MENU ATAS
# ==========================================
st.markdown("""
    <div class="nav-container">
        <div class="brand-title">🚦 MOVIO PROJECT</div>
        <div style="color: #94a3b8; font-size: 14px; font-weight: 500;">Sistem Prediksi Kepadatan Lalu Lintas</div>
    </div>
""", unsafe_allow_html=True)

menu_cols = st.columns(4)
with menu_cols[0]:
    if st.button("🏠 Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
        st.session_state.current_page = "Dashboard"
        st.rerun()
with menu_cols[1]:
    if st.button("🛠️ Input Manual", use_container_width=True, type="primary" if st.session_state.current_page == "Input Manual" else "secondary"):
        st.session_state.current_page = "Input Manual"
        st.rerun()
with menu_cols[2]:
    if st.button("📁 Input CSV", use_container_width=True, type="primary" if st.session_state.current_page == "Input CSV" else "secondary"):
        st.session_state.current_page = "Input CSV"
        st.rerun()
with menu_cols[3]:
    if st.button("📜 History Predict", use_container_width=True, type="primary" if st.session_state.current_page == "History Predict" else "secondary"):
        st.session_state.current_page = "History Predict"
        st.rerun()

st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin-top:0;'>", unsafe_allow_html=True)

# ==========================================
# 5. RENDER HALAMAN BERDASARKAN STATE
# ==========================================

# --- HALAMAN DASHBOARD ---
if st.session_state.current_page == "Dashboard":
    st.markdown("""
        <div class='welcome-banner'>
            <h1>Selamat Datang di Aplikasi Movio!</h1>
            <p>
                Movio adalah platform analisis cerdas berbasis Machine Learning yang dirancang khusus untuk memetakan, 
                menganalisis, dan memprediksi dinamika kondisi lalu lintas perkotaan demi mendukung efisiensi sistem transportasi jalan raya.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 class='sub-title'>⚙️ Apa yang Aplikasi Ini Lakukan?</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div class='dashboard-grid-3'>
            <div class='feature-card'>
                <h4>🚦 Prediksi Kondisi Lalu Lintas</h4>
                <p>Memprediksi tingkat kepadatan lalu lintas berdasarkan volume kendaraan dan secara otomatis mengklasifikasikannya ke dalam kategori <b>Low, Normal, High, atau Heavy</b>.</p>
            </div>
            <div class='feature-card'>
                <h4>📊 Analisis Data Kendaraan</h4>
                <p>Sistem menganalisis beberapa parameter input untuk memahami pola lalu lintas, yaitu <b>CarCount</b> (jumlah mobil), <b>BikeCount</b> (jumlah motor), <b>BusCount</b> (jumlah bus), <b>TruckCount</b> (jumlah truk), <b>Day</b> (hari), dan <b>Hour</b> (jam pengamatan).</p>
            </div>
            <div class='feature-card'>
                <h4>🤖 Prediksi 3 Model ML</h4>
                <p>Menggunakan algoritma <b>SVM, KNN, dan Decision Tree</b> untuk menghasilkan prediksi kondisi lalu lintas serta membandingkan performa model terbaik secara real-time.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
        
    st.markdown("<h3 class='sub-title'>📊 Informasi Karakteristik Dataset</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div class='dashboard-grid-3'>
            <div class='feature-card'>
                <h4 style='color: #34d399 !important;'>📈 Volume & Struktur</h4>
                <p><b>📊 Total Data</b> : 2.976 Records<br><b>📈 Jumlah Fitur</b> : 7 Features</p>
            </div>
            <div class='feature-card'>
                <h4 style='color: #34d399 !important;'>🎯 Target Output Kelas</h4>
                <p><b>🎯 Kelas Prediksi</b> : Low, Normal, High, Heavy</p>
            </div>
            <div class='feature-card'>
                <h4 style='color: #34d399 !important;'>🧠 Arsitektur Model</h4>
                <p><b>🧠 Model Digunakan</b> : SVM, KNN, Decision Tree</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 class='sub-title'>🚀 Panduan Cara Penggunaan</h3>", unsafe_allow_html=True)
    st.markdown("""
        <div class='dashboard-grid-2'>
            <div class='feature-card use-card'>
                <h4>🛠️ Manual Prediction</h4>
               <ol style="color: #cbd5e1 !important; font-size: 14px; line-height: 1.7; margin: 0; padding-left: 20px;">
                    <li>Isi data kendaraan yang tersedia</li>
                    <li>Tentukan hari dan jam</li>
                    <li>Pilih model yang ingin digunakan</li>
                    <li>Klik Prediksi untuk melihat hasil</li>
                </ol>
            </div>
            <div class='feature-card use-card'>
                <h4>📁 CSV Prediction</h4>
               <ol style="color: #cbd5e1 !important; font-size: 14px; line-height: 1.7; margin: 0; padding-left: 20px;">
                    <li>Siapkan file data CSV</li>
                    <li>Upload file ke sistem</li>
                    <li>Jalankan prediksi otomatis</li>
                    <li>Download hasil prediksi</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- HALAMAN INPUT MANUAL ---
elif st.session_state.current_page == "Input Manual":
    st.markdown("<h2 class='sub-title'>🛠️ Klasifikasi via Input Manual</h2>", unsafe_allow_html=True)
    
    # Menghapus st.columns agar input tersusun ke bawah (vertikal)
    cars = st.number_input("Jumlah Mobil (CarCount)", min_value=0, value=0)
    bikes = st.number_input("Jumlah Motor (BikeCount)", min_value=0, value=0)
    buses = st.number_input("Jumlah Bus (BusCount)", min_value=0, value=0)
    trucks = st.number_input("Jumlah Truk (TruckCount)", min_value=0, value=0)
        
    # Perhitungan Total Real-time
    total_v = cars + bikes + buses + trucks
    st.metric(label="Total Akumulasi Kendaraan (Otomatis)", value=total_v)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Input waktu dan model juga disusun ke bawah
    hari = st.selectbox("Pilih Hari", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    jam = st.slider("Pilih Jam (Hour)", 0, 23, 0)
    model_pilihan = st.selectbox("Pilih Model Algoritma", ["Decision Tree", "k-NN", "SVM"])
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tombol aksi tanpa st.form
    btn_prediksi = st.button("Lakukan Prediksi", key="btn_utama_aksi_manual")
        
    if btn_prediksi:
        df_manual = pd.DataFrame([{
            'CarCount': cars, 
            'BikeCount': bikes, 
            'BusCount': buses, 
            'TruckCount': trucks, 
            'Total': total_v, 
            'Day of the week': hari, 
            'Hour': jam
        }])
        
        hasil = execute_prediction(df_manual, model_pilihan)[0]
        hasil_str = str(hasil).lower().strip()
        
        st.session_state.history_manual.append({
            'Waktu Aktivitas': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Model Dipakai': model_pilihan,
            'Ringkasan Data': f"Mobil: {cars}, Motor: {bikes}, Bus: {buses}, Truk: {trucks} (Total: {total_v}) pada Jam {jam} ({hari})",
            'Hasil Prediksi': hasil_str.upper()
        })
        
        st.markdown("### 🎯 Hasil Prediksi Kondisi Jalan:")
        if hasil_str == 'heavy':
            st.markdown("<div class='result-box bg-heavy'>⚠️ HEAVY </div>", unsafe_allow_html=True)
        elif hasil_str == 'high':
            st.markdown("<div class='result-box bg-high'>🟠 HIGH </div>", unsafe_allow_html=True)
        elif hasil_str == 'normal':
            st.markdown("<div class='result-box bg-normal'>🔵 NORMAL </div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box bg-low'>🟢 LOW </div>", unsafe_allow_html=True)

# --- HALAMAN INPUT CSV (PISAH DATASET & PREDIKSI) ---
elif st.session_state.current_page == "Input CSV":
    st.markdown("<h2 class='sub-title'>📁 Batch Prediction Via File CSV</h2>", unsafe_allow_html=True)
    
    model_csv = st.selectbox("Pilih Konfigurasi Arsitektur ML", ["Decision Tree", "k-NN", "SVM"])
    file_unggahan = st.file_uploader("Unggah File CSV Anda", type=["csv"])
    
    if file_unggahan is not None:
        try:
            df_csv = pd.read_csv(file_unggahan)
            st.success("Berkas berhasil dimuat!")
            
            # --- SEKSI 1: HANYA DATASET INPUT ASLI ---
            st.markdown("### 📄 Preview Dataset Input Asli")
            st.dataframe(df_csv.head(5), use_container_width=True)
            
            if st.button("Jalankan Batch Prediction", key="btn_utama_aksi_csv"):
                with st.spinner("Model sedang memproses data..."):
                    # Eksekusi kalkulasi prediksi
                    pred_list = execute_prediction(df_csv, model_csv)
                    
                    # --- SEKSI 2: HANYA HASIL PREDIKSI YANG DIPISAH ---
                    st.markdown("### 🏆 Hasil Analisis Prediksi")
                    df_hasil_saja = pd.DataFrame({
                        'Traffic_Situation_Prediction': pred_list
                    })
                    st.dataframe(df_hasil_saja, use_container_width=True)
                    
                    # File unduhan gabungan tetap disediakan agar komplit bagi user
                    df_gabungan = df_csv.copy()
                    df_gabungan['Traffic_Situation_Prediction'] = pred_list
                    csv_bytes = df_gabungan.to_csv(index=False).encode('utf-8')
                    
                    st.download_button(
                        label="📥 Download Hasil Prediksi Lengkap (.CSV)",
                        data=csv_bytes,
                        file_name=f"movio_prediction_{model_csv.lower()}.csv",
                        mime="text/csv"
                    )
                    
                    st.session_state.history_csv.append({
                        'Waktu Aktivitas': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'Model Dipakai': model_csv,
                        'Nama File': file_unggahan.name,
                        'Jumlah Baris': f"{len(df_csv)} Baris Data",
                        'Status': "Sukses Terprediksi"
                    })
        except Exception as kegagalan:
            st.error(f"Error pembacaan berkas atau kolom tidak sesuai: {kegagalan}")

# --- HALAMAN HISTORY PREDICT ---
elif st.session_state.current_page == "History Predict":
    st.markdown("<h2 class='sub-title'>📜 Catatan Riwayat Prediksi</h2>", unsafe_allow_html=True)
    
    tab_manual, tab_csv = st.tabs(["🛠️ Riwayat Input Manual", "📁 Riwayat Batch File CSV"])
    
    with tab_manual:
        if len(st.session_state.history_manual) > 0:
            df_m = pd.DataFrame(st.session_state.history_manual)
            st.dataframe(df_m.sort_values(by="Waktu Aktivitas", ascending=False), use_container_width=True)
            if st.button("🗑️ Bersihkan Riwayat Manual", key="btn_utama_aksi_del_m"):
                st.session_state.history_manual = []
                st.rerun()
        else:
            st.info("Belum ada riwayat dari input manual.")
            
    with tab_csv:
        if len(st.session_state.history_csv) > 0:
            df_c = pd.DataFrame(st.session_state.history_csv)
            st.dataframe(df_c.sort_values(by="Waktu Aktivitas", ascending=False), use_container_width=True)
            if st.button("🗑️ Bersihkan Riwayat CSV", key="btn_utama_aksi_del_c"):
                st.session_state.history_csv = []
                st.rerun()
        else:
            st.info("Belum ada riwayat dari unggahan file CSV.")