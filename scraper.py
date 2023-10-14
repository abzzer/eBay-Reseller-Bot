import requests  # Used to make HTTP requests
from bs4 import (
    BeautifulSoup,
)  # Used to parse HTML (divides HTML into parts and identifies each component)
import re  # Used to seperate numbers from text

# use only BUY-IT-NOW links

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

        # the index here is each listing and we get that with each item that contains "s-item s-item__pl-on-bottom"
        # Note: I would normally utilise the .text.strip() but in the case of eBay i found that when this was used the outputs would also include <--!""--> (html comments) and other unrequired text etc so I read the documentation and found that .get_text removes all things in <> and just includes the text and strip=true works the same as .strip()
        for index, listing in enumerate(listings):
            print(f"\nListing {index + 1}:")

            # Extracting and printing the title
            # Here I used if else statement just checks that the element is not blank
            # I also found that in most the titles there was a "New listing" string so I used the replace to remove that out, equally you can use string slicing
            title = listing.find("span", {"role": "heading", "aria-level": "3"})
            print(
                "Title:",
                title.get_text(strip=True).replace("New listing", "", 1)
                if title
                else "N/A",
            )

            # Extracting and printing the date
            # Here we use select_one which uses CSS selectors because we can only find the "date" in a nested structure of classes
            date = listing.select_one(".s-item__dynamic.s-item__listingDate .BOLD")
            print("Date:", date.get_text(strip=True) if date else "N/A")

            # Extracting and printing the price
            price = listing.find(class_="s-item__price")
            print("Price:", price.get_text(strip=True) if price else "N/A")

            # Extracting and printing the shipping cost
            # I wanted to purely derive the numbers which was hard because all the shipping cost etc were texts with numbers in the middle, I thought to utilise the .isdigit() logic integrated in python but after researching I came accross the re library which was much easier to implement
            shipping_cost_element = listing.find(
                class_="s-item__shipping s-item__logisticsCost"
            )
            if shipping_cost_element:
                shipping_cost_text = shipping_cost_element.get_text(strip=True)
                # here we are basically saying we want only the numbers in the form nnn.nnn as in decimals
                shipping_cost_numbers = re.findall(r"\d+\.\d+", shipping_cost_text)
                # given that shipping_cost_numbers print it basically
                shipping_cost = (
                    " ".join(shipping_cost_numbers) if shipping_cost_numbers else "Free"
                )
            else:
                shipping_cost = "Free"

            print("Shipping Cost:", shipping_cost)

            # Extracting and printing the URL
            # Note that the URL was located in the tag itself so I didnt want to use .get_text because that would remove the url so instead I used[""] which basically finds an attribute located in the text called href it will take it and extract the text within it
            url = listing.find(class_="s-item__link")
            print("URL:", url["href"] if url and url.has_attr("href") else "N/A")

    else:
        print(f"Failed to retrieve content: {response.status_code}")
        # i.e either eBay is down, your internet is not working, your IP has been suspended etc. etc.
