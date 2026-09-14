import requests
from bs4 import BeautifulSoup

response = requests.get("https://books.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")
books_data = []
for book in books:
    title = book.h3.a["title"]
    price = float(book.find("p", class_="price_color").text.replace("Â£", ""))
    book_data = {"title": title, "price": price}
    books_data.append(book_data)
    #print(title, price)
#print(books_data)

#CHEAPEST BOOK
cheapest_price = 1000
cheapest_book = ""
for book_data in books_data:
    if book_data["price"] < cheapest_price:
        cheapest_price = book_data["price"]
        cheapest_book = book_data["title"]
print(f"The cheapest book is '{cheapest_book}', at £{cheapest_price}!")
##############

#MOST EXPENSIVE BOOK
highest_price = 0
highest_book = ""
for book_data in books_data:
    if book_data["price"] > highest_price:
        highest_price = book_data["price"]
        highest_book = book_data["title"]
print(f"The most expensive book is '{highest_book}', at £{highest_price}!")
###################

#BOOKS UNDER 20 QUID
books_less20 = []
for book_data in books_data:
    if book_data["price"] < 20:
        books_less20.append(book_data)
print("\n~~Books Under 20~~")
for number, book_less20 in enumerate(books_less20, 1):
    print(f"{number}. {book_less20["title"]}")
print(f"There are {len(books_less20)} books under £20.")
###################

#AVERAGE COST PER BOOK
total_price = 0
for book_data in books_data:
    total_price += book_data["price"]
average_cost = total_price / len(books_data)
print(f"The average book price is £{average_cost:.2f}.")
print("~~BOOKS~~")
for number, book_data in enumerate(books_data, 1):
    print(f"{number}. {book_data["title"]} - £{book_data["price"]:.2f}")
######################

#SORT BY PRICE
books_sorted = sorted(books_data, key=lambda book_data: book_data["price"], reverse=True)
for book_data in books_sorted:
    print(book_data["title"], book_data["price"])





