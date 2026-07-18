import pandas as pd


REQUIRED_COLUMNS = [
    "ID",
    "Document Title",
    "Source URL"
]


def validate_dataframe(df: pd.DataFrame):
    """
    Validate metadata before downloading documents.
    """

    print("=" * 50)
    print("Validating Metadata...")
    print("=" * 50)

    # ----------------------------
    # Check required columns
    # ----------------------------
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # ----------------------------
    # Remove completely empty rows
    # ----------------------------
    df = df.dropna(how="all")

    # ----------------------------
    # Missing URL
    # ----------------------------
    missing_url = df["Source URL"].isna().sum()

    # ----------------------------
    # Missing Title
    # ----------------------------
    missing_title = df["Document Title"].isna().sum()

    # ----------------------------
    # Duplicate URLs
    # ----------------------------
    duplicate_urls = df["Source URL"].duplicated().sum()

    print(f"Total Documents : {len(df)}")
    print(f"Missing Titles  : {missing_title}")
    print(f"Missing URLs    : {missing_url}")
    print(f"Duplicate URLs  : {duplicate_urls}")

    print("\nMetadata Validation Completed.\n")

    return df