import os
import shutil
import subprocess
from pdf2docx import Converter


def _find_soffice():
    path = shutil.which("soffice") or shutil.which("libreoffice")
    if path:
        return path
    candidates = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    raise FileNotFoundError("LibreOffice not found.")


def word_to_pdf(input_path, output_dir):
    soffice = _find_soffice()
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf",
         "--outdir", output_dir, input_path],
        check=True,
        timeout=120,
    )
    base = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(output_dir, base + ".pdf")


def pdf_to_word(input_path, output_dir):
    base = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, base + ".docx")
    cv = Converter(input_path)
    try:
        cv.convert(output_path)
    finally:
        cv.close()
    return output_path