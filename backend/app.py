import os
import uuid
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from converters import word_to_pdf, pdf_to_word

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB


def _handle(convert_fn, allowed_ext, out_ext):
    if "file" not in request.files:
        return jsonify({"error": "No file was uploaded."}), 400

    f = request.files["file"]
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in allowed_ext:
        return jsonify({"error": f"Only {', '.join(allowed_ext)} files are allowed."}), 400

    job_id = uuid.uuid4().hex
    in_path = os.path.join(UPLOAD_DIR, job_id + ext)
    f.save(in_path)

    try:
        out_path = convert_fn(in_path, OUTPUT_DIR)
        original_name = os.path.splitext(f.filename)[0]
        return send_file(
            out_path,
            as_attachment=True,
            download_name=original_name + out_ext,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(in_path):
            os.remove(in_path)


@app.route("/api/word-to-pdf", methods=["POST"])
def api_word_to_pdf():
    return _handle(word_to_pdf, (".doc", ".docx"), ".pdf")


@app.route("/api/pdf-to-word", methods=["POST"])
def api_pdf_to_word():
    return _handle(pdf_to_word, (".pdf",), ".docx")


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)