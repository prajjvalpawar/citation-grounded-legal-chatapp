import os
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

from .config import (
    METADATA_FILE,
    RAW_DOCUMENTS_DIR,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    HEADERS,
)

from .validator import validate_dataframe


def get_extension(url: str):
    """
    Detect file extension from URL.
    """

    url = url.lower()

    if ".pdf" in url:
        return ".pdf"

    if ".docx" in url:
        return ".docx"

    if ".doc" in url:
        return ".doc"

    return ".html"


def download_file(url, output_path):

    for _ in range(MAX_RETRIES):

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            return True

        except Exception:
            pass

    return False


def main():

    RAW_DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(METADATA_FILE, header=1)

    df = validate_dataframe(df)

    success = 0
    failed = 0

    print("=" * 50)
    print("Downloading Documents...")
    print("=" * 50)

    for _, row in tqdm(df.iterrows(), total=len(df)):

        doc_id = int(row["ID"])

        url = str(row["Source URL"]).strip()

        extension = get_extension(url)

        filename = f"{doc_id:03d}{extension}"

        output_file = RAW_DOCUMENTS_DIR / filename

        if output_file.exists():
            continue

        ok = download_file(url, output_file)

        if ok:
            success += 1
        else:
            failed += 1

    print("\n")
    print("=" * 50)
    print("Download Summary")
    print("=" * 50)

    print(f"Downloaded : {success}")
    print(f"Failed     : {failed}")


if __name__ == "__main__":
    main()