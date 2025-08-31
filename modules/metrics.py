import cv2
import numpy as np
import os
import pandas as pd

def read_and_preprocess(source_path, target_image):
    s = cv2.imread(source_path)
    if s is None or target_image is None:
        raise ValueError(f"Gagal membaca gambar: {source_path}")
    if len(s.shape) == 2:
        s = cv2.cvtColor(s, cv2.COLOR_GRAY2BGR)
    if len(target_image.shape) == 2:
        target_image = cv2.cvtColor(target_image, cv2.COLOR_GRAY2BGR)
    s = cv2.resize(s, (target_image.shape[1], target_image.shape[0]))
    return s, target_image

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0: return float('inf')
    return 10 * np.log10(255.0 ** 2 / mse)

def calculate_ssim(img1, img2):
    from skimage.metrics import structural_similarity as ssim
    if len(img1.shape) == 3: img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    if len(img2.shape) == 3: img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return ssim(img1, img2, data_range=255)

def calculate_rmse(img1, img2):
    return np.sqrt(np.mean((img1 - img2) ** 2))

def evaluate_quality():
    target_dir = "data/target"
    result_dir = "data/result_color-transfer"

    target_files = sorted([f for f in os.listdir(target_dir) if f.lower().endswith(('.jpg','.png','.jpeg'))])
    result_files = sorted([f for f in os.listdir(result_dir) if f.lower().endswith(('.jpg','.png','.jpeg'))])
    if not target_files: return

    target_img = cv2.imread(os.path.join(target_dir, target_files[0]))
    results = []

    for result_file in result_files:
        try:
            s, r = read_and_preprocess(os.path.join(result_dir, result_file), target_img)
            psnr_CT = calculate_psnr(s, r)
            ssim_CT = calculate_ssim(s, r)
            rmse_CT = calculate_rmse(s, r)
            results.append({'filename': result_file,'psnr': psnr_CT,'ssim': ssim_CT,'rmse': rmse_CT})
        except Exception as e:
            results.append({'filename': result_file,'error': str(e)})

    df = pd.DataFrame(results)
    df.to_csv("quality_metrics_results.csv", index=False)
    print("Hasil metrik kualitas disimpan ke quality_metrics_results.csv")
