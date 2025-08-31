import os
import pytesseract
from PIL import Image
from modules.utils import ensure_dir, create_zip

def process_ocr_from_folder(input_folder, output_folder):
    ensure_dir(output_folder)
    files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg','.jpeg','.png'))])
    for file in files:
        try:
            img_path = os.path.join(input_folder, file)
            image = Image.open(img_path)
            text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
            lines = [' '.join(line.strip().split()) for line in text.split('\n') if line.strip()]
            processed_text = '\n'.join(lines)
            output_txt_path = os.path.join(output_folder, os.path.splitext(file)[0]+'.txt')
            with open(output_txt_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
            print(f"OCR selesai: {file}")
        except Exception as e:
            print(f"Gagal OCR {file}: {e}")

def run_ocr():
    out_color = "data/ocr_results/color-transfer"
    out_raw = "data/ocr_results/raw"
    ensure_dir(out_color); ensure_dir(out_raw)
    print("\n--- OCR Color Transfer ---")
    process_ocr_from_folder("data/result_color-transfer", out_color)
    create_zip("hasil_ocr-colortransfer.zip", out_color)
    print("\n--- OCR Raw ---")
    process_ocr_from_folder("data/source", out_raw)
    create_zip("hasil_ocr-raw.zip", out_raw)
