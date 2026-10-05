# PiyXoX Laravel 12 + Filament 5 CRUD Manager

Skrip Python otomatis (`app.py`) untuk mempermudah dan mempercepat *workflow* pembuatan aplikasi/projek berbasis **Laravel 12** yang diintegrasikan dengan **Filament Admin Panel**. 
Dikembangkan untuk membantu developer melewati proses konfigurasi manual yang panjang (instalasi composer, inisialisasi `.env`, setup database, integrasi auth), serta memfasilitasi pembuatan sistem CRUD secara kilat langsung dari satu pintu terminal.
Link Tutorial YT: https://youtu.be/PfP2_zsqzwg?si=QbQL92DrGoHAB074

## 🚀 Fitur Utama
- **Auto-Installer:** Mengunduh dan menginstal kerangka kerja Laravel 12 dan mengintegrasikan Filament secara efisien.
- **Auto-Configuration:** Membantu konfigurasi file `.env` (MySQL port, username, database) dan menyesuaikan kapabilitas *database driver* Laravel 12 yang kini menuntut sinkronisasi cermat.
- **Auto-Migration & Database Setup:** Membuat database MySQL langsung (melalui PDO script) dan memigrasi struktur awal secara *on the fly*.
- **Admin Management:** Terintegrasi langsung dengan perintah pembuatan User/Akun Admin untuk dapat *login* ke Dashboard Filament.
- **CRUD Generator Mutakhir:** Membangun Model, Factory, Seeder, dan Filament Resource CRUD (termasuk deteksi mode existing table/tabel lama, kolom string, foreignId, integer, bool, dsb.) secara terstruktur dengan sistem anti-duplikasi migrasi.
- **Smart Port Binding & Auto-Browser:** Meluncurkan server Artisan dan melakukan deteksi port bebas (contoh: 8000, 8001) secara otomatis untuk mencegah tabrakan *session* apabila membuka lebih dari 1 project secara serentak.

## 📋 Prasyarat Lingkungan (Requirements)
Lihat detail *dependencies* lengkap pada `requirements.txt`.
Pada dasarnya komputer Anda harus siap dan terinstal:
- **Python >= 3.8**
- **PHP >= 8.2** (Syarat mutlak untuk Laravel 12)
- **Composer 2.0+**
- **MySQL Server** (dari XAMPP / Laragon / Native)

## 📌 Cara Penggunaan

1. Jalankan skrip Python berikut:
   ```bash
   python app.py
   ```
2. Langkah Utama Aplikasi: 
   Apabila membuat project baru, menu interaktif akan membimbing Anda. **Sangat krusial untuk mengikuti alur urutan berikut agar konfigurasi saling mengikat (Database -> Auth -> CRUD):**
   - **Menu 1:** `Setup Environment` (Merupakan fondasi utama. Akan menyiapkan `.env`, membuat DB MySQL, mengatur struktur Laravel, dan meng-install package Filament)
   - **Menu 2:** `Buat Akun Admin Filament` (Membuat akun/pass login khusus panel Dashboard).
   - **Menu 3:** `Generate CRUD` (Proses intinya. Anda tinggal menyebutkan Nama Model dan tabel akan dikonstruksikan).
   - **Menu 4:** `Jalankan Server & Buka Admin` (Mengaktifkan PHP artisan lokal dan membuka halaman otomatis ke web browser Anda di port yang aman).
   - **Menu 5:** `Clear Cache` (Tool utility jika Anda mengganti konfigurasi/environment).


## 💡 Tips & Informasi Penting
- Ketika pembuatan nama database maupun project: hindari penggunaan tombol spasi. Gunakan _underscore_ (_) jika dibutuhkan.
- Jika dalam `Menu 3` Anda mencetak Model ke "**Target Tabel yang Sudah Ada**" atau jika pernah ter-*migrate* lalu Anda ulang, skrip ini sekarang akan cerdas melompati *migrasi ulang* (*bypass migration*) guna menghindari *crash error syntax sql*.
- Jangan kuatir mengenai masalah "Salah login ke server sebelumnya", skrip ini telah dipatch untuk selalu mendeteksi port kosong saat berjalan untuk menghindari konflik akun di memori browser.
