# ----------------------EBAY WEBSCRAPER FOR RESELLING----------------------

Welcome to this project. This project is a webscraper designed to work on EBAY.co.uk

## Description
*eBay Webscraper for Reselling* is a Python application crafted to assist online resellers or purchasers in identifying profitable listings on eBay.co.uk. By leveraging web scraping technologies, it scrutinizes the specified eBay listing page and alerts the user via Discord when it spots listings that meet a profitable range, determined by the user's desired profit margin and purchase price thresholds.

## What it Does
Upon providing an eBay.co.uk URL, the application fetches, parses, and evaluates the listings on the page. The user is prompted to input a desired profit margin, minimum acceptable purchase price, and the lowest market price for an item. These parameters are crucial for sifting through ingenuine products and establishing a meaningful profit calculation baseline. Then, the application scans through each listing, extracting vital information like price, shipping cost, and URL. If it identifies a listing within the user-defined profitable range, it sends a notification to a specified Discord channel through a webhook, sharing pertinent listing details.

**Note:** Extensive market knowledge is required to set the lowest market price parameter effectively. Although an automation for it is desirable, markets vary significantly, requiring user insights to optimize the parameter effectively.

## Technologies Used
- **Beautiful Soup:** Engaged for parsing HTML and extracting necessary information from eBay listings due to its substantial efficacy in web scraping.
- **Requests:** Deployed for making HTTP requests because of its simplicity and ability to manage HTTP requests succinctly.
- **JSON:** Utilized to store previously sent URLs to circumvent redundant notifications and to store your webhook link, ensuring you don't have to reinsert it repeatedly.
- **Regex (re):** Employed to extract numerical values from strings, supporting accurate pricing information analysis.

## Challenges and Future Features
### Challenges
Managing varied listing formats, maintaining connections with eBay to persistently scrape without restrictions and circumventing IP bans, establishing and storing discord webhooks effectively in JSON, defining functions to minimize repetition, and ensuring notifications are sent reliably and formatted correctly have posed significant challenges in this project.

### Future Features
Anticipation is towards the integration of AI to better filter and identify highly profitable listings and potentially AUTO purchase listings that depict tremendous profitability. Enabling multiple URLs to run in parallel, storing URLs in JSON, and expanding compatibility with other websites to automate the discovery of new drops is also in the pipeline.

```shell
pip install json
pip install beautifulsoup4
pip install requests
```



## Steps
1. **Download:** Obtain the project by downloading it as a zip file from the repository.
2. **Extract:** Extract the downloaded zip file to your preferred location.
3. **Change Scrape Time:** Open `scraper.py`, scroll to the bottom, and modify `time.sleep(30)`. Note: this value is in seconds but ensure it is not less than 2-3 minutes to avoid IP suspension.
4. **Run:** Navigate to the project directory and open the `RUNME` file.

## Usage
- **Setup Discord Webhook:** Create a Discord webhook and provide its URL when prompted by the application.
- **Input eBay URL:** Provide the eBay.co.uk URL of the listings page you wish to monitor.
- **Configure Parameters:** Input the desired profit margin (how much below the current lowest non-profitable price in the market), lowest acceptable purchase price (to ensure product is authentic), and how much below the current lowest non-profitable price in the market.
- **Receive Notifications:** The application will send notifications to your Discord channel when it identifies listings within your defined profitable range.

## License
This project is licensed under the GNU General Public License. See the `LICENSE` file for details.

