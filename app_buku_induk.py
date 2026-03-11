import sys
import sqlite3
import os
import pandas as pd
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QTabWidget, QFileDialog, QMessageBox, 
                             QFrame, QLineEdit, QComboBox, QDateEdit, QFormLayout, 
                             QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt, QDate, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon

# Import untuk PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --- DATABASE ENGINE ---
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("master_sekolah.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Tabel Siswa Lengkap
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nisn TEXT UNIQUE, 
            nama TEXT, 
            jk TEXT, 
            tempat_lahir TEXT, 
            tgl_lahir TEXT, 
            agama TEXT, 
            alamat TEXT, 
            foto_path TEXT,
            nama_ayah TEXT, 
            pekerjaan_ayah TEXT, 
            nama_ibu TEXT, 
            kelas_sekarang TEXT, 
            status_akademik TEXT)''')
        self.conn.commit()

# --- MAIN APPLICATION WINDOW ---
class BukuIndukUltimate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.foto_sementara = ""
        
        self.setWindowTitle("SI-GHOZALI: Sistem Buku Induk & Rapor Digital V3.0")
        self.resize(1280, 800)
        self.setStyleSheet("background-color: #f5f6fa;")

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)

        # 1. HEADER PANEL
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #2f3640; border-radius: 0px;")
        h_layout = QHBoxLayout(header)
        
        lbl_title = QLabel("🏫 SMK ISLAM AL-GHOZALI | DASHBOARD ADMINISTRASI")
        lbl_title.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        h_layout.addWidget(lbl_title)
        h_layout.addStretch()
        
        self.main_layout.addWidget(header)

        # 2. TAB UTAMA
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { height: 40px; width: 200px; font-weight: bold; }")
        
        # Inisialisasi Tab
        self.tab_dashboard = QWidget()
        self.tab_data_siswa = QWidget()
        
        self.tabs.addTab(self.tab_dashboard, "📊 DASHBOARD")
        self.tabs.addTab(self.tab_data_siswa, "👥 DATA INDUK SISWA")
        
        self.setup_dashboard_tab()
        self.setup_siswa_tab()
        
        self.main_layout.addWidget(self.tabs)

    # --- TAB 1: DASHBOARD ---
    def setup_dashboard_tab(self):
        layout = QVBoxLayout(self.tab_dashboard)
        
        stats_layout = QHBoxLayout()
        stats_layout.addWidget(self.create_card("TOTAL SISWA", "20", "#e17055"))
        stats_layout.addWidget(self.create_card("ALUMNI", "0", "#0984e3"))
        stats_layout.addWidget(self.create_card("GURU & STAF", "1", "#00b894"))
        
        layout.addLayout(stats_layout)
        
        info_box = QFrame()
        info_box.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #ddd;")
        ib_layout = QVBoxLayout(info_box)
        ib_layout.addWidget(QLabel("Selamat Datang di Sistem Informasi Sekolah"))
        ib_layout.addWidget(QLabel("Gunakan Tab 'Data Induk Siswa' untuk mengelola data, cetak rapor, dan kartu ujian."))
        
        layout.addWidget(info_box)
        layout.addStretch()

    def create_card(self, title, value, color):
        card = QFrame()
        card.setMinimumHeight(150)
        card.setStyleSheet(f"background-color: {color}; border-radius: 15px; color: white;")
        l = QVBoxLayout(card)
        t = QLabel(title); t.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        v = QLabel(value); v.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addWidget(t); l.addWidget(v)
        return card

    # --- TAB 2: DATA SISWA ---
    def setup_siswa_tab(self):
        main_layout = QHBoxLayout(self.tab_data_siswa)
        
        # Sisi Kiri: Form Input
        form_container = QFrame()
        form_container.setFixedWidth(400)
        form_container.setStyleSheet("background-color: white; border-radius: 10px;")
        left_layout = QVBoxLayout(form_container)
        
        lbl_form = QLabel("INPUT DATA SISWA BARU")
        lbl_form.setStyleSheet("font-weight: bold; color: #2f3640;")
        left_layout.addWidget(lbl_form)

        # Form Scrollable jika field banyak
        self.input_form = QFormLayout()
        
        self.in_nisn = QLineEdit()
        self.in_nama = QLineEdit()
        self.in_jk = QComboBox(); self.in_jk.addItems(["Laki-Laki", "Perempuan"])
        self.in_tempat = QLineEdit()
        self.in_tgl = QDateEdit(); self.in_tgl.setCalendarPopup(True); self.in_tgl.setDate(QDate.currentDate())
        self.in_alamat = QLineEdit()
        self.in_ayah = QLineEdit()
        self.in_kelas = QComboBox(); self.in_kelas.addItems(["X DKV 1", "X DKV 2", "XI DKV", "XII DKV"])
        
        self.input_form.addRow("NISN:", self.in_nisn)
        self.input_form.addRow("Nama Lengkap:", self.in_nama)
        self.input_form.addRow("Jenis Kelamin:", self.in_jk)
        self.input_form.addRow("Tempat Lahir:", self.in_tempat)
        self.input_form.addRow("Tanggal Lahir:", self.in_tgl)
        self.input_form.addRow("Alamat:", self.in_alamat)
        self.input_form.addRow("Nama Ayah:", self.in_ayah)
        self.input_form.addRow("Kelas:", self.in_kelas)

        # Preview Foto
        self.lbl_foto = QLabel("FOTO 3x4")
        self.lbl_foto.setFixedSize(100, 130)
        self.lbl_foto.setStyleSheet("border: 2px dashed #ccc; background: #f9f9f9;")
        self.lbl_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        btn_foto = QPushButton("Pilih Foto")
        btn_foto.clicked.connect(self.pilih_foto)
        
        left_layout.addLayout(self.input_form)
        left_layout.addWidget(self.lbl_foto, alignment=Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(btn_foto)
        
        btn_simpan = QPushButton("💾 SIMPAN DATA SISWA")
        btn_simpan.setFixedHeight(40)
        btn_simpan.setStyleSheet("background-color: #00b894; color: white; font-weight: bold;")
        btn_simpan.clicked.connect(self.simpan_siswa)
        left_layout.addWidget(btn_simpan)

        # Sisi Kanan: Tabel Data
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        
        # Toolbar Atas Tabel
        toolbar = QHBoxLayout()
        self.in_cari = QLineEdit(); self.in_cari.setPlaceholderText("Cari Nama atau NISN...")
        btn_cari = QPushButton("Cari"); btn_cari.clicked.connect(self.load_data_table)
        
        toolbar.addWidget(self.in_cari)
        toolbar.addWidget(btn_cari)
        right_layout.addLayout(toolbar)

        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["NISN", "NAMA", "JK", "KELAS", "AYAH", "STATUS"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.table)

        # Panel Tombol Aksi Bawah
        aksi_layout = QHBoxLayout()
        btn_xls = QPushButton("📗 Export Excel"); btn_xls.clicked.connect(self.export_excel)
        btn_p5 = QPushButton("📄 Cetak Rapor P5"); btn_p5.clicked.connect(self.cetak_rapor_pdf)
        btn_kartu = QPushButton("🪪 Cetak Kartu Ujian"); btn_kartu.clicked.connect(self.cetak_kartu_pdf)
        btn_naik = QPushButton("📈 Naik Kelas"); btn_naik.setStyleSheet("background-color: #fab1a0;"); btn_naik.clicked.connect(self.naik_kelas)
        
        aksi_layout.addWidget(btn_xls)
        aksi_layout.addWidget(btn_p5)
        aksi_layout.addWidget(btn_kartu)
        aksi_layout.addWidget(btn_naik)
        right_layout.addLayout(aksi_layout)

        main_layout.addWidget(form_container)
        main_layout.addWidget(right_panel)
        
        self.load_data_table()

    # --- LOGIKA FITUR ---

    def pilih_foto(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Foto", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.foto_sementara = file_path
            pix = QPixmap(file_path).scaled(100, 130, Qt.AspectRatioMode.KeepAspectRatio)
            self.lbl_foto.setPixmap(pix)

    def simpan_siswa(self):
        data = (
            self.in_nisn.text(), self.in_nama.text(), self.in_jk.currentText(),
            self.in_tempat.text(), self.in_tgl.date().toString("dd-MM-yyyy"),
            self.in_alamat.text(), self.foto_sementara, self.in_ayah.text(),
            self.in_kelas.currentText(), "Aktif"
        )
        
        if not data[0] or not data[1]:
            QMessageBox.warning(self, "Input Error", "NISN dan Nama harus diisi!")
            return

        try:
            self.db.cursor.execute('''INSERT OR REPLACE INTO siswa 
                (nisn, nama, jk, tempat_lahir, tgl_lahir, alamat, foto_path, nama_ayah, kelas_sekarang, status_akademik)
                VALUES (?,?,?,?,?,?,?,?,?,?)''', data)
            self.db.conn.commit()
            QMessageBox.information(self, "Sukses", "Data siswa berhasil disimpan!")
            self.load_data_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def load_data_table(self):
        cari = self.in_cari.text()
        query = "SELECT nisn, nama, jk, kelas_sekarang, nama_ayah, status_akademik FROM siswa"
        if cari:
            query += f" WHERE nama LIKE '%{cari}%' OR nisn LIKE '%{cari}%'"
        
        df = pd.read_sql_query(query, self.db.conn)
        self.table.setRowCount(len(df))
        for i, row in df.iterrows():
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def export_excel(self):
        df = pd.read_sql_query("SELECT * FROM siswa", self.db.conn)
        path, _ = QFileDialog.getSaveFileName(self, "Simpan Excel", "", "Excel Files (*.xlsx)")
        if path:
            df.to_excel(path, index=False)
            QMessageBox.information(self, "Sukses", "Data berhasil diekspor!")

    def cetak_rapor_pdf(self):
        row = self.table.currentRow()
        if row < 0: return
        
        nisn = self.table.item(row, 0).text()
        nama = self.table.item(row, 1).text()
        kelas = self.table.item(row, 3).text()

        doc = SimpleDocTemplate(f"Rapor_P5_{nama}.pdf", pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"<b>RAPOR PROJEK PENGUATAN PROFIL PELAJAR PANCASILA</b>", styles['Title']))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Nama Siswa: {nama} | NISN: {nisn} | Kelas: {kelas}", styles['Normal']))
        elements.append(Spacer(1, 10))

        data = [
            ['Komponen Proyek', 'Capaian', 'Catatan'],
            ['1. Kebersihan Lingkungan', 'Sangat Berkembang', 'Aktif dalam gotong royong'],
            ['2. Suara Demokrasi', 'Berkembang', 'Berani mengutarakan pendapat'],
            ['3. Kewirausahaan', 'Berkembang', 'Kreatif dalam membuat produk']
        ]
        
        t = Table(data, colWidths=[200, 100, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('PADDING', (0,0), (-1,-1), 10)
        ]))
        elements.append(t)
        doc.build(elements)
        QMessageBox.information(self, "Sukses", f"Rapor PDF {nama} berhasil dicetak!")

    def cetak_kartu_pdf(self):
        row = self.table.currentRow()
        if row < 0: return
        
        nisn = self.table.item(row, 0).text()
        nama = self.table.item(row, 1).text()
        kelas = self.table.item(row, 3).text()

        c = canvas.Canvas(f"Kartu_Ujian_{nisn}.pdf", pagesize=(300, 200))
        c.rect(5, 5, 290, 190)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(150, 175, "KARTU PESERTA UJIAN SMK AL-GHOZALI")
        c.line(10, 165, 290, 165)
        
        c.setFont("Helvetica", 9)
        c.drawString(20, 140, f"Nama  : {nama}")
        c.drawString(20, 125, f"NISN  : {nisn}")
        c.drawString(20, 110, f"Kelas : {kelas}")
        
        c.rect(220, 100, 50, 60) # Frame Foto
        c.setFont("Helvetica", 6)
        c.drawCentredString(245, 125, "FOTO 2x3")
        
        c.save()
        QMessageBox.information(self, "Sukses", "Kartu ujian telah dibuat.")

    def naik_kelas(self):
        row = self.table.currentRow()
        if row < 0: return
        
        nisn = self.table.item(row, 0).text()
        nama = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(self, "Konfirmasi", f"Naikkan kelas ananda {nama}?", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.db.cursor.execute("UPDATE siswa SET kelas_sekarang = 'XI DKV' WHERE nisn = ?", (nisn,))
            self.db.conn.commit()
            self.load_data_table()
            QMessageBox.information(self, "Sukses", "Status kelas berhasil diupdate!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set Tema Fusion agar terlihat modern di Windows
    app.setStyle("Fusion")
    window = BukuIndukUltimate()
    window.show()
    sys.exit(app.exec())