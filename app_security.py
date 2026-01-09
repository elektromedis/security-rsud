import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Security RSUD Cipayung", layout="wide")

# --- FUNGSI BANTUAN (LOGIKA) ---

# Fungsi untuk menyimpan data ke file CSV (Supaya data tidak hilang saat direfresh)
def simpan_data(data_baru, nama_file):
    if not os.path.isfile(nama_file):
        df = pd.DataFrame(data_baru)
        df.to_csv(nama_file, index=False)
    else:
        df = pd.read_csv(nama_file)
        df_baru = pd.DataFrame(data_baru)
        df = pd.concat([df, df_baru], ignore_index=True)
        df.to_csv(nama_file, index=False)

# --- TAMPILAN UTAMA (SIDEBAR) ---
st.sidebar.image("https://drive.google.com/file/d/1dZZlAIiTRHy4j7bC7DQjKNMJE37N5cCw/view?usp=sharing", width=100)
st.sidebar.title("Navigasi Security")
menu = st.sidebar.radio("Pilih Menu:", ["Absensi & Disiplin", "Input Laporan K3", "Wawasan Fasilitas"])

# --- HALAMAN 1: ABSENSI & DISIPLIN ---
if menu == "Absensi & Disiplin":
    st.header("📋 Absensi Security Officer - RSUD Cipayung")
    
    with st.form("form_absensi"):
        nama = st.selectbox("Nama Petugas:", ["Pilih Nama Anda","Agung", "Bagus Maryanto", "Murjadi", "Liftahudin"])
        shift = st.selectbox("Shift Jaga:", ["Pagi (07.00 - 15.00)", "Siang (15.00 - 23.00)", "Malam (23.00 - 07.00)"])
        lokasi = st.selectbox("Pos Jaga:", ["Lobby Utama", "IGD", "Ruang Rawat Inap", "Parkiran"])
        submit_absen = st.form_submit_button("Masuk Absen")

        if submit_absen and nama:
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Logika sederhana untuk cek kedisiplinan (Contoh: Absen di atas jam 8 dianggap telat)
            # Di sini kita catat saja waktunya dulu.
            
            data_absen = {
                "Waktu": [waktu_sekarang],
                "Nama": [nama],
                "Shift": [shift],
                "Lokasi": [lokasi],
                "Status": ["Hadir"]
            }
            simpan_data(data_absen, "data_absensi.csv")
            st.success(f"Absensi berhasil dicatat untuk {nama} pada {waktu_sekarang}")

    # Menampilkan Riwayat Absensi
    if os.path.isfile("data_absensi.csv"):
        st.subheader("Riwayat Kedisiplinan")
        df_absen = pd.read_csv("data_absensi.csv")
        st.dataframe(df_absen)

# --- HALAMAN 2: INPUT LAPORAN (DISIPLIN INPUT FORMULIR) ---
elif menu == "Input Laporan K3":
    st.header("📝 Laporan Kejadian & K3")
    st.info("Disiplin input formulir: Harap lapor segera setelah kejadian.")

    with st.form("form_laporan"):
        pelapor = st.text_input("Nama Pelapor:")
        jenis_kejadian = st.selectbox("Jenis Kejadian:", ["Pencurian", "Kerusakan Fasilitas", "Kecelakaan Kerja", "Gangguan Ketertiban", "Lainnya"])
        deskripsi = st.text_area("Kronologi Singkat:")
        tindak_lanjut = st.radio("Apakah sudah ditangani?", ["Belum", "Sedang Proses", "Selesai"])
        submit_laporan = st.form_submit_button("Kirim Laporan")

        if submit_laporan and pelapor:
            waktu_lapor = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_laporan = {
                "Waktu Lapor": [waktu_lapor],
                "Pelapor": [pelapor],
                "Kejadian": [jenis_kejadian],
                "Deskripsi": [deskripsi],
                "Status": [tindak_lanjut]
            }
            simpan_data(data_laporan, "data_laporan.csv")
            st.success("Laporan berhasil dikirim. Terima kasih atas kedisiplinan Anda!")

# --- HALAMAN 3: WAWASAN FASILITAS ---
elif menu == "Wawasan Fasilitas":
    st.header("🏥 Wawasan Fasilitas RSUD Cipayung")
    st.write("Ensiklopedia mini untuk Security Officer agar paham area rumah sakit.")

    pilihan_info = st.selectbox("Cari Informasi Area:", ["IGD", "Farmasi", "Kamar Jenazah", "Jalur Evakuasi"])

    if pilihan_info == "IGD":
        st.warning("Zona Merah: Prioritas Penyelamatan Nyawa.")
        st.write("- **Akses:** Hanya untuk pasien darurat dan 1 penunggu.")
        st.write("- **Tugas Security:** Pastikan jalur ambulans tidak terhalang parkir liar.")
    
    elif pilihan_info == "Farmasi":
        st.info("Zona Pelayanan Obat.")
        st.write("- **Tugas Security:** Mengatur antrean agar tidak menumpuk di loket.")
    
    elif pilihan_info == "Kamar Jenazah":
        st.write("- **Akses:** Terbatas. Hanya petugas berwenang dan keluarga inti.")
    
    elif pilihan_info == "Jalur Evakuasi":
        st.error("PENTING: Jalur Keselamatan (K3)")
        st.write("- Pastikan tidak ada barang (troli/kursi) yang menghalangi tangga darurat.")
        st.write("- Titik kumpul ada di halaman parkir depan.")

# Footer
st.markdown("---")
st.caption("Sistem Manajemen Security RSUD Cipayung - Dikembangkan dengan Python Streamlit")





