import os
import csv
import jiwer
from modules.utils import ensure_dir, create_zip

def clean_text(text):
    transformation = jiwer.Compose([jiwer.RemoveMultipleSpaces(), jiwer.Strip(), jiwer.RemoveEmptyStrings()])
    return transformation(text)

def read_text_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read().strip()
    except: return ""

def calculate_metrics(ref, hyp):
    hyp_clean = clean_text(hyp)
    words = jiwer.process_words(ref, hyp_clean)
    chars = jiwer.process_characters(ref, hyp_clean)
    total_words = words.hits + words.substitutions + words.deletions
    total_chars = len(ref)
    return {
        "total_words": total_words,"total_chars": total_chars,
        "wer": words.wer*100,"cer": chars.cer*100,
        "word_sub": words.substitutions,"word_ins": words.insertions,"word_del": words.deletions,
        "char_sub": chars.substitutions,"char_ins": chars.insertions,"char_del": chars.deletions
    }

def evaluate_ocr():
    gt_dir = "data/original"
    res_color = "data/ocr_results/color-transfer"
    res_raw = "data/ocr_results/raw"
    eval_color = "data/evaluasi/color-transfer"; ensure_dir(eval_color)
    eval_raw = "data/evaluasi/raw"; ensure_dir(eval_raw)

    results=[]
    for file in os.listdir(gt_dir):
        if not file.endswith(".txt"): continue
        gt = clean_text(read_text_file(os.path.join(gt_dir,file)))
        color_text = read_text_file(os.path.join(res_color,file))
        raw_text = read_text_file(os.path.join(res_raw,file))
        m_color = calculate_metrics(gt,color_text)
        m_raw = calculate_metrics(gt,raw_text)
        results.append({"filename":file,**m_color,**{k+"_raw":v for k,v in m_raw.items()},
                        "wer_improve":m_raw["wer"]-m_color["wer"],
                        "cer_improve":m_raw["cer"]-m_color["cer"]})
    # Simpan ke CSV
    with open("ocr_evaluation.csv","w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f)
        header=["filename","wer","cer","wer_raw","cer_raw","wer_improve","cer_improve"]
        writer.writerow(header)
        for r in results: writer.writerow([r["filename"],r["wer"],r["cer"],r["wer_raw"],r["cer_raw"],r["wer_improve"],r["cer_improve"]])
    print("Evaluasi OCR disimpan ke ocr_evaluation.csv")
