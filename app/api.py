import requests
from config import BACKEND_URL

ENDPOINTS = {
    "word_to_pdf": "/api/word-to-pdf",
    "pdf_to_word": "/api/pdf-to-word",
}


def convert_file(mode, file_name, file_bytes):
    """
    mode: "word_to_pdf" or "pdf_to_word"
    Returns: (True, converted_bytes) or (False, error_message)
    """
    url = BACKEND_URL + ENDPOINTS[mode]

    try:
        response = requests.post(
            url,
            files={"file": (file_name, file_bytes)},
            timeout=180,
        )
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to the server. Is the backend running?"
    except requests.exceptions.Timeout:
        return False, "The conversion took too long. Please try again."

    if response.status_code == 200:
        return True, response.content

    try:
        error = response.json().get("error", "Something went wrong.")
    except ValueError:
        error = f"Server error ({response.status_code})"
    return False, error