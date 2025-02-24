import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from printing_directory.get_websites import get_websites
from printing_directory.browser_check_manufacturers_website import check_manufacturers
from printing_directory.export_excel import csv_to_excel

csv_path = Path(__file__).parent.parent / "outputs" / "manufacturers.csv"
excel_path = Path(__file__).parent.parent / "outputs" / "manufacturers.xlsx"
evomi_proxy = ""
NUM_THREADS = 1
MAX_RETRIES = 3


def main():
    df_websites = get_websites(MAX_RETRIES)
    df_checked = check_manufacturers(df_websites, evomi_proxy, NUM_THREADS, MAX_RETRIES)
    df_checked.to_csv(csv_path, index=False)
    csv_to_excel(df_checked, excel_path)


if __name__ == "__main__":
    main()
