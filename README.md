# 🏫 SI-GHOZALI: Sistem Informasi Buku Induk & Rapor Digital

**SI-GHOZALI** adalah aplikasi manajemen data siswa modern yang dirancang khusus untuk ekosistem pendidikan di **Pondok Modern Al-Ghozali**. Aplikasi ini mengintegrasikan pendataan administratif dengan teknologi AI untuk mempermudah tugas guru dan meningkatkan kualitas data sekolah.

---

## ✨ Fitur Unggulan

* **🗂️ Modul Data Induk:** Pengelolaan data siswa lengkap (NISN, NIK, Riwayat Keluarga, hingga Foto).
* **📊 Dashboard Statistik:** Visualisasi jumlah siswa, guru, dan alumni secara real-time.
* **📄 Rapor Kurikulum Merdeka (P5):** Pembuatan Rapor Projek Penguatan Profil Pelajar Pancasila secara otomatis dalam format PDF.
* **🪪 Kartu Ujian Otomatis:** Cetak kartu peserta ujian secara massal hanya dengan satu klik.
* **🤖 AI Assistant (Gemini API):** Membantu guru menghasilkan deskripsi capaian kompetensi siswa secara otomatis dan objektif.
* **☁️ Cloud Sync (Firebase):** Data tersimpan aman di cloud, memungkinkan sinkronisasi antar unit SMP dan SMA.

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Teknologi |
| :--- | :--- |
| **Language** | Python 3.12 |
| **GUI Framework** | PySide6 (Qt for Python) / Streamlit (Web) |
| **Database** | SQLite (Local) & Firebase Firestore (Cloud) |
| **PDF Engine** | ReportLab |
| **Data Processing** | Pandas & Openpyxl |
| **AI Integration** | Google Gemini Pro API |

---

## 🚀 Cara Instalasi (Pengembang)

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/username-kamu/app-buku-induk.git](https://github.com/username-kamu/app-buku-induk.git)
    cd app-buku-induk
    ```

2.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Aplikasi:**
    ```bash
    python app_buku_induk.py
    ```

---

## 📦 Distribusi (Pengguna Akhir)

Untuk pengguna yang tidak memiliki Python, silakan unduh file eksekusi (`.exe`) langsung dari menu **[Releases]** di repository ini.

---

## 👨‍💻 Kontributor

* **Liyas Syarifudin, S.Pd.I, M.Pd (El-Syarif)** - *Lead Developer & Head of Education Quality Development PM Al-Ghozali*

---

> *"Digitalisasi pendidikan bukan hanya tentang alat, tapi tentang efisiensi untuk kemaslahatan santri."*