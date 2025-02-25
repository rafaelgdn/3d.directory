from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from pathlib import Path
import pandas as pd
import hrequests
import time
import json
import re

csv_path = Path(__file__).parent.parent / "manufacturers.csv"
save_path = Path(__file__).parent.parent / "manufacturers_checked.csv"

NUM_THREADS = 20


def get_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def extract_emails(text):
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.com\b"
    return re.findall(email_pattern, text)


def remove_duplicates(items):
    return list(dict.fromkeys(items))


def process_urls(urls, session):
    digifabster_urls = []
    threeyourmind_urls = []
    amfg_urls = []

    for url in urls:
        for i in range(10):
            try:
                print(f"Checking {url}")
                resp = session.get(url)
                page_text = resp.text.lower()

                if "digifabster.com" in page_text:
                    digifabster_urls.append(url)

                if "3yourmind.com" in page_text:
                    threeyourmind_urls.append(url)

                if "amfg.ai" in page_text:
                    amfg_urls.append(url)

                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
                continue

    return digifabster_urls, threeyourmind_urls, amfg_urls


def process_website(row):
    index, url = row

    print(f"Checking main url: {url}")

    for i in range(3):
        try:
            session = hrequests.Session()
            resp = session.get(url)

            found_urls = [
                link
                for link in resp.html.links
                if get_domain(url) in link
                and "wp-content" not in link
                and "uploads" not in link
                and ".jpg" not in link
                and ".png" not in link
                and ".pdf" not in link
                and ".jpeg" not in link
                and ".gif" not in link
                and ".svg" not in link
                and ".webp" not in link
                and ".ico" not in link
                and ".css" not in link
                and ".js" not in link
            ]
            found_urls.append(url)
            found_urls = remove_duplicates(found_urls)

            found_emails = extract_emails(resp.text)

            digifabster_urls, threeyourmind_urls, amfg_urls = process_urls(
                found_urls, session
            )

            return index, found_emails, digifabster_urls, threeyourmind_urls, amfg_urls

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)
            continue

    return index, [], [], [], []


def main():
    df = pd.read_csv(csv_path)

    if "emails" not in df.columns:
        df["emails"] = None

    if "digifabster_urls" not in df.columns:
        df["digifabster_urls"] = None

    if "3yourmind_urls" not in df.columns:
        df["3yourmind_urls"] = None

    if "amfg_urls" not in df.columns:
        df["amfg_urls"] = None

    df["emails"] = df["emails"].astype("object")
    df["digifabster_urls"] = df["digifabster_urls"].astype("object")
    df["3yourmind_urls"] = df["3yourmind_urls"].astype("object")
    df["amfg_urls"] = df["amfg_urls"].astype("object")

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        future_to_index = {
            executor.submit(process_website, (index, row["url"])): index
            for index, row in df.iterrows()
            if not pd.isna(row["url"])
        }

        for future in as_completed(future_to_index):
            index, found_emails, digifabster_urls, threeyourmind_urls, amfg_urls = (
                future.result()
            )

            if found_emails:
                df.at[index, "emails"] = json.dumps(remove_duplicates(found_emails))

            if amfg_urls:
                df.at[index, "amfg_urls"] = json.dumps(remove_duplicates(amfg_urls))

            if digifabster_urls:
                df.at[index, "digifabster_urls"] = json.dumps(
                    remove_duplicates(digifabster_urls)
                )

            if threeyourmind_urls:
                df.at[index, "3yourmind_urls"] = json.dumps(
                    remove_duplicates(threeyourmind_urls)
                )

            print(
                f"{remove_duplicates(found_emails)}\n{remove_duplicates(amfg_urls)}\n{remove_duplicates(digifabster_urls)}\n{remove_duplicates(threeyourmind_urls)}\n\n"
            )

    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    main()
