----------------------EBAY WEBSCRAPER FOR RESELLING----------------------

Welcome, this project. This project is a webscraper that works on EBAY.com

Description
eBay webscraper for resellling is a Python application designed to help online resellers or purchasers identify profitable listings on eBay.co.uk. Utilizing web scraping technologies, it inspects the specified eBay listing page and notifies the user via Discord when it identifies listings that fall within a profitable range, defined by the user's desired profit margin and purchase price limits.



What it Does
Upon providing an eBay.co.uk URL, the application retrieves, parses, and analyzes the listings on the page. The user is prompted to input a preferred profit margin, minimum acceptable purchase price (I did this because when listings are shown on ebay there are a lot of ingenuine products this allows you to filter them out), and the lowest market price for an item (this is purely to: calculate the mean and not let the mean be effected by other ingenuine products and it was also to calculate the profit margin i.e say we have object x with the lowest possible listing where you will cut even being £300 to make profit as a reseller we ideally want to buy something cheaper then 300 so that we are able to resell it so this parameter is used to calculate the maxmimum listing proce) (NOTE: this parameter is heavily based on your knowledge of the market I wanted to automate it but all markets are different just find what parameter works best for you). Then, it scans through each listing, extracting essential information like price, shipping cost, and URL. If it finds a listing within the user-defined profitable range, it sends a notification to a specified Discord channel through a webhook, providing relevant listing details.



Technologies Used
Beautiful Soup: Utilized for parsing HTML and extracting the needed information from eBay listings due to its robustness and efficiency in web scraping.
Requests: Employed for making HTTP requests due to its simplicity and capability to send HTTP requests succinctly.
JSON: Applied to store previously sent URLs to avoid redundant notifications, also used to store your webhook link so you dont have to keep inserting it over and over again.
Regex (re): Used for extracting numerical values from strings, aiding in the precise analysis of pricing information.
Challenges and Future Features


Challenges and future features:

Challenges: Handling varied listing formats and extracting specific data before finding regex, managing connections with eBay to continually scrape without restrictions and IP bans, Ensuring discord webhooks were properly established and stored into JSON, Defining functions to avoid repetitions and ensuring that notifications are reliably sent and formatted correctly.

Future Features: Integrate AI to better filter and identify highly profitable listings even at some point AUTO purchase listings that are very profitable, Letting multiple URLs run parallele, Storing URLs in JSON and expand compatibility with other websites to automate finding new drops.


Pre-requisites:
Ensure to have Python and pip installed. Then, run the following commands to install necessary packages:
    pip install json
    pip install beautifulsoup4
    pip install requests



Steps:
Download: Obtain the project by downloading it as a zip file from the repository.
Extract: Extract the downloaded zip file to your preferred location.
Change scrape time: Open scraper.py scroll to bottom change time.sleep(30) - this is in seconds but dont let it be less than 2-3 minutes otherwise your IP will get suspended
Run: Navigate to the project directory and open the RUNME file.
Usage
Setup Discord Webhook: Create a Discord webhook and provide its URL when prompted by the application.
Input eBay URL: Provide the eBay.co.uk URL of the listings page you wish to monitor.
Configure Parameters: Input the desired profit margin (how much below the current lowest non-profitable price in the market is), lowest acceptable purchase price(to ensure product is authentic), and how much below the current lowest non-profitable price in the market.
Receive Notifications: The application will send notifications to your Discord channel when it finds listings within your defined profitable range.



License
This project is licensed under the GNU General Public License. See the LICENSE file for details.
