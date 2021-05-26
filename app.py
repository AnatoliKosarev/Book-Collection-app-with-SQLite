from utils import database

MENU_OPTION_MESSAGE = """
Please choose one of the following options:
- 'a' to add a new book
- 'l' to list all available books
- 'r' to mark a book as read
- 'd' to delete a book
- 'q' to quit the program

Enter here: """
PROMPT_AUTHOR_MESSAGE = "Please enter author of the book, {action}"
PROMPT_NAME_MESSAGE = "Please enter name of the book, {action}"
BOOK_INFO_DISPLAY_TEMPLATE = "\"{name}\" by {author}, status: {status}"
MISSING_VALUE_MESSAGE = "{parameter} parameter missing, please try again"


def prompt_add_book():
    action = "you'd like to add: "
    name = input(PROMPT_NAME_MESSAGE.format(action=action)).strip().title()
    author = input(PROMPT_AUTHOR_MESSAGE.format(action=action)).strip().title()
    if name and author:
        database.add_book(name, author)
    else:
        print(MISSING_VALUE_MESSAGE.format(parameter="Name or author"))


def list_available_books():
    books = database.get_book_collection()
    for book in books:
        status = "Read" if book["read"] else "Not Read"
        print(BOOK_INFO_DISPLAY_TEMPLATE.format(name=book['name'], author=book['author'], status=status))


def prompt_mark_book_as_read():
    action = "you'd like to mark as read: "
    name = input(PROMPT_NAME_MESSAGE.format(action=action)).strip().title()
    if name:
        database.mark_book_as_read(name)
    else:
        print(MISSING_VALUE_MESSAGE.format(parameter="Name"))


def prompt_delete_book():
    action = "you'd like to delete: "
    name = input(PROMPT_NAME_MESSAGE.format(action=action)).strip().title()
    if name:
        database.delete_book(name)
    else:
        print(MISSING_VALUE_MESSAGE.format(parameter="Name"))


options = {
    'a': prompt_add_book,
    'l': list_available_books,
    'r': prompt_mark_book_as_read,
    'd': prompt_delete_book
}


def menu():
    user_input = input(MENU_OPTION_MESSAGE)
    while user_input != 'q':
        if user_input in options:
            user_selection = options[user_input]
            database.create_db_table()
            if user_input != 'a' and not database.get_book_collection():  # option l or r or d selected when book collection is empty
                print("Your book collection is empty. PLease add books to collection first.")
            else:
                user_selection()
        else:
            print("Invalid selection. Please try again.")

        user_input = input(MENU_OPTION_MESSAGE)


menu()
