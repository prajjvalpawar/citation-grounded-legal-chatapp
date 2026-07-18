import json
import os

import fitz  # PyMuPDF
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


# ==============================
# CONFIGURATION
# ==============================

METADATA_FILE = "data/metadata/metadata.xlsx"
PDF_FOLDER = "data/documents"
RAW_DOCUMENTS_FOLDER = "data/raw_documents"
OUTPUT_FILE = "processed/legal_chunks.json"

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(RAW_DOCUMENTS_FOLDER, exist_ok=True)
os.makedirs("processed", exist_ok=True)


# ==============================
# 1. LOAD METADATA
# ==============================

def load_metadata():
    print("\nLoading metadata...")

    try:
        df = pd.read_excel(METADATA_FILE, sheet_name="Document Corpus", header=1)
    except ValueError:
        df = pd.read_excel(METADATA_FILE, header=1)

    df = df.dropna(how="all").copy()

    print("Total documents found:", len(df))
    print("Columns:", df.columns.tolist())

    return df


# ==============================
# 2. DOWNLOAD PDF DOCUMENTS
# ==============================

def safe_value(row, key, default=""):
    value = row.get(key, default)
    if pd.isna(value):
        return default
    return str(value).strip()


def find_document_path(row, index):
    doc_id = row.get("ID")
    candidates = []

    if pd.notna(doc_id):
        try:
            doc_id = int(float(doc_id))
            formatted_id = f"{doc_id:03d}"
            candidates.extend(
                [
                    os.path.join(RAW_DOCUMENTS_FOLDER, f"{formatted_id}.pdf"),
                    os.path.join(RAW_DOCUMENTS_FOLDER, f"{formatted_id}.html"),
                    os.path.join(RAW_DOCUMENTS_FOLDER, f"{formatted_id}.htm"),
                    os.path.join(RAW_DOCUMENTS_FOLDER, f"{formatted_id}.txt"),
                ]
            )
        except (ValueError, TypeError):
            pass

    candidates.append(os.path.join(PDF_FOLDER, f"document_{index}.pdf"))

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


def download_documents(df):
    print("\nChecking documents...")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        source_url = safe_value(row, "Source URL")
        if not source_url.startswith(("http://", "https://")):
            continue

        existing_path = find_document_path(row, index)
        if existing_path:
            continue

        filepath = os.path.join(PDF_FOLDER, f"document_{index}.pdf")

        try:
            response = requests.get(source_url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
        except Exception as e:
            print("Download error:", e)


# ==============================
# 3. EXTRACT TEXT FROM FILE
# ==============================

def extract_text(file_path):
    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
        elif ext in {".html", ".htm"}:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            text = soup.get_text("\n", strip=True)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    except Exception as e:
        print("Read error:", file_path, e)

    return text


# ==============================
# 4. CLEAN TEXT
# ==============================

def clean_text(text):
    return " ".join(text.split())


# ==============================
# 5. TEXT CHUNKING
# ==============================

def create_chunks(text, chunk_size=1000, overlap=200):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


# ==============================
# 6. PROCESS DOCUMENTS
# ==============================

def process_documents(df):
    all_chunks = []

    print("\nProcessing documents...")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        document_path = find_document_path(row, index)
        if not document_path:
            continue

        text = extract_text(document_path)
        if len(text.strip()) < 20:
            fallback_text = " ".join(
                [
                    safe_value(row, "Document Title", "Unknown"),
                    safe_value(row, "Category", ""),
                    safe_value(row, "Source URL", ""),
                ]
            )
            text = fallback_text

        text = clean_text(text)
        if len(text) == 0:
            continue

        chunks = create_chunks(text)

        for chunk_id, chunk in enumerate(chunks):
            data = {
                "text": chunk,
                "metadata": {
                    "document_id": index,
                    "title": safe_value(row, "Document Title", "Unknown"),
                    "source": safe_value(row, "Source URL", ""),
                    "chunk_id": chunk_id,
                },
            }
            all_chunks.append(data)

    return all_chunks


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    metadata = load_metadata()
    download_documents(metadata)
    chunks = process_documents(metadata)

    print("\nTotal chunks created:", len(chunks))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=4, ensure_ascii=False)

    print("\nSUCCESS!")
    print("Saved:", OUTPUT_FILE)