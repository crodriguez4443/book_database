from models import (Base, session, Book, engine)
import datetime
import csv
import time


def menu():
    while True:
        print(''' 
            \nProgramming books
            \r1) Add book
            \r2) View all books
            \r3) Search for books
            \r4) Book analysis
            \r5) Exit''')
        choice = input('what would you like to do?')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print('\nChoose an option above! \nAnd press ENTER')

def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except:
        input('''
            \n %%%%%% DATE ERROR %%%%%
            \r Incorrect date format
            \r Ex January 13, 2003
            \r Press enter to try again
            \r %%%%%%%%%%%%%%%%%%%%%%%%
            \r''')
    else:
        return return_date

def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
                    \n %%%%%% PRICE ERROR %%%%%
                    \r Incorrect price format. Should not have currency symbol
                    \r Ex 10.99 and not $10.99
                    \r Press enter to try again
                    \r %%%%%%%%%%%%%%%%%%%%%%%%
                    \r''')
    else:
        return int(price_float * 100)

def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                print(row)
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Book(title=title, author=author, published_date=date, price=price)
                session.add(new_book)
        session.commmit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # add book
            title = input("Title: ")
            author = input("Author: ")
            date_error = True
            while date_error:
                date = input("Published date: (ex: October 25, 2017) ")
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input("Price: (ex: 25.65) ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author} | {book.price}')
                input('\nPress enter to return tot he main menu.')
        elif choice == '3':
            #search
            pass
        elif choice == '4':
            #book analysis
            pass
        else:
            print('bye, you have exited')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
    for book in session.query(Book):
        print(book)