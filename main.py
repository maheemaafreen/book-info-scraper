import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com"

#RETRIEVING FUNCTION
def retrieve_webpage():
    response = requests.get(url)
    response.raise_for_status()
    return response
####################

response = retrieve_webpage()

#SOUP PARSING
def create_soup():
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
#############

soup = create_soup()

#FINDING THE BOOKS
def find_books():
    books = soup.find_all("article", class_="product_pod")
    return books
#################
books = find_books()

#CREATING DATA LIST
def get_book_data():
    books_data = []
    for book in books:
        title = book.h3.a["title"]
        price = float(book.find("p", class_="price_color").text.replace("Â£", ""))
        book_data = {"title": title, "price_gbp": price, "under_20": price<20}
        books_data.append(book_data)
    return books_data
###################
books_data = get_book_data()

#BOOK LIST
def show_books(books_data):
    print("~~BOOKS~~")
    for number, book_data in enumerate(books_data, 1):
        print(f"{number}. {book_data["title"]} - £{book_data["price_gbp"]:.2f}")
##########
show_books(books_data)

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
cheapest_title, cheapest_price = cheapest_book(books_data)
print(f"\nThe cheapest book is '{cheapest_title}', at £{cheapest_price}!\n")

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
highest_book, highest_price = most_expensive(books_data)
print(f"The most expensive book is '{highest_book}', at £{highest_price}!")

#BOOKS UNDER 20 QUID
def under_20(books_data):
    books_less20 = []
    for book_data in books_data:
        if book_data["under_20"]:
            books_less20.append(book_data)
    return books_less20
###################
books_less20 = under_20(books_data)
print("\n~~Books Under 20~~")
for number, book_less20 in enumerate(books_less20, 1):
    print(f"{number}. {book_less20["title"]}")
print(f"There are {len(books_less20)} books under £20.\n")

#AVERAGE COST PER BOOK
def avg_price(books_data):
    total_price = 0
    for book_data in books_data:
        total_price += book_data["price_gbp"]
    average_cost = total_price / len(books_data)
    return average_cost
######################
average_cost = avg_price(books_data)
print(f"The average book price is £{average_cost:.2f}.")

#CSV FILE
def save_to_csv(books_data):
    with open("books.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price_gbp", "under_20"])
        writer.writeheader()
        writer.writerows(books_data)
#########
save_to_csv(books_data)