from urllib.parse import urljoin
import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"
current_url = url
#RETRIEVING FUNCTION
def retrieve_webpage(current_url):
    try:
        response = requests.get(current_url, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException:
        print("Oops! There was a problem retrieving the webpage.")
        return None
####################
#SOUP PARSING
def create_soup(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
#############
#FINDING THE BOOKS
def find_books(soup):
    books = soup.find_all("article", class_="product_pod")
    return books
#################
#CREATING DATA LIST
def get_book_data(books):
    books_data = []
    for book in books:
        title = book.h3.a["title"]
        price = float(book.find("p", class_="price_color").text.replace("Â£", ""))
        book_data = {"title": title, "price_gbp": price}
        books_data.append(book_data)
    return books_data
###################
#BOOK LIST
def show_books(books_data):
    print("~~BOOKS~~")
    for number, book_data in enumerate(books_data, 1):
        print(f"{number}. {book_data["title"]} - £{book_data["price_gbp"]:.2f}")
##########
#CHEAPEST BOOK
def cheapest_book(books_data):
    cheapest_price = 1000
    cheapest_title = ""
    for book_data in books_data:
        if book_data["price_gbp"] < cheapest_price:
            cheapest_price = book_data["price_gbp"]
            cheapest_title = book_data["title"]
    return cheapest_title, cheapest_price
##############
#MOST EXPENSIVE BOOK
def most_expensive(books_data):
    highest_price = books_data[0]["price_gbp"]
    highest_book = books_data[0]["title"]
    for book_data in books_data:
        if book_data["price_gbp"] > highest_price:
            highest_price = book_data["price_gbp"]
            highest_book = book_data["title"]
    return highest_book, highest_price
###################
#BOOKS UNDER 20 QUID
def under_price(books_data, price_limit):
    books_under_price = []
    for book_data in books_data:
        if book_data["price_gbp"] < price_limit:
            books_under_price.append(book_data)
    return books_under_price
###################
#AVERAGE COST PER BOOK
def avg_price(books_data):
    total_price = 0
    for book_data in books_data:
        total_price += book_data["price_gbp"]
    average_cost = total_price / len(books_data)
    return average_cost
######################
#CSV FILE
def save_to_csv(books_data):
    with open("books.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price_gbp"])
        writer.writeheader()
        writer.writerows(books_data)
#########
print(requests.get(url))

books_data = []
current_page = 1
while current_url:
    print(f"Scraping page {current_page}/50...")
    response = retrieve_webpage(current_url)
    if response is None:
        break
    soup = create_soup(response)
    books = find_books(soup)
    books_data.extend(get_book_data(books))
    next_link = soup.find("a", string="next")
    if next_link:
        next_url = urljoin(current_url, next_link["href"])
        current_url = next_url
        current_page += 1
    else:
        break
while True:
    try:
        price_limit = float(input("Enter a price limit: "))
        if price_limit <= 0 or (price_limit*100)%1 != 0:
            print("Oops! Please enter a valid price.")
        else:
            break
    except ValueError:
        print("Oops! Please enter a number.")

#cheapest_title, cheapest_price = cheapest_book(books_data)
#print(f"The cheapest book is '{cheapest_title}', at £{cheapest_price:.2f}!\n")

#highest_title, highest_price = most_expensive(books_data)
#print(f"The most expensive book is '{highest_title}', at £{highest_price:.2f}!\n")

books_under_price = under_price(books_data, price_limit)
print(f"There are {len(books_under_price)} books under £{price_limit:.2f}.\n")

#average_cost = avg_price(books_data)
#print(f"The average book price is £{average_cost:.2f}.")

save_to_csv(books_data)