import requests  # Used to make HTTP requests - make sure to pip install
from bs4 import (
    BeautifulSoup,
)  # Used to parse HTML (divides HTML into parts and identifies each component) - make sure to pip install
import re  # Used to seperate numbers from text
import time  # Used to make file run periodically
import json  # locally store the sent URLs to ensure only new is sent

# use only BUY-IT-NOW links


# we need to ask user for webhook first of all
def get_discord_webhook():
    while True:
        url_webhook = input("Please enter your Discord webhook URL: ")
        # first we check if format is correct
        if url_webhook.startswith("https://discordapp.com/api/webhooks/"):
            # Here the user can easily make a mistake in typing or pasting so I chose to send a test message to check if teh webhook succesfully connected
            test_message = {
                "content": "This is a test message to see if we are connected"
            }
            # saw on stack overflow how you can send to discord via the requests library
            response = requests.post(url_webhook, data=test_message)
            # 204 is the code that shows the webhook is connected according to documentation
            if response.status_code == 204:
                print("Test message sent successfully!")
                return url_webhook
            else:
                print(
                    "Failed to send test message. Please check the webhook URL and try again."
                )
        else:
            print("Invalid URL. Please enter a valid Discord webhook URL.")


webhook_url = get_discord_webhook()


def load_sent_urls():
    try:
        with open("sent_urls.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


sent_url = load_sent_urls()  # list of URLs we already sent


def save_sent_urls(sent_url):
    with open("sent_urls.json", "w") as file:
        json.dump(sent_url, file)


def send_to_discord(content):
    # Sending a message to Discord channel
    payload = {"content": content}
    requests.post(webhook_url, data=payload)
    if response.status_code == 204:
        # Basically if our request goes through ie status code 204 according to documentation we add the url to sent urls temporarily and also save it to the json
        sent_url.append(url)
        save_sent_urls(sent_url)


# Basically just return true if we have listing already in list then dont return
def is_new_listing(listing, sent_url):
    listing_url = (
        listing.find(class_="s-item__link")["href"]
        if listing.find(class_="s-item__link")
        else None
    )

    if listing_url and listing_url not in sent_url:
        return True
    return False


url = input(
    "Please enter the eBay URL: "
)  # here you are asked for the URL of your item


if "ebay.co.uk" not in url:
    print("Please provide a valid eBay URL.")

else:
    response = requests.get(url)

    """" The "200" is a HTTP status code which shows that a connection was established
    using the TCP/IP protocol (basically the server saying ok you can access the site) & 
    the request for the HTML file was fulfilled (i.e you are now on the website and 
    have access to the html file)"""

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")  # Parsing with lxml
        listings = soup.find_all(class_="s-item s-item__pl-on-bottom")
        # We want a list of prices so we can just keep adding to it
        prices = []
        # I know we derive the listing prices twice in this whole script but it was important for the functionality I wanted, However if you find a better way feel free to push request
        # Here we evaluate each listing alone derive its text and then use this really cool library I found called re which essentially saves you having to check every character using the .isdigit() binary logic
        for listing in listings:
            price_element = listing.find(class_="s-item__price")
            if price_element:
                price_text = price_element.get_text(strip=True)
                match = re.search(r"\d+\.\d+", price_text)
                if match:
                    prices.append(float(match.group()))
        # now I just sorted to make it more useful in the next steps
        prices = sorted(prices)

        # Here I made a function that ensures the user only inputs numbers and nothing else

        def get_user_input(prompt):
            while True:
                user_input = input(prompt)
                try:
                    return float(user_input)
                except ValueError:
                    print("Invalid input. Please enter a number only.")

        """ User input - these are the values that are more important - the lowest price the item is currenly in the market for that you deep not worth paying, 
        how much you want your profit margin to be and the lowest price you would pay for a genuine product i.e you cant get ps5 for less than 200 if it is real as of 2023"""

        lowest_price = float(
            get_user_input("Enter the lowest price of your item on the market: ")
        )
        profit_margin = float(get_user_input("Enter desired profit margin: "))
        min_price = float(
            get_user_input("Enter the lowest price you will buy the item for: ")
        )

        # Ensure min_price is valid
        average_price = sum(prices) / len(prices) if prices else 0
        while min_price >= lowest_price - profit_margin:
            print("Ensure lowest price is less than (lowest price - profit margin).")
            min_price = float(input("Enter minimum price: "))

        # Calculating average market price excluding items priced below the lowest price again we use another list, it is easier to deal with items this way - note I could have used num.py
        valid_prices = [p for p in prices if p > lowest_price]
        average_valid_price = (
            sum(valid_prices) / len(valid_prices) if valid_prices else 0
        )

        print(
            f"Average market price (excluding items below {lowest_price}): {average_valid_price:.2f}"
        )

        count_list = 0

        # the index here is each listing and we get that with each item that contains "s-item s-item__pl-on-bottom"
        # Note: I would normally utilise the .text.strip() but in the case of eBay i found that when this was used the outputs would also include <--!""--> (html comments) and other unrequired text etc so I read the documentation and found that .get_text removes all things in <> and just includes the text and strip=true works the same as .strip()
        for index, listing in enumerate(listings):
            # Check if it is a new listing
            if not is_new_listing(listing):
                continue
            price_element = listing.find(class_="s-item__price")
            # Here I just made sure to refind the prices but on an item by item basis, compare them to the values we already have and if it is a match ie it is greater than minimum and meets profit margin then the script is ran
            if price_element:
                price_text = price_element.get_text(strip=True)
                match = re.search(r"\d+\.\d+", price_text)
                # This wasnt mandatory but I found some items that were glitched broke the code so I had to make sure that match existed before I make a float
                if match:
                    price = float(match.group())
                    if min_price < price < (lowest_price - profit_margin):
                        count_list += 1
                        # Here I defined content element so it makes it easy to print to discord via concatination
                        content = f"\nListing {count_list}:\n"
                        # Extracting and printing the title
                        # Here I used if else statement just checks that the element is not blank
                        # I also found that in most the titles there was a "New listing" string so I used the replace to remove that out, equally you can use string slicing
                        title = listing.find(
                            "span", {"role": "heading", "aria-level": "3"}
                        )
                        content += f"Title: {title.get_text(strip=True).replace('New listing', '', 1) if title else 'N/A'}\n"

                        # Extracting and printing the date
                        # Here we use select_one which uses CSS selectors because we can only find the "date" in a nested structure of classes
                        date = listing.select_one(
                            ".s-item__dynamic.s-item__listingDate .BOLD"
                        )
                        content += (
                            f"Date: {date.get_text(strip=True) if date else 'N/A'}"
                        )

                        # Printing the price element
                        content += f"Price: {price_text}\n"

                        # Extracting and printing the shipping cost
                        # I wanted to purely derive the numbers which was hard because all the shipping cost etc were texts with numbers in the middle, I thought to utilise the .isdigit() logic integrated in python but after researching I came accross the re library which was much easier to implement
                        shipping_cost_element = listing.find(
                            class_="s-item__shipping s-item__logisticsCost"
                        )
                        if shipping_cost_element:
                            shipping_cost_text = shipping_cost_element.get_text(
                                strip=True
                            )
                            # here we are basically saying we want only the numbers in the form nnn.nnn as in decimals
                            shipping_cost_numbers = re.findall(
                                r"\d+\.\d+", shipping_cost_text
                            )
                            # given that shipping_cost_numbers print it basically
                            shipping_cost = (
                                " ".join(shipping_cost_numbers)
                                if shipping_cost_numbers
                                else "Free"
                            )
                        else:
                            shipping_cost = "Free"

                        content += f"Shipping Cost: {shipping_cost}\n"

                        # Extracting and printing the URL
                        # Note that the URL was located in the tag itself so I didnt want to use .get_text because that would remove the url so instead I used[""] which basically finds an attribute located in the text called href it will take it and extract the text within it
                        url = listing.find(class_="s-item__link")
                        content += f"URL: {url['href'] if url and url.has_attr('href') else 'N/A'}\n"

                        send_to_discord(f"NEW PROFITABLE LISTING! \n\n {content} \n\n")
                    count_list = 0

    else:
        print(f"Failed to retrieve content: {response.status_code}")
        # i.e either eBay is down, your internet is not working, your IP has been suspended etc. etc.
