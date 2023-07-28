# Game Price Checker 💵

The **Game Price Checker** is a Python script that allows you to extract a URL from the clipboard, download the web page content, and retrieve the price of a game from the GOG API. The script is designed to work on macOS systems.

## Requirements

- Python 3.x
- Requests library (for making HTTP requests)
- Regular expressions (re) module
- Threading module (for concurrent requests)
- Logging module (for logging)

## How to Use

1. Copy a URL containing a game page (e.g., `https://www.gog.com/game/diablo`) to the clipboard.

2. Run the Python script with the following arguments:

    - `-u`, `--url`: The URL of the game page to scrape (required).
    - `-n`, `--normalize`: (Optional) Normalize currencies to USD.
    - `-c`, `--count` : (Optional) default = 10, number of countries to show in sorted prices result
    - `-p`, `--pretty` : (Optional) shows result as pretty table

Example:
```
python app.py -u https://www.gog.com/game/diablo -n -p
>>>...
>>>
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

3. The script will download the web page, extract the product ID, and fetch the price from the GOG API for multiple countries concurrently using threads.

4. The prices for different countries will be displayed in descending order of value. If the `-n` flag is provided, the prices will be normalized to USD.

## Limitations

- The script uses regular expressions to extract the product ID and prices, which might not handle all possible web page structures or API responses. Some pages may require additional parsing logic.
- The API endpoint used to fetch prices is specific to GOG, and it may change over time. Ensure the API remains accessible and the script is updated accordingly.

## Important Note

- The script is provided as-is, and it is advisable to use it responsibly and in accordance with the website's terms of use. Automated scraping of websites can put a strain on their servers, so use the script with caution and avoid making excessive requests.

## Credits

- This script is provided as an educational example and is not intended for commercial purposes. It was created as part of a task and is not an official GOG product.

## License

- The **Game Price Checker** Python script is released under the [MIT License](LICENSE). Feel free to modify and distribute the script according to the terms of the license.

## Disclaimer

- The author of this script is not responsible for any misuse or consequences of using the script on unauthorized websites. Always make sure you have the right to access and use the data from the websites you interact with.
