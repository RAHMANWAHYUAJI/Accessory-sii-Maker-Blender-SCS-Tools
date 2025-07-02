# io_scs_tools: SII Generator for Blender

Sebuah addon Blender yang dirancang untuk menyederhanakan dan mengotomatisasi proses pembuatan file `.sii` (SCS Definition File). Fitur ini sangat esensial bagi para *modder* game simulasi truk seperti Euro Truck Simulator 2 (ETS2) atau American Truck Simulator (ATS).

[![addon-layout.png](https://i.postimg.cc/YSqbDThN/addon-layout.png)](https://postimg.cc/sMqYv6P1)

---

## ✨ Fitur Utama

* **Panel Generator Terintegrasi:** Membuat file `.sii` untuk berbagai tipe data (`accessory`, `cabin`, `chassis`) langsung dari panel di 3D View.
* **Pembuatan Massal (Batch):** Mampu membuat file `.sii` untuk semua *SCS Root Object* yang terseleksi secara bersamaan.
* **Akses Cepat:** Setelah file dibuat, tombol **Buka Folder Tujuan** akan muncul untuk membuka lokasi file secara instan.
* **Validasi Otomatis:** Input pada *field* nama definisi dan nama file akan divalidasi dan diformat secara otomatis untuk mencegah karakter yang tidak valid.
* **Input Fleksibel:** Mendukung pemilihan `variant` dan `look` otomatis dari data objek, serta input manual jika diperlukan.
* **Atribut Dinamis:** Fitur tambah/hapus item yang mudah untuk atribut seperti `suitable_for`, `defaults`, `conflict_with`, dan `overrides`.
* **Pratinjau Langsung:** Lihat isi file `.sii` yang akan dihasilkan sebelum menyimpannya dengan fitur **Preview**.
* **Dukungan Multi-Bahasa:** Antarmuka panel tersedia dalam Bahasa Indonesia dan Inggris.

---

## ⚙️ Persyaratan

* **Blender 2.79** (untuk versi lawas) atau **Blender 2.80+** (untuk versi terbaru).
* Addon ini dirancang untuk alur kerja modding game berbasis SCS Software (ETS2/ATS).

**Preview Blender 2.79 vvv**

![image](https://github.com/user-attachments/assets/de109679-dda5-4e82-a535-18db7aaff44b)




**Preview Blender 2.93 vvv**

![image](https://github.com/user-attachments/assets/fa5e4698-cc83-4309-88ab-6395fc219dab)




**Preview Blender 3.6 vvv**

![image](https://github.com/user-attachments/assets/6f5ec1ae-fe16-45a9-8a12-c7913d0282e6)

---

## 🚀 Pemasangan (Installation)

#### Metode 1: Install dari File .zip (Disarankan)

1.  Unduh versi terbaru addon dari halaman **[Releases](https://github.com/RAHMANWAHYUAJI/Accessory-sii-Maker-Blender-SCS-Tools/releases)** di GitHub.
2.  Buka Blender, masuk ke menu `Edit > Preferences > Add-ons`.
3.  Klik tombol **Install...** di bagian atas.
4.  Arahkan ke file `.zip` yang baru saja Anda unduh, lalu klik **Install Add-on**.
5.  Cari "SCS Tools" di kolom pencarian, lalu centang kotak untuk mengaktifkannya.

#### Metode 2: Pemasangan Manual

1.  Unduh kode sumber (source code) dan ekstrak file `.zip` tersebut.
2.  Anda akan mendapatkan sebuah folder bernama `io_scs_tools`.
3.  Salin (copy) seluruh folder `io_scs_tools` tersebut ke dalam direktori addons Blender Anda.
    * **Lokasi Direktori:**
        ```
        C:\Users\NAMA_USER\AppData\Roaming\Blender Foundation\Blender\VERSI_BLENDER\scripts\addons\
        ```
    * Ganti `NAMA_USER` dan `VERSI_BLENDER` (misal: 2.79, 3.6, 4.1) sesuai dengan konfigurasi PC Anda.
4.  Buka Blender (atau restart jika sudah terbuka), lalu aktifkan addon seperti pada metode pertama.

---

## 📖 Panduan Penggunaan

### 1. Pengaturan Awal (Wajib)

Sebelum menggunakan generator, Anda **wajib** mengatur path utama proyek mod Anda.

* Masuk ke `Edit > Preferences > Add-ons`.
* Cari addon "SCS Tools" dan buka pengaturannya.
* Isi field **SCS Project Base Path** dengan path ke folder utama mod Anda (folder yang berisi folder `def`, `vehicle`, dll).
![image](https://github.com/user-attachments/assets/02622943-6253-4f4a-a124-6786c350c72a)


### 2. Alur Kerja Dasar

1.  **Pilih SCS Root Object:** Panel "SCS .sii Generator" hanya akan muncul di tab **"SCS Tools"** pada 3D View jika Anda memilih objek yang telah ditetapkan sebagai **SCS Root Object**.
2.  **Isi Data:** Lengkapi semua *field* yang relevan pada panel. Addon akan membantu memformat beberapa input secara otomatis.
3.  **Generate File:**
    * Klik **Generate SII** untuk membuat file dari objek yang sedang aktif.
    * Klik **Batch Generate** untuk membuat file dari semua objek yang terseleksi.
4.  **Buka Folder:** Setelah berhasil, tombol **Buka Folder Tujuan** akan muncul. Klik untuk langsung melihat file `.sii` Anda.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **GNU General Public License v3.0**. Lihat file `LICENSE` untuk detail lebih lanjut.

---

## 🤝 Kontribusi & Laporan Masalah

Jika Anda menemukan masalah (bug) atau memiliki saran untuk fitur baru, silakan buat laporan melalui tab **[Issues](https://github.com/RAHMANWAHYUAJI/Accessory-sii-Maker-Blender-SCS-Tools/issues)** di repositori ini.

---

## 👤 Kreator

* **@rw_aji**
