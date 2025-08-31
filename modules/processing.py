import cv2
import numpy as np
import os
from modules.utils import ensure_dir, create_zip

def read_file(source_path, target_path):
    s = cv2.imread(source_path)
    s = cv2.cvtColor(s, cv2.COLOR_BGR2LAB)
    t = cv2.imread(target_path)
    t = cv2.cvtColor(t, cv2.COLOR_BGR2LAB)
    return s, t

def get_mean_and_std(x):
    x_mean, x_std = cv2.meanStdDev(x)
    x_mean = np.hstack(np.around(x_mean, 2))
    x_std = np.hstack(np.around(x_std, 2))
    return x_mean, x_std

def color_transfer(s, t):
    s_mean, s_std = get_mean_and_std(s)
    t_mean, t_std = get_mean_and_std(t)
    h, w, c = s.shape
    for i in range(h):
        for j in range(w):
            for k in range(c):
                x = s[i, j, k]
                x = ((x - s_mean[k]) * (t_std[k] / s_std[k])) + t_mean[k]
                x = round(x)
                x = max(0, min(255, x))
                s[i, j, k] = x
    return cv2.cvtColor(s, cv2.COLOR_LAB2BGR)

def illumination_correction(image):
    dilated = cv2.dilate(image, np.ones((7,7), np.uint8))
    bg = cv2.medianBlur(dilated, 21)
    diff = 255 - cv2.absdiff(image, bg)
    return cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX)

def edge_preserving(image):
    return cv2.bilateralFilter(image, 9, 75, 75)

def noise_reduction(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 3, 3, 7, 21)

def stretch_contrast(image):
    img_float = image.astype(np.float32)
    for i in range(3):
        channel = img_float[:,:,i]
        min_val, max_val = np.min(channel), np.max(channel)
        img_float[:,:,i] = 255 * (channel - min_val) / (max_val - min_val + 1e-5)
    return img_float.astype(np.uint8)

def unsharpMasking(image):
    blurred = cv2.GaussianBlur(image, (5,5), 1.0)
    return cv2.addWeighted(image, 1.5, blurred, -0.5, 0)

def preprocess_image(image):
    image = illumination_correction(image)
    image = noise_reduction(image)
    return image

def postprocess_image(image):
    image = edge_preserving(image)
    image = unsharpMasking(image)
    image = stretch_contrast(image)
    return image

def process_images():
    source_dir = "data/source"
    target_dir = "data/target"
    result_dir = "data/result_color-transfer"
    ensure_dir(result_dir)

    source_files = sorted([f for f in os.listdir(source_dir) if f.endswith('.jpg')])
    target_files = [f for f in os.listdir(target_dir) if f.endswith('.jpg')]
    if not target_files:
        print("Error: Tidak ada file target ditemukan!")
        return
    target_file = target_files[0]

    for i, source_file in enumerate(source_files):
        print(f"Processing {i+1}: {source_file} with target {target_file}...")
        s, t = read_file(os.path.join(source_dir, source_file), os.path.join(target_dir, target_file))
        s = preprocess_image(s)
        s = color_transfer(s, t)
        s = postprocess_image(s)
        cv2.imwrite(os.path.join(result_dir, source_file), s)

    zip_filename = os.path.join(os.getcwd(), 'hasil_image_enhancement-colortransfer.zip')
    create_zip(zip_filename, result_dir)
    print(f"Hasil dibungkus di {zip_filename}")
