import pandas as pd

from .config import METADATA_FILE


def load_metadata():
    """
    Load metadata Excel file.
    """

    try:
        df = pd.read_excel(METADATA_FILE, header=1)

        print("=" * 50)
        print("Metadata Loaded Successfully")
        print("=" * 50)

        print(f"Total Documents : {len(df)}")
        print(f"Total Columns   : {len(df.columns)}")

        print("\nColumns Found:")

        for column in df.columns:
            print(f"• {column}")

        return df

    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    load_metadata()