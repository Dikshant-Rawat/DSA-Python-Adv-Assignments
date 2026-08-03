class LibraryManagementSystem:
    def _init_(self):
        # Sample Initial Data: Pre-populating books
        self.books = {
            "B101": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "is_issued": False, "issued_to": None},
            "B102": {"title": "To Kill a Mockingbird", "author": "Harper Lee", "is_issued": False, "issued_to": None},
            "B103": {"title": "1984", "author": "George Orwell", "is_issued": False, "issued_to": None}
        }
        # Sample Initial Data: Pre-populating users
        self.users = {
            "U001": {"name": "Alice Johnson", "issued_books": []},
            "U002": {"name": "Bob Smith", "issued_books": []}
        }

    # Helper function to check if User exists
    def find_user(self, user_id):
        return self.users.get(user_id)

    # Helper function to check if Book exists
    def find_book(self, book_id):
        return self.books.get(book_id)

    # 1. Update User
    def update_user(self):
        print("\n---  Update User Details ---")
        user_id = input("Enter User ID to update (e.g., U001): ").strip()
        user = self.find_user(user_id)

        if not user:
            print(f"User ID '{user_id}' not found in system!")
            return

        print(f"User Found: {user['name']}")
        new_name = input("Enter new name (leave blank to keep current): ").strip()
        if new_name:
            user["name"] = new_name
            print("User name updated successfully.")

    # 2. Update Book
    def update_book(self):
        print("\n--- Update Book Details ---")
        book_id = input("Enter Book ID to update (e.g., B101): ").strip()
        book = self.find_book(book_id)

        if not book:
            print(f"Book ID '{book_id}' not found in system!")
            return

        print(f"Book Found: '{book['title']}' by {book['author']}")
        new_title = input("Enter new Title (leave blank to keep current): ").strip()
        new_author = input("Enter new Author (leave blank to keep current): ").strip()

        if new_title:
            book["title"] = new_title
        if new_author:
            book["author"] = new_author
        print("Book details updated successfully.")

    # 3 & 7. Borrow a Book
    def borrow_book(self):
        print("\n---Borrow / Issue a Book ---")
        book_id = input("Enter Book ID: ").strip()
        book = self.find_book(book_id)

        # Check if Book is found
        if not book:
            print(f"Book ID '{book_id}' not found in system!")
            return
        
        print(f"Book Found: '{book['title']}'")

        if book["is_issued"]:
            borrower = self.users.get(book["issued_to"], {}).get("name", "Unknown")
            print(f"Book is already issued to {borrower} (User ID: {book['issued_to']}).")
            return

        # Asking for User ID and validating user exists
        user_id = input("Enter User ID borrowing the book: ").strip()
        user = self.find_user(user_id)

        # Check if User is found
        if not user:
            print(f"User ID '{user_id}' not found in system!")
            add_now = input("Would you like to register this new user? (y/n): ").strip().lower()
            if add_now == 'y':
                name = input(f"Enter name for new User '{user_id}': ").strip()
                self.users[user_id] = {"name": name, "issued_books": []}
                user = self.users[user_id]
                print(f"User '{name}' created.")
            else:
                return

        print(f"User Found: {user['name']}")

        # Issue book and update records
        book["is_issued"] = True
        book["issued_to"] = user_id
        user["issued_books"].append(book_id)

        print(f"Success! '{book['title']}' has been issued to {user['name']} (User ID: {user_id}).")

    # 4. Display which book is issued to which user
    def display_issued_books(self):
        print("\n--- Issued Books & User Mapping ---")
        issued_books = [b_id for b_id, b in self.books.items() if b["is_issued"]]

        if not issued_books:
            print("No books are currently issued.")
            return

        print(f"{'Book ID':<10} | {'Book Title':<25} | {'User ID':<10} | {'User Name'}")
        print("-" * 65)
        for b_id in issued_books:
            book = self.books[b_id]
            u_id = book["issued_to"]
            user = self.users.get(u_id, {})
            u_name = user.get("name", "Unknown User")
            print(f"{b_id:<10} | {book['title']:<25} | {u_id:<10} | {u_name}")

    # 5. Add a Book
    def add_book(self):
        print("\n--- ➕ Add a Book ---")
        book_id = input("Enter new Book ID: ").strip()
        if book_id in self.books:
            print("A book with this ID already exists!")
            return

        title = input("Enter Book Title: ").strip()
        author = input("Enter Author Name: ").strip()

        self.books[book_id] = {
            "title": title,
            "author": author,
            "is_issued": False,
            "issued_to": None
        }
        print(f"Book '{title}' (ID: {book_id}) added successfully.")

    # 6. Show All Books
    def show_all_books(self):
        print("\n--- All Books in Library ---")
        if not self.books:
            print("No books found in system.")
            return

        print(f"{'ID':<10} | {'Title':<25} | {'Author':<20} | {'Status':<12}")
        print("-" * 75)
        for b_id, details in self.books.items():
            status = f"Issued to {details['issued_to']}" if details["is_issued"] else "Available"
            print(f"{b_id:<10} | {details['title']:<25} | {details['author']:<20} | {status:<12}")

    # 8. Return a Book
    def return_book(self):
        print("\n---Return a Book ---")
        book_id = input("Enter Book ID to return: ").strip()
        book = self.find_book(book_id)

        if not book:
            print(f"Book ID '{book_id}' not found in system!")
            return

        if not book["is_issued"]:
            print("This book is currently not checked out.")
            return

        user_id = book["issued_to"]
        user = self.find_user(user_id)

        # Update records
        book["is_issued"] = False
        book["issued_to"] = None

        if user and book_id in user["issued_books"]:
            user["issued_books"].remove(book_id)

        user_name = user["name"] if user else f"ID {user_id}"
        print(f"Book '{book['title']}' successfully returned by {user_name}.")


def main():
    library = LibraryManagementSystem()

    while True:
        print("\n" + "=" * 45)
        print("        LIBRARY MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1) Update User")
        print("2) Update Book")
        print("3) Borrow a Book (Requires User ID)")
        print("4) Display Issued Books & Users")
        print("5) Add a Book")
        print("6) Show All Books")
        print("7) Borrow a Book")
        print("8) Return a Book")
        print("9) Exit")
        print("=" * 45)

        choice = input("Enter menu option: ").strip()

        if choice == '1':
            library.update_user()
        elif choice == '2':
            library.update_book()
        elif choice in ['3', '7']:
            library.borrow_book()
        elif choice == '4':
            library.display_issued_books()
        elif choice == '5':
            library.add_book()
        elif choice == '6':
            library.show_all_books()
        elif choice == '8':
            library.return_book()
        elif choice == '9':
            print("\nExiting system. Goodbye!")
            break
        else:
            print("Invalid input! Please enter a number between 1 and 9.")


if _name_ == "_main_":
    main()