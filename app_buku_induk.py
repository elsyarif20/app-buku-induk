import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import google.generativeai as genai
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# --- A. KONFIGURASI API & DATABASE ---
# Masukkan API Key Gemini Anda di sini
GENIMINI_API_KEY = "ISI_DENGAN_API_KEY_KAMU" 
genai.configure(api_key=GENIMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inisialisasi Firebase (Gunakan Secrets di Streamlit Cloud untuk keamanan)
if not firebase_admin._apps:
    try:
        # Untuk lokal, pakai file key.json. Untuk Cloud, gunakan st.secrets
        if "firebase" in st.secrets:
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
        else:
            cred = credentials.Certificate('key.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Koneksi Database Gagal: {e}")

db = firestore.client() if firebase_admin._apps else None

# --- B. UI SETUP ---
st.set_page_config(page_title="SI-GHOZALI Web", layout="wide", page_icon="🏫")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- C. SIDEBAR NAVIGATION ---
st.sidebar.image("https://via.placeholder.com/150?text=AL-GHOZALI", width=100)
st.sidebar.title("SI-GHOZALI V3.0")
menu = st.sidebar.radio("Navigasi", ["📊 Dashboard", "📝 Input Siswa", "👥 Data Induk", "🤖 AI Rapor Assistant"])

# --- D. FITUR: DASHBOARD ---
if menu == "📊 Dashboard":
    st.title("Pusat Data Pendidikan Al-Ghozali")
    st.write(f"Selamat datang, **Bapak Liyas Syarifudin** (Head of Quality Development)")
    
    col1, col2, col3 = st.columns(3)
    # Simulasi hitung data (Nanti bisa pakai len(df))
    col1.metric("Total Siswa", "20", "+2")
    col2.metric("Total Guru", "1", "0")
    col3.metric("Tahun Ajaran", "2023/2024", "Aktif")

    st.divider()
    st.info("💡 Gunakan menu di samping untuk mengelola data siswa secara real-time.")

# --- E. FITUR: INPUT SISWA ---
elif menu == "📝 Input Siswa":
    st.subheader("Registrasi Siswa Baru")
    with st.form("form_input", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nisn = st.text_input("NISN")
            nama = st.text_input("Nama Lengkap")
            jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
        with c2:
            kelas = st.selectbox("Unit / Kelas", ["X DKV 1", "X DKV 2", "XI DKV", "XII DKV"])
            ayah = st.text_input("Nama Orang Tua/Wali")
            alamat = st.text_area("Alamat")
        
        btn_save = st.form_submit_button("Simpan Data ke Cloud")
        
        if btn_save:
            if db and nisn and nama:
                db.collection('siswa').document(nisn).set({
                    'nisn': nisn, 'nama': nama, 'jk': jk, 
                    'kelas': kelas, 'ayah': ayah, 'alamat': alamat
                })
                st.success(f"Berhasil! Data {nama} sudah tersimpan di Firebase.")
            else:
                st.warning("Mohon lengkapi data dan pastikan Database aktif.")

# --- F. FITUR: DATA INDUK & EKSPOR ---
elif menu == "👥 Data Induk":
    st.subheader("Tabel Induk Siswa Terintegrasi")
    if db:
        docs = db.collection('siswa').stream()
        list_data = [doc.to_dict() for doc in docs]
        
        if list_data:
            df = pd.DataFrame(list_data)
            st.dataframe(df, use_container_width=True)
            
            # Fitur Cetak Kartu Ujian Sederhana
            pilih_siswa = st.selectbox("Pilih Siswa untuk Cetak Kartu", df['nama'].tolist())
            if st.button("🖨️ Generate Kartu PDF"):
                siswa = df[df['nama'] == pilih_siswa].iloc[0]
                buf = io.BytesIO()
                c = canvas.Canvas(buf, pagesize=(300, 200))
                c.rect(10, 10, 280, 180)
                c.drawCentredString(150, 170, "KARTU PESERTA UJIAN")
                c.drawString(30, 130, f"Nama : {siswa['nama']}")
                c.drawString(30, 110, f"NISN : {siswa['nisn']}")
                c.drawString(30, 90, f"Kelas: {siswa['kelas']}")
                c.save()
                st.download_button("Download Kartu", buf.getvalue(), f"Kartu_{siswa['nisn']}.pdf")
        else:
            st.write("Belum ada data di cloud.")

# --- G. FITUR: AI RAPOR ASSISTANT ---
elif menu == "🤖 AI Rapor Assistant":
    st.subheader("Asisten Penulisan Deskripsi Rapor (Gemini AI)")
    nama_s = st.text_input("Nama Siswa")
    proyek = st.text_input("Nama Proyek P5", "Kebersihan Lingkungan")
    capaian = st.select_slider("Tingkat Capaian", ["Mulai Berkembang", "Sedang Berkembang", "Berkembang Sesuai Harapan", "Sangat Berkembang"])
    
    if st.button("Generate Narasi Rapor"):
        with st.spinner("AI sedang berpikir..."):
            prompt = f"Buat deskripsi rapor P5 untuk siswa bernama {nama_s}. Proyek: {proyek}. Capaian: {capaian}. Gunakan bahasa yang edukatif dan memotivasi untuk Kurikulum Merdeka."
            response = model.generate_content(prompt)
            st.write("### Rekomendasi Narasi:")
            st.info(response.text)
