import re
from threading import Thread
import logging
from argparse import ArgumentParser
from urllib import request as urllib_request
import json
from gog_price_checker.countries import COUNTRIES

COUNTRY_PRICES = {}

logging.basicConfig(
    level=logging.INFO,
)


def extract_product_id(url):
    html = urllib_request.urlopen(url).read().decode('utf-8')
    raw_card_product = re.search(r"card-product=\"\d*\"", html).group()
    product_id = re.search(r"(\d+)", raw_card_product).group()
    logging.debug(f"raw product id: {raw_card_product}")
    logging.debug(f"product id: {product_id}")
    return product_id


def request_price(product_id, country_code, normalize=None):
    data = None
    url = f"https://api.gog.com/products/{product_id}/prices?countryCode={country_code}"
    if normalize:
        url += "&currency=USD"
    try:
        logging.debug(url)
        response = urllib_request.urlopen(url).read().decode('utf-8')
        data = json.loads(response)
        logging.debug(data)
        price = data['_embedded']['prices'][0]['finalPrice'].split(" ")
        price[0] = int(price[0]) / 100
        logging.debug(price)
        COUNTRY_PRICES[COUNTRIES[country_code]] = price
    except KeyError as no_key_error:
        logging.error(no_key_error)
        logging.error(data)


def request_prices(product_id, normalize=None):
    threads = []
    for country_code in COUNTRIES:
        t = Thread(target=request_price, args=(product_id, country_code, normalize))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def sort_prices():
    return sorted(COUNTRY_PRICES.items(), key=lambda x: x[1], reverse=False)


def out_result(count, pretty=None):
    sorted_prices = sort_prices()
    count = min(abs(count), len(sorted_prices))
    if pretty:
        shift_country = 25
        shift_price = 10
        header = f"{'Country':<{shift_country}} {'Price':<{shift_price}} {'Currency'}"
        print(header)
        print("-" * len(header))
        for i, price in enumerate(sorted_prices):
            if i == count:
                break
            country, price_val, currency = price[0], price[1][0], price[1][1]
            print(f"{country:<{shift_country}} {price_val:<{shift_price}} {currency}")
    else:
        for i, price in enumerate(sorted_prices):
            if i == count:
                break
            print(f"{price[0]}: {price[1][0]} {price[1][1]}")


def main():
    args = init_parser().parse_args()
    if "gogdb.org" in args.url:
        product_id = args.url.split("/")[-1]
    else:
        product_id = extract_product_id(args.url)
    request_prices(product_id, args.normalize)
    sort_prices()
    out_result(args.count, args.pretty)


def init_parser():
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", required=True, type=str, help="url to scrape")
    parser.add_argument("-n", "--normalize", action="store_true", help="normalize currencies to USD")
    parser.add_argument("-c", "--count", type=int, default=10, help="number of countries to show")
    parser.add_argument("-p", "--pretty", action="store_true", help="shows result as pretty table")
    return parser


if __name__ == "__main__":
    main()
