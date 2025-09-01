K3521010 | Annisa Nur Chasidiyah | Penelitian Skripsi

# Color Transfer OCR Enhancement

Proyek ini merupakan implementasi **Image Enhancement menggunakan Color Transfer** untuk optimasi hasil **Optical Character Recognition (OCR)** pada halaman buku lama.  
Evaluasi dilakukan dengan metrik **PSNR, SSIM, RMSE** untuk kualitas gambar dan **WER, CER** untuk hasil OCR.

---

## 🔗 Repository
[GitHub Link](https://github.com/Anchosy24/colortransfer-ocr-enhancement.git)

---

## 🚀 Petunjuk Pemakaian

### 1. Install Python
- Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Saat instalasi, pastikan opsi **"Add Python to PATH"** dicentang.
- Verifikasi instalasi:
  ```bash
  python --version

### 2. Install Tesseract OCR

* Download installer Tesseract (Windows): [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
* Install pada perangkat.
* Catat lokasi instalasi (misalnya `C:\Program Files\Tesseract-OCR\tesseract.exe`) dan tambahkan ke **PATH**.
* Verifikasi instalasi:

  ```bash
  tesseract --version
  ```

### 3. Clone Repository

```bash
git clone https://github.com/Anchosy24/colortransfer-ocr-enhancement.git
cd colortransfer-ocr-enhancement
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📂 Struktur Folder

```
data/
├── original/              # Ground truth text file (format .txt)
├── input/                 # Gambar asli (scan halaman buku lama)
├── result_color-transfer/ # Hasil enhancement (otomatis dibuat)
├── ocr_results/           # Hasil OCR (otomatis dibuat)
│   ├── raw/
│   └── color-transfer/
└── evaluasi/              # Hasil evaluasi OCR (otomatis dibuat)
```

---

## ▶️ Menjalankan Program

Jalankan pipeline utama:

```bash
python main.py
```

### Alur Program:

1. **Enhancement** dengan metode Color Transfer
2. **Evaluasi kualitas gambar** (PSNR, SSIM, RMSE)
3. **OCR dengan Tesseract** → hasil disimpan di `data/ocr_results/`
4. **Evaluasi OCR** (WER, CER) → hasil disimpan di `data/evaluasi/ocr_evaluation.csv`

---

## 📊 Hasil

* **Kualitas Gambar:**
  `quality_metrics_results.csv`

* **Hasil OCR:**
  `data/ocr_results/`

* **Evaluasi OCR (WER & CER):**
  `data/evaluasi/ocr_evaluation.csv`

---

## 📝 Lisensi

Proyek ini dibuat untuk kebutuhan akademik (skripsi/penelitian). Silakan gunakan dan modifikasi sesuai kebutuhan.

```
