import requests
import re
from threading import Thread
import sys
import logging

COUNTRIES = {
    "US": "United States",
    "AR": "Argentina",
    "BS": "Bahamas",
    "BR": "Brazil",
    "CA": "Canada",
    "CL": "Chile",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "GL": "Greenland",
    "MX": "Mexico",
    "PA": "Panama",
    "VE": "Venezuela",
    "AL": "Albania",
    "AD": "Andorra",
    "AT": "Austria",
    "BE": "Belgium",
    "BA": "Bosnia and Herzegovina",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "EE": "Estonia",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HU": "Hungary",
    "IS": "Iceland",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IT": "Italy",
    "LV": "Latvia",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MT": "Malta",
    "MD": "Moldova",
    "MC": "Monaco",
    "ME": "Montenegro",
    "NL": "Netherlands",
    "MK": "North Macedonia",
    "NO": "Norway",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "RS": "Serbia",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ES": "Spain",
    "SE": "Sweden",
    "CH": "Switzerland",
    "TR": "Turkey",
    "UA": "Ukraine",
    "UK": "United Kingdom",
    "AU": "Australia",
    "BD": "Bangladesh",
    "KH": "Cambodia",
    "CN": "China",
    "HK": "Hong Kong SAR China",
    "IN": "India",
    "ID": "Indonesia",
    "JP": "Japan",
    "MY": "Malaysia",
    "MN": "Mongolia",
    "NZ": "New Zealand",
    "PH": "Philippines",
    "SG": "Singapore",
    "LK": "Sri Lanka",
    "TW": "Taiwan",
    "VN": "Vietnam",
    "DZ": "Algeria",
    "AM": "Armenia",
    "EG": "Egypt",
    "GE": "Georgia",
    "IL": "Israel",
    "KZ": "Kazakhstan",
    "MA": "Morocco",
    "NG": "Nigeria",
    "QA": "Qatar",
    "SA": "Saudi Arabia",
    "ZA": "South Africa",
    "AE": "United Arab Emirates"}

GOG_API_URL: str = "https://api.gog.com / products"
GOG_PRICE_URL: str = "https://api.gog.com/products/%ID%/prices?countryCode=%CODE%"
COUNTRY_PRICES: dict = {}

logging.basicConfig(
    level=logging.INFO,
)


def extract_product_id(url):
    html = requests.get(url)
    # TODO: 27.07.2023-10:51 регулярка на продакт ид
    raw_card_product = re.search(r"card-product=\"\d*\"", html.text).group()
    product_id = re.search(r"(\d+)", raw_card_product).group()
    logging.debug(f"raw product id: {raw_card_product}")
    logging.debug(f"product id: {product_id}")
    return product_id


def request_price(product_id, country_code):
    data = None
    try:
        url = f"https://api.gog.com/products/{product_id}/prices?countryCode={country_code}"
        logging.debug(url)
        response = requests.get(url)
        data = response.json()
        logging.debug(response.json())
        price = data['_embedded']['prices'][0]['finalPrice'].split(" ")
        price[0] = int(price[0]) / 100
        logging.debug(price)
        COUNTRY_PRICES[COUNTRIES[country_code]] = price
    except KeyError as no_key_error:
        logging.error(no_key_error)
        logging.error(data)


def request_prices(product_id):
    threads = []
    for country_code in COUNTRIES:
        t = Thread(target=request_price, args=(product_id, country_code))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def sort_prices():
    global COUNTRY_PRICES
    COUNTRY_PRICES = sorted(COUNTRY_PRICES.items(), key=lambda x: x[1], reverse=True)


def out_result():
    print(COUNTRY_PRICES)
    pass


def main(args):
    game_url = "https://www.gog.com/game/diablo"
    product_id = extract_product_id(game_url)
    request_prices(product_id)
    sort_prices()
    out_result()


if __name__ == "__main__":
    args = sys.argv
    main(args)
