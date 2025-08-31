import os
import zipfile

def ensure_dir(path):
    """Buat folder jika belum ada"""
    os.makedirs(path, exist_ok=True)

def create_zip(output_filename, source_dir):
    """Membuat file zip dari semua file dalam direktori sumber"""
    with zipfile.ZipFile(output_filename, 'w') as zipf:
        for file in os.listdir(source_dir):
            file_path = os.path.join(source_dir, file)
            if os.path.isfile(file_path):
                zipf.write(file_path, arcname=file)
