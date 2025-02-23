import hrequests
import xmltodict
import pandas
from bs4 import BeautifulSoup

evomi_proxy = ""


def get_info_from_element(element):
    if element:
        span_element = element.find_next_sibling("span")
        if span_element:
            return span_element.text.strip()
        else:
            parent = element.parent
            if parent:
                info = parent.get_text(strip=True)
                return info.replace(element.get("title", ""), "").strip()
    return ""


def get_websites():
    url = "https://www.3d.directory/sitemap/manufacturers"
    resp = hrequests.get(url, proxy=evomi_proxy)
    sitemap = xmltodict.parse(resp.text)
    urls = [url["loc"] for url in sitemap["urlset"]["url"]]
    manufacturers = []

    for url in urls:
        for i in range(10):
            try:
                resp = hrequests.get(url, proxy=evomi_proxy)
                html = BeautifulSoup(resp.text, "html.parser")

                name = html.select_one("h1.company-profile-heading").text.strip()

                website_url = (
                    html.select_one("div.visit-website a")
                    .get("href")
                    .replace("?utm_source=3D.directory", "")
                )

                phone_element = html.find("i", title="Phone")
                fax_element = html.find("i", title="Fax")
                location_element = html.find("i", title="Location")
                hq_address_element = html.find("i", title="HQ Address")
                phone_number = get_info_from_element(phone_element)
                fax_number = get_info_from_element(fax_element)
                location = get_info_from_element(location_element)
                hq_address = get_info_from_element(hq_address_element)

                manufacturer = {
                    "name": name,
                    "url": website_url,
                    "emails": "",
                    "phone_number": phone_number,
                    "fax_number": fax_number,
                    "location": location,
                    "hq_address": hq_address,
                }

                manufacturers.append(manufacturer)
                print(f"\nManufacturer: {manufacturer}")
                break
            except Exception as e:
                print(e)
                continue

    csv = pandas.DataFrame(manufacturers)
    csv.to_csv("manufacturers.csv", index=False)


get_websites()
