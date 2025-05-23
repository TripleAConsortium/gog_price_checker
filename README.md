# Game Price Checker 💵
[![PyPI](https://img.shields.io/pypi/v/gog-price-checker)](https://pypi.org/project/gog-price-checker/)
![Latest build status](https://github.com/iampopovich/gog_price_checker/workflows/upload-python-package/badge.svg)

The **Game Price Checker** is a Python script that allows you to check game prices from the GOG API. It can fetch prices for individual games by URL or compare prices across your entire GOG wishlist to find the best deals across different countries.

## Requirements

- Python 3.x
- Requests library (for making HTTP requests)
- Regular expressions (re) module
- Threading module (for concurrent requests)
- Logging module (for logging)

## Installation
```
pip install gog-price-checker
```

## How to Use

1. Copy a URL containing a game page (e.g., `https://www.gog.com/game/diablo`) to the clipboard.

2. Run the Python script with the following arguments:

    - `-u`, `--url`: The URL of the game page to scrape.
    - `-w`, `--wishlist`: Username to fetch wishlist for (e.g., your GOG username).
    - `-n`, `--normalize`: (Optional) Normalize currencies to USD.
    - `-c`, `--count` : (Optional) default = 10, number of countries to show in sorted prices result.
    - `-p`, `--pretty` : (Optional) Shows result as pretty table.
    - `-v`, `--verbose` : (Optional) Enable verbose logging.

Examples:

**Check prices for a single game:**
```
gog-price-checker -u https://www.gog.com/game/diablo -n -p
```

**Check prices for your entire wishlist:**
```
gog-price-checker -w your_gog_username -p
```
Output:
```
Country                   Price      Currency
---------------------------------------------
Ukraine                   5.51       USD
Moldova                   5.51       USD
Kazakhstan                5.51       USD
Armenia                   5.51       USD
China                     5.57       USD
Poland                    8.34       USD
Australia                 9.24       USD
New Zealand               9.24       USD
Andorra                   9.99       USD
Spain                     9.99       USD
Sweden                    9.99       USD
...
```

3. For single game checks, the script will download the web page, extract the product ID, and fetch the price from the GOG API for multiple countries concurrently using threads.

4. For wishlist checks, the script will fetch your wishlist for each country and find the best price for each game.

5. The prices will be displayed in ascending order (cheapest first). If the `-n` flag is provided, the prices will be normalized to USD.

## Limitations

- The script uses regular expressions to extract the product ID and prices, which might not handle all possible web page structures or API responses. Some pages may require additional parsing logic.
- The API endpoint used to fetch prices is specific to GOG, and it may change over time. Ensure the API remains accessible and the script is updated accordingly.
- Wishlist functionality requires a public GOG wishlist. Private wishlists cannot be accessed.

## Important Note

- The script is provided as-is, and it is advisable to use it responsibly and in accordance with the website's terms of use. Automated scraping of websites can put a strain on their servers, so use the script with caution and avoid making excessive requests.

## Credits

- This script is provided as an educational example and is not intended for commercial purposes. It was created as part of a task and is not an official GOG product.

## License

- The **Game Price Checker** Python script is released under the [MIT License](LICENSE). Feel free to modify and distribute the script according to the terms of the license.

## Disclaimer

- The author of this script is not responsible for any misuse or consequences of using the script on unauthorized websites. Always make sure you have the right to access and use the data from the websites you interact with.
