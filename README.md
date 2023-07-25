# Game Price Checker 💵

The **Game Price Checker** is an AppleScript script that allows you to extract a URL from the clipboard, download the web page content, and retrieve the price of a game from the GOG API. The script is designed to work on macOS systems.

## Requirements

- macOS operating system.
- AppleScript is pre-installed on macOS and doesn't require additional installations.

## How to Use

1. Copy a URL containing a game page (e.g., `https://www.gog.com/game/diablo`) to the clipboard.

2. Run the **Game Price Checker** AppleScript.

3. The script will download the web page, extract the product ID, and fetch the price from the GOG API.

4. A dialog box will be displayed, showing the name of the game and its price in the specified country (Argentina by default).

## Limitations

- The script uses basic shell commands and regular expressions, which might not handle all possible web page structures or API responses. Some pages may require additional parsing logic.
- The script fetches the price based on the specified `countryCode`, which is set to "AR" (Argentina) by default. You may modify the script to use a different country code as needed.

## Important Note

- The script is provided as-is, and it is advisable to use it responsibly and in accordance with the website's terms of use. Automated scraping of websites can put a strain on their servers, so use the script with caution and avoid making excessive requests.

## Credits

- This script is provided as an educational example and is not intended for commercial purposes. It was created as a part of a task and is not an official GOG product.

## License

- The **Game Price Checker** AppleScript is released under the [MIT License](LICENSE). Feel free to modify and distribute the script according to the terms of the license.

## Disclaimer

- The author of this script is not responsible for any misuse or consequences of using the script on unauthorized websites. Always make sure you have the right to access and use the data from the websites you interact with.
