# Word ⇄ PDF Converter

Convert Word documents to PDF and PDF files back to Word. Built with Python: a Flask backend that does the conversion and a Flet app for the user interface.

## Features

- Word (.doc, .docx) to PDF
- PDF to Word (.docx)
- Clean UI with light and dark theme
- Converted files are saved to your Downloads folder

## Tech Stack

- **Backend:** Flask, flask-cors, pdf2docx
- **Word to PDF:** LibreOffice (headless)
- **Frontend:** Flet, requests

## Project Structure

```
word to pdf/
├── Backend/
│   ├── app.py            # Flask server
│   ├── converters.py     # Conversion logic
│   └── requirements.txt
├── app/
│   ├── main.py           # Flet UI
│   ├── api.py            # Talks to the backend
│   ├── config.py         # App settings
│   └── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- [LibreOffice](https://www.libreoffice.org/download/) installed (needed for Word to PDF)

## Setup

### 1. Backend

```
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 2. App

Open a new terminal (keep the backend running):

```
cd app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Usage

1. Choose a mode: Word → PDF or PDF → Word
2. Select your file
3. Click Convert
4. Find the converted file in your Downloads folder

## Roadmap

- Web version
- Mobile version (Android/iOS)
