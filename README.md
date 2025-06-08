# Proyek AI: Sistem Rekomendasi Karir Mahasiswa

Proyek ini adalah implementasi sistem *machine learning* untuk memprediksi dan merekomendasikan jalur karir yang sesuai bagi mahasiswa Ilmu Komputer berdasarkan profil akademik dan teknis mereka.

## 📝 Deskripsi Proyek

Sistem ini menggunakan model klasifikasi (XGBoost/CatBoost) yang telah dilatih pada dataset profil mahasiswa untuk memberikan rekomendasi 10 grup karir yang berbeda. Aplikasi ini terdiri dari frontend web interaktif dan backend API yang dibangun dengan Flask.

## 🚀 Fitur Utama
-   Prediksi 3 rekomendasi karir teratas beserta skor probabilitasnya.
-   Antarmuka web yang intuitif untuk input data pengguna.
-   Perbandingan 5 arsitektur model berbeda untuk menemukan yang paling optimal.
-   Akurasi model mencapai 99%+ pada dataset pengujian berkualitas tinggi.

## 🛠️ Teknologi yang Digunakan
-   **Backend:** Python, Flask, Pandas, Scikit-learn, XGBoost, CatBoost, LightGBM
-   **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
-   **Lingkungan:** Jupyter Notebook, VS Code

## ⚙️ Cara Menjalankan Proyek

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/nama-anda/nama-repo-anda.git](https://github.com/nama-anda/nama-repo-anda.git)
    cd nama-repo-anda
    ```

2.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Siapkan Aset Model:**
    * Pastikan Anda sudah memiliki dataset `cleaned_cs_students.csv` (unduh dari [link sumber data Anda di sini]).
    * Jalankan skrip untuk membuat file konfigurasi dan melatih model:
        ```bash
        python extract_options.py
        python prepare_model_xgb.py
        ```

4.  **Jalankan Server Backend:**
    ```bash
    python app_xgb.py
    ```
    Server akan berjalan di `http://127.0.0.1:5000`.

5.  **Buka Aplikasi Web:**
    * Buka file `index.html` di browser Anda.
    * Isi form dan lihat hasilnya!

## 📂 Struktur Folder
```
.
├── app_xgb.py              # Server Flask API
├── index.html              # Halaman utama web
├── script.js               # Logika frontend
├── style.css               # Styling halaman web
├── prepare_model_xgb.py    # Skrip untuk melatih & menyimpan model
├── extract_options.py      # Skrip untuk membuat konfigurasi form
├── generate_final_report.py # Skrip untuk analisis & membuat laporan
├── requirements.txt        # Daftar library Python
└── README.md               # Dokumentasi ini
