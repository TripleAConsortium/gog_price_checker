import re
import json
import logging
from threading import Thread
from argparse import ArgumentParser
from urllib import request as urllib_request
import os
import tempfile


class Price:
    country_code = None
    country_name = None
    currency = None
    value = None
    value_usd = None

    def __init__(self, country_code, country_name):
        self.country_name = country_name
        self.country_code = country_code


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
    "GB": "United Kingdom",
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

COUNTRY_PRICES = [Price(key, value) for key, value in COUNTRIES.items()]

def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def extract_product_id(url):
    html = urllib_request.urlopen(url).read().decode('utf-8')
    raw_card_product = re.search(r"card-product=\"\d*\"", html).group()
    product_id = re.search(r"(\d+)", raw_card_product).group()
    logging.debug(f"raw product id: {raw_card_product}")
    logging.debug(f"product id: {product_id}")
    return product_id


def request_price(product_id, price, normalize=None):
    data = None
    url = f"https://api.gog.com/products/{product_id}/prices?countryCode={price.country_code}"
    if normalize:
        url += "&currency=USD"
    try:
        logging.debug(url)
        response = urllib_request.urlopen(url).read().decode('utf-8')
        data = json.loads(response)
        logging.debug(data)
        for i , item in enumerate(data['_embedded']['prices']):
            if i == 0:
                final_price = item['finalPrice'].split(" ")
                price.value = int(final_price[0]) / 100
                price.currency = final_price[1]
            if item['currency']['code'] == "USD":
                price.value_usd = int(item['finalPrice'].split(" ")[0]) / 100
        logging.debug(price)
    except KeyError as no_key_error:
        logging.error(no_key_error)
        logging.error(data)


def request_prices(product_id, normalize=None):
    threads = []
    for price in COUNTRY_PRICES:
        t = Thread(target=request_price, args=(product_id, price, normalize))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def sort_prices():
    return sorted(COUNTRY_PRICES, key=lambda x: x.value_usd, reverse=False)


def out_result(count, pretty=None):
    sorted_prices = sort_prices()
    count = min(abs(count), len(sorted_prices))
    out_string = ""
    if pretty:
        shift_country = 25
        shift_price = 10
        header = f"{'Country':<{shift_country}} {'Price':<{shift_price}} {'Currency'}\n"
        out_string += header
        out_string += "-" * (len(header)-1)
        for i, price in enumerate(sorted_prices):
            if i == count:
                break
            out_string += f"\n{price.country_name:<{shift_country}} {price.value:<{shift_price}} {price.currency}"
    else:
        for i, price in enumerate(sorted_prices):
            if i == count:
                break
            out_string += f"\n{price.country_name}: {price.value} {price.currency}"
    print(out_string)


def fetch_wishlist(username, country_code):
    """Fetch wishlist HTML for a specific user and country code"""
    url = f'https://www.gog.com/u/{username}/wishlist'
    headers = {
        'Cookie': f'gog_lc={country_code}_USD_en-US',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    req = urllib_request.Request(url, headers=headers)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_file:
        try:
            with urllib_request.urlopen(req) as response:
                html_content = response.read().decode('utf-8')
                temp_file.write(html_content.encode('utf-8'))
                temp_filename = temp_file.name

            logging.info(f"Wishlist for {username} with country code {country_code} saved to {temp_filename}")
            return html_content, temp_filename
        except Exception as e:
            logging.error(f"Error fetching wishlist: {e}")
            return None, None

def extract_gog_data(html_content):
    """Extract gogData object from HTML content"""
    try:
        # Find the gogData object in the HTML
        match = re.search(r'window\.gogData\s*=\s*(\{.*?\});\s*window\.', html_content, re.DOTALL)
        if match:
            gog_data_str = match.group(1)
            # Parse the JSON data
            gog_data = json.loads(gog_data_str)
            return gog_data
        else:
            # Alternative approach if the first pattern doesn't match
            match = re.search(r'var gogData\s*=\s*(\{.*?\});\s*', html_content, re.DOTALL)
            if match:
                gog_data_str = match.group(1)
                gog_data = json.loads(gog_data_str)
                return gog_data

            logging.error("Could not find gogData in HTML")
            return None
    except Exception as e:
        logging.error(f"Error extracting gogData: {e}")
        return None

def process_wishlist(username, normalize=False):
    """Process wishlist for all countries and find the best prices"""
    # Dictionary to store product prices: {product_name: {country_code: {price, currency}}}
    product_prices = {}

    # Process each country
    for country_code, country_name in COUNTRIES.items():
        logging.info(f"Processing country: {country_name} ({country_code})")

        # Fetch wishlist for this country
        html_content, temp_filename = fetch_wishlist(username, country_code)
        if not html_content:
            continue

        # Extract gogData
        gog_data = extract_gog_data(html_content)
        if not gog_data or 'products' not in gog_data:
            # Clean up temp file
            if temp_filename and os.path.exists(temp_filename):
                os.unlink(temp_filename)
            continue

        # Process products
        for product in gog_data['products']:
            product_id = product.get('id')
            product_title = product.get('title')

            if not product_id or not product_title:
                continue

            # Get price information
            price_info = product.get('price')
            if not price_info:
                continue

            # Handle different price formats
            amount = None
            currency = 'USD'  # Default currency

            if isinstance(price_info, dict):
                amount = price_info.get('amount')

                # Handle currency which could be a string or a dict
                curr_info = price_info.get('currency')
                if isinstance(curr_info, dict):
                    currency = curr_info.get('code', 'USD')
                elif isinstance(curr_info, str):
                    currency = curr_info
            elif isinstance(price_info, str):
                # Sometimes price might be directly a string like "19.99 USD"
                parts = price_info.split(' ')
                if len(parts) >= 2:
                    try:
                        amount = parts[0]
                        currency = parts[1]
                    except (IndexError, ValueError):
                        logging.warning(f"Could not parse price string: {price_info}")
                        continue

            if amount is None:
                continue

            # Initialize product in dictionary if not exists
            if product_title not in product_prices:
                product_prices[product_title] = {}

            # Store price information
            product_prices[product_title][country_code] = {
                'country_code': country_code,
                'country_name': country_name,
                'price': amount,
                'currency': currency
            }

        # Clean up temp file
        if temp_filename and os.path.exists(temp_filename):
            os.unlink(temp_filename)

    # Find the best price for each product
    best_prices = {}
    for product_name, country_prices in product_prices.items():
        if not country_prices:
            continue

        # Find the lowest price
        lowest_price = None
        lowest_country = None

        for country_code, price_data in country_prices.items():
            price = price_data['price']

            # Convert to float for comparison
            try:
                price_value = float(price)
            except (ValueError, TypeError):
                continue

            if lowest_price is None or price_value < lowest_price:
                lowest_price = price_value
                lowest_country = country_code

        if lowest_country:
            best_prices[product_name] = country_prices[lowest_country]

    return best_prices

def display_best_prices(best_prices, pretty=False):
    """Display the best prices for each product"""
    if not best_prices:
        print("No products found in wishlist or prices could not be determined.")
        return

    if pretty:
        # Pretty table format
        product_width = max(len(product) for product in best_prices.keys()) + 2
        price_width = 10
        currency_width = 8
        country_width = 20

        header = f"{'Product':<{product_width}} {'Price':<{price_width}} {'Currency':<{currency_width}} {'Country'}"
        print(header)
        print("-" * len(header))

        for product, price_data in best_prices.items():
            print(f"{product:<{product_width}} {price_data['price']:<{price_width}} {price_data['currency']:<{currency_width}} {price_data['country_name']}")
    else:
        # Simple format
        for product, price_data in best_prices.items():
            print(f"{product} - {price_data['price']} {price_data['currency']} - {price_data['country_name']}")

def main():
    args = init_parser().parse_args()

    if args.wishlist:
        logging.info(f"Fetching wishlist for user: {args.wishlist}")
        best_prices = process_wishlist(args.wishlist, args.normalize)
        display_best_prices(best_prices, args.pretty)
    elif args.url:
        if "gogdb.org" in args.url:
            product_id = args.url.split("/")[-1]
        else:
            product_id = extract_product_id(args.url)
        request_prices(product_id, args.normalize)
        sort_prices()
        out_result(args.count, args.pretty)
    else:
        print("Please provide either a URL (-u) or a wishlist username (-w)")


def init_parser():
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", type=str, help="url to scrape")
    parser.add_argument("-n", "--normalize", action="store_true", help="normalize currencies to USD")
    parser.add_argument("-c", "--count", type=int, default=10, help="number of countries to show")
    parser.add_argument("-p", "--pretty", action="store_true", help="shows result as pretty table")
    parser.add_argument("-w", "--wishlist", type=str, help="username to fetch wishlist for")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose logging")
    return parser


if __name__ == "__main__":
    args = init_parser().parse_args()
    setup_logging(args.verbose)
    main()
