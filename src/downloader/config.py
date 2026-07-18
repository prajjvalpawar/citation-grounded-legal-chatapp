from pathlib import Path

# ==========================================================
# Project Root Directory
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==========================================================
# Data Directories
# ==========================================================

DATA_DIR = PROJECT_ROOT / "data"

METADATA_DIR = DATA_DIR / "metadata"

RAW_DOCUMENTS_DIR = DATA_DIR / "raw_documents"

PROCESSED_DIR = DATA_DIR / "processed"

CHUNKS_DIR = DATA_DIR / "chunks"

# ==========================================================
# Metadata File
# ==========================================================

METADATA_FILE = METADATA_DIR / "metadata.xlsx"

# ==========================================================
# Download Settings
# ==========================================================

REQUEST_TIMEOUT = 30

MAX_RETRIES = 3

# ==========================================================
# Supported File Extensions
# ==========================================================

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
]

# ==========================================================
# User Agent
# ==========================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}