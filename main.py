from modules.processing import process_images
from modules.metrics import evaluate_quality
from modules.ocr import run_ocr
from modules.evaluation import evaluate_ocr

if __name__ == "__main__":
    print("=== STEP 1: Enhancement ===")
    process_images()
    print("\n=== STEP 2: Quality Metrics ===")
    evaluate_quality()
    print("\n=== STEP 3: OCR ===")
    run_ocr()
    print("\n=== STEP 4: Evaluation ===")
    evaluate_ocr()
    print("\nPipeline selesai 🚀")
