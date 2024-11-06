import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
import mysql.connector
from mysql.connector import Error

# Main application window
root = tk.Tk()
root.title("Library Management System")
root.geometry("1000x700")
root.config(bg="#0baaea")

#----------------------------------------------------------------------------------------------------------------------#
# Global entry variables
entry_number_of_books_issued = None
member_code = None
entry_member_name = None
entry_member_address = None
entry_member_phone = None

entry_accession = None
entry_subject = None
entry_title = None
entry_author = None
entry_publisher = None
entry_price = None
entry_member_code = None
entry_issue_date = None

entry_accession_modify = None
entry_subject_modify = None
entry_title_modify = None
entry_author_modify = None
entry_publisher_modify = None
entry_price_modify = None
entry_member_code_modify = None
entry_issue_date_modify = None

def connect_db():
    """Connect to the database and return the connection object."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

def reports_window():
    """Create and display the reports window."""
    report = Toplevel(root)
    report.title("Reports")
    report.geometry("800x600")

    report_label = tk.Label(report, text="Reports", font=("Calibri", 25, "bold"), fg="darkblue")
    report_label.pack(pady=20)

    # Text area to display the reports
    report_display = scrolledtext.ScrolledText(report, width=80, height=15, font=("Arial", 12))
    report_display.pack(padx=20, pady=20)

    # Define report buttons
    report_buttons = [
        ("Subject Wise Book List", subject_wise_report),
        ("Books Issued to Members", books_issued_report),
        ("Books Currently in Library", books_in_library_report),
        ("List of Members", list_of_members_report),
    ]

    # Create buttons for each report
    for i, (text, command) in enumerate(report_buttons):
        button = tk.Button(report, text=text, font=("Arial", 12),
                           command=lambda cmd=command: display_report(cmd, report_display),
                           width=30)
        button.pack(pady=5)

def display_report(report_func, report_display):
    """Fetch and display the selected report."""
    report_display.delete(1.0, tk.END)  # Clear previous report
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        report = report_func(cursor)  # Call the report function and get results
        report_display.insert(tk.END, report)  # Display report in the text area
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def subject_wise_report(cursor):
    """Generate the subject-wise book list report."""
    query = "SELECT subject_code, COUNT(*) FROM library_management GROUP BY subject_code"
    cursor.execute(query)
    results = cursor.fetchall()
    report = "Subject Wise Book List:\n\n"
    for row in results:
        report += f"Subject: {row[0]}, Count: {row[1]}\n"
    return report

def books_issued_report(cursor):
    """Generate the books issued to members report."""
    query = "SELECT book_title, member_code FROM member_details WHERE book_title IS NOT NULL"
    cursor.execute(query)
    results = cursor.fetchall()
    report = "Books Issued to Members:\n\n"
    for row in results:
        report += f"Book: {row[0]}, Member Code: {row[1]}\n"
    return report

def books_in_library_report(cursor):
    """Generate the books currently in the library report."""
    query = "SELECT title FROM library_management WHERE title NOT IN (SELECT book_title FROM member_details WHERE book_title IS NOT NULL)"
    cursor.execute(query)
    results = cursor.fetchall()
    report = "Books Currently in Library:\n\n"
    for row in results:
        report += f"Book: {row[0]}\n"
    return report

def list_of_members_report(cursor):
    """Generate the list of members report."""
    query = "SELECT member_code, member_name FROM member_details"
    cursor.execute(query)
    results = cursor.fetchall()
    report = "List of Members:\n\n"
    for row in results:
        report += f"Member Code: {row[0]}, Name: {row[1]}\n"
    return report

#----------------------------------------------------------------------------------------------------------------------#
def return_book_window():
    global entry_accession  # Ensure this is declared as global
    global entry_subject
    global entry_title
    global entry_author
    global entry_publisher
    global entry_price
    global entry_member_code

    return_book_win = Toplevel(root)
    return_book_win.title("Return Book")
    return_book_win.geometry("800x600")
    return_book_win.config(bg="#0baaea")

    add_modify_label = tk.Label(return_book_win, text="Return A Book", font=("calibri", 25, "bold"), fg="darkblue", bg="#0baaea", padx=30, pady=30)
    add_modify_label.grid(row=0, column=1, columnspan=5, pady=20)

    tk.Label(return_book_win, text="Accession Number", bg="#0baaea", font=("calibri", 14), fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_accession = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_accession.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(return_book_win, text="Subject Code", bg="#0baaea", font=("calibri", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_subject = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_subject.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(return_book_win, text="Title", bg="#0baaea", font=("calibri", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_title = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_title.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(return_book_win, text="Author", bg="#0baaea", font=("calibri", 14)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_author = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_author.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(return_book_win, text="Publisher", bg="#0baaea", font=("calibri", 14)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
    entry_publisher = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_publisher.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(return_book_win, text="Price", bg="#0baaea", font=("calibri", 14)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
    entry_price = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_price.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(return_book_win, text="Member Code", bg="#0baaea", font=("calibri", 14)).grid(row=7, column=0, padx=10, pady=5, sticky="e")
    entry_member_code = tk.Entry(return_book_win, font=("Arial", 14), width=30)
    entry_member_code.grid(row=7, column=1, padx=10, pady=5)
    tk.Button(return_book_win, text="Return Book", command=return_a_book, font=("Arial", 14), width=15).grid(row=9, column=0, padx=10, pady=20, sticky="e")
    tk.Button(return_book_win, text="Clear", command=clear_fields, font=("Arial", 14), width=15).grid(row=9, column=1, padx=10, pady=20)
def return_a_book():
    # Retrieve values from entry fields
    accession_number = entry_accession.get()
    subject_code = entry_subject.get()
    title = entry_title.get()
    author = entry_author.get()
    publisher = entry_publisher.get()
    price = entry_price.get()
    member_code = entry_member_code.get()

    # Validate member code
    if not validate_member(member_code):
        messagebox.showerror("Invalid Member Code", "The member code does not exist.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()

        # Insert the book back into the library_management table
        insert_query = '''INSERT INTO library_management (accession_number, subject_code, title, author, publisher, price)
                          VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(insert_query, (accession_number, subject_code, title, author, publisher, float(price)))
        conn.commit()

        # Delete the specific book_title from member_details for the matching member_code
        delete_query = '''UPDATE member_details SET book_title = NULL WHERE member_code = %s AND book_title = %s'''
        cursor.execute(delete_query, (member_code, title))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Message", "Book Returned Successfully and Book Title Removed")
        else:
            messagebox.showinfo("Message", "Book Returned Successfully, but No Matching Title Found")

        clear_fields()

    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def validate_member(member_code):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()
        sql = "SELECT * FROM member_details WHERE member_code = %s"
        cursor.execute(sql, (member_code,))
        return cursor.fetchone() is not None  # Returns True if member exists
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#----------------------------------------------------------------------------------------------------------------------#
def fetch_all_data(search_term):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT title, author, price FROM library_management WHERE title LIKE %s', (f'%{search_term}%',))
        results = cursor.fetchall()
        conn.close()

        if results:
            return "\n".join(
                f'Title: {row[0]}, Author: {row[1]}, Price: {row[2]}' for row in results
            )
        else:
            return "No Data Found"
    except mysql.connector.Error as err:
        return f"Error: {err}"

def result_label(search):
    search_term = book_search.get()
    data = fetch_all_data(search_term)

    # Clear any existing label before displaying the new result
    for widget in search.winfo_children():
        if isinstance(widget, tk.Label) and widget != search_label:
            widget.destroy()

    display_result = tk.Label(search, text=data, font=("Product Sans", 14), bg="darkblue", fg="white")
    display_result.grid(row=9, column=1, padx=10, pady=10)

    # Show a message box if no data found
    if "No Data Found" in data:
        messagebox.showinfo("Search Result", "The book is not available.")

def open_search_window():
    search = Toplevel(root)
    search.title("Available Books")
    search.geometry("800x600")
    search.config(bg="#0baaea")

    global search_label
    search_label = tk.Label(search, text="Search Books",
                                       font=("calibri", 25, "bold"), fg="darkblue", bg="#0baaea", padx=30, pady=30)
    search_label.grid(row=0, column=1, columnspan=5, pady=20)

    global book_search
    book_search = tk.Entry(search, font=("Arial", 14), width=30)
    book_search.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(search, text="Search", command=lambda: result_label(search)).grid(row=8, column=1, padx=10, pady=20)
#----------------------------------------------------------------------------------------------------------------------#

def clear_fields():
    entry_member_code.delete(0, tk.END)
    entry_title.delete(0, tk.END)
def issue_book():
    issue_book_window = Toplevel(root)
    issue_book_window.geometry("700x700")
    issue_book_window.config(bg="lightgray")

    title = tk.Label(issue_book_window, text="Issue Book", font=("Product Sans", 40, "bold"), bg="darkblue", fg="white")
    title.grid(row=0, column=0, columnspan=2, pady=50)

    tk.Label(issue_book_window, text="Member Code", bg="lightgray", font=("Calibri", 14), fg="darkblue").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    global entry_member_code
    entry_member_code = tk.Entry(issue_book_window, font=("Arial", 14), width=30)
    entry_member_code.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(issue_book_window, text="Title", bg="lightgray", font=("Calibri", 14), fg="darkblue").grid(row=3, column=0, padx=10, pady=5, sticky="e")

    global entry_title
    entry_title = tk.Entry(issue_book_window, font=("Arial", 14), width=30)
    entry_title.grid(row=3, column=1, padx=10, pady=5)

    tk.Button(issue_book_window, text="Issue Book", font=("Arial", 14), width=12, bg="black", fg="white", command=mc_for_issue).grid(row=9, column=0, padx=10, pady=20, sticky="e")
    tk.Button(issue_book_window, text="Clear", command=clear_fields, font=("Arial", 14), width=12, bg="black", fg="white").grid(row=9, column=1, padx=10, pady=20)

def mc_for_issue():
    member_code = entry_member_code.get()
    title = entry_title.get()

    if not member_code or not title:
        messagebox.showerror("Input Error", "Please enter both Member Code and Title")
        return

    if validate_member(member_code) and validate_title(title):
        if can_issue_more_books(member_code):
            success = delete_book_record(title)
            if success:
                # Update the member's book title
                if update_member_book(member_code, title):
                    messagebox.showinfo("Message", "Book Issued Successfully")
                else:
                    messagebox.showerror("Message", "Failed to update member details")
            else:
                messagebox.showerror("Message", "Failed to issue book")
        else:
            messagebox.showerror("Message", "Cannot issue more than 3 books to a member.")
    else:
        messagebox.showerror("Message", "Invalid Member Code or Title")

def can_issue_more_books(member_code):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM member_details WHERE member_code = %s AND book_title IS NOT NULL"
        cursor.execute(sql, (member_code,))
        count = cursor.fetchone()[0]
        return count < 3  # Allows issuing if less than 3 titles are assigned
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def validate_member(member_code):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()
        sql = "SELECT * FROM member_details WHERE member_code = %s"
        cursor.execute(sql, (member_code,))
        result = cursor.fetchone()  # Fetch the result
        return result is not None  # Returns True if member exists
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()  # Ensure cursor is closed
        if conn:
            conn.close()  # Ensure connection is closed


def validate_title(title):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()
        sql = "SELECT * FROM library_management WHERE title = %s"
        cursor.execute(sql, (title,))
        result = cursor.fetchone()  # Fetch the result
        return result is not None  # Returns True if title exists
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()  # Ensure cursor is closed
        if conn:
            conn.close()  # Ensure connection is closed

def delete_book_record(title):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()
        sql_delete = "DELETE FROM library_management WHERE title = %s"
        cursor.execute(sql_delete, (title,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_member_book(member_code, title):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()
        sql_update = "UPDATE member_details SET book_title = %s WHERE member_code = %s"
        cursor.execute(sql_update, (title, member_code))
        conn.commit()
        return cursor.rowcount > 0  # Returns True if the update was successful
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#----------------------------------------------------------------------------------------------------------------------#

def add_member():
    member_code_value = member_code.get()
    member_name = entry_member_name.get()
    member_address = entry_member_address.get()
    member_phone = entry_member_phone.get()

    if not all([member_code_value, member_name, member_address, member_phone]):
        messagebox.showinfo("Input Error", "Please fill all fields.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()

        # SQL query to insert new member
        query = '''INSERT INTO member_details (member_code, member_name, member_address, member_phone)
                   VALUES (%s, %s, %s, %s)'''
        cursor.execute(query, (member_code_value, member_name, member_address, member_phone))

        conn.commit()
        messagebox.showinfo("Success", "Member Added!")
        clear_fields()

    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#----------------------------------------------------------------------------------------------------------------------#

def add_modify_member():
    add_modify_member_window = Toplevel(root)
    add_modify_member_window.title("Add Or Modify Member")
    add_modify_member_window.geometry("800x600")
    add_modify_member_window.config(bg="#0baaea")

    # Title label for the new window
    add_modify_member_label = tk.Label(add_modify_member_window, text="Add A New Member Or Update An Existing Member",
                                       font=("calibri", 25, "bold"), fg="darkblue", bg="#0baaea", padx=30, pady=30)
    add_modify_member_label.grid(row=0, column=1, columnspan=5, pady=20)

    # Member Code
    tk.Label(add_modify_member_window, text="Member Code", bg="#0baaea", font=("calibri", 14), fg="white").grid(row=1,
                                                                                                                column=0,
                                                                                                                padx=10,
                                                                                                                pady=5,
                                                                                                                sticky="e")
    global member_code
    member_code = tk.Entry(add_modify_member_window, font=("Arial", 14), width=30)
    member_code.grid(row=1, column=1, padx=10, pady=5)


    # Member Name
    tk.Label(add_modify_member_window, text="Member Name", bg="#0baaea", font=("calibri", 14)).grid(row=3, column=0,
                                                                                                    padx=10, pady=5,
                                                                                                    sticky="e")
    global entry_member_name
    entry_member_name = tk.Entry(add_modify_member_window, font=("Arial", 14), width=30)
    entry_member_name.grid(row=3, column=1, padx=10, pady=5)

    # Member Address
    tk.Label(add_modify_member_window, text="Member Address", bg="#0baaea", font=("calibri", 14)).grid(row=4, column=0,
                                                                                                       padx=10, pady=5,
                                                                                                       sticky="e")
    global entry_member_address
    entry_member_address = tk.Entry(add_modify_member_window, font=("Arial", 14), width=30)
    entry_member_address.grid(row=4, column=1, padx=10, pady=5)

    # Member Phone
    tk.Label(add_modify_member_window, text="Member Phone", bg="#0baaea", font=("calibri", 14)).grid(row=5, column=0,
                                                                                                     padx=10, pady=5,
                                                                                                     sticky="e")
    global entry_member_phone
    entry_member_phone = tk.Entry(add_modify_member_window, font=("Arial", 14), width=30)
    entry_member_phone.grid(row=5, column=1, padx=10, pady=5)

    # Add Member and Clear buttons
    tk.Button(add_modify_member_window, text="Add Member", command=add_member, font=("Arial", 14), width=15).grid(row=6,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=20,
                                                                                                                  sticky="e")
    tk.Button(add_modify_member_window, text="Clear", command=clear_fields, font=("Arial", 14), width=15).grid(row=6,
                                                                                                               column=1,
                                                                                                               padx=10,
                                                                                                               pady=20)


#----------------------------------------------------------------------------------------------------------------------#

# Function to handle adding the book
def add_book():
    accession_number = entry_accession.get()
    subject_code = entry_subject.get()
    title = entry_title.get()
    author = entry_author.get()
    publisher = entry_publisher.get()
    price = entry_price.get()


    # Check for empty fields
    if not all([accession_number, subject_code, title, author, publisher, price]):
        messagebox.showinfo("Input Error", "Please fill all fields.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()

        # SQL query to insert new book
        query = '''INSERT INTO library_management (accession_number, subject_code, title, author, publisher, price)
                   VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (
            accession_number, subject_code, title, author, publisher, float(price)))

        conn.commit()
        messagebox.showinfo("Success", "Book Added!")
        clear_fields()

    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#----------------------------------------------------------------------------------------------------------------------#

# Function for the Modify Book window
def modify_book_window():
    modify_book = Toplevel(root)
    modify_book.title("Modify Book")
    modify_book.geometry("800x600")
    modify_book.config(bg="#0baaea")

    tk.Label(modify_book, text="Enter Accession Number", bg="#0baaea", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    global entry_accession_modify
    entry_accession_modify = tk.Entry(modify_book, font=("Arial", 14))
    entry_accession_modify.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(modify_book, text="Load Book", command=load_book_details).grid(row=0, column=2, padx=10, pady=10)

    # Create entry fields for modification
    global entry_subject_modify, entry_title_modify, entry_author_modify, entry_publisher_modify
    global entry_price_modify

    tk.Label(modify_book, text="Subject Code", bg="#0baaea", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    entry_subject_modify = tk.Entry(modify_book, font=("Arial", 14))
    entry_subject_modify.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(modify_book, text="Title", bg="#0baaea", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
    entry_title_modify = tk.Entry(modify_book, font=("Arial", 14))
    entry_title_modify.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(modify_book, text="Author", bg="#0baaea", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5)
    entry_author_modify = tk.Entry(modify_book, font=("Arial", 14))
    entry_author_modify.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(modify_book, text="Publisher", bg="#0baaea", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5)
    entry_publisher_modify = tk.Entry(modify_book, font=("Arial", 14))
    entry_publisher_modify.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(modify_book, text="Price", bg="#0baaea", font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=5)
    entry_price_modify = tk.Entry(modify_book, font=("Arial", 14))
    entry_price_modify.grid(row=5, column=1, padx=10, pady=5)

    tk.Button(modify_book, text="Update Book", command=update_book).grid(row=8, column=1, padx=10, pady=20)

#----------------------------------------------------------------------------------------------------------------------#

def load_book_details():
    accession_number = entry_accession_modify.get()
    if not accession_number:
        messagebox.showinfo("Input Error", "Please enter an accession number.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()

        # Fetch the book details based on the accession number
        query = '''SELECT subject_code, title, author, publisher, price
                   FROM library_management WHERE accession_number = %s'''
        cursor.execute(query, (accession_number,))
        book = cursor.fetchone()

        if book:
            entry_subject_modify.delete(0, tk.END)
            entry_subject_modify.insert(0, book[0])
            entry_title_modify.delete(0, tk.END)
            entry_title_modify.insert(0, book[1])
            entry_author_modify.delete(0, tk.END)
            entry_author_modify.insert(0, book[2])
            entry_publisher_modify.delete(0, tk.END)
            entry_publisher_modify.insert(0, book[3])
            entry_price_modify.delete(0, tk.END)
            entry_price_modify.insert(0, book[4])
        else:
            messagebox.showerror("Error", "Book not found!")

    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#----------------------------------------------------------------------------------------------------------------------#

def update_book():
    accession_number = entry_accession_modify.get()
    subject_code = entry_subject_modify.get()
    title = entry_title_modify.get()
    author = entry_author_modify.get()
    publisher = entry_publisher_modify.get()
    price = entry_price_modify.get()

    # Check for empty fields
    if not all([accession_number, subject_code, title, author, publisher, price]):
        messagebox.showinfo("Input Error", "Please fill all fields.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="library_management_system"
        )
        cursor = conn.cursor()

        # Update the book details
        query = '''UPDATE library_management
                   SET subject_code = %s, title = %s, author = %s, publisher = %s, price = %s
                   WHERE accession_number = %s'''
        cursor.execute(query, (
            subject_code, title, author, publisher, float(price), accession_number))
        conn.commit()
        messagebox.showinfo("Success", "Book Updated Successfully!")
        clear_modify_fields()

    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

#----------------------------------------------------------------------------------------------------------------------#

# Function to clear entry fields
def clear_fields():
    entry_accession.delete(0, tk.END)
    entry_subject.delete(0, tk.END)
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_publisher.delete(0, tk.END)
    entry_price.delete(0, tk.END)



#----------------------------------------------------------------------------------------------------------------------#

def clear_modify_fields():
    entry_accession_modify.delete(0, tk.END)
    entry_subject_modify.delete(0, tk.END)
    entry_title_modify.delete(0, tk.END)
    entry_author_modify.delete(0, tk.END)
    entry_publisher_modify.delete(0, tk.END)
    entry_price_modify.delete(0, tk.END)



#----------------------------------------------------------------------------------------------------------------------#

# Function for the Add/Modify Book window
def add_modify_book():
    add_modify_window = Toplevel(root)
    add_modify_window.title("Add Or Modify Book")
    add_modify_window.geometry("800x600")
    add_modify_window.config(bg="#0baaea")

    # Title label for the new window
    add_modify_label = tk.Label(add_modify_window, text="Add A New Book Or Update An Existing Book",
                                font=("calibri", 25, "bold"), fg="darkblue", bg="#0baaea", padx=30, pady=30)
    add_modify_label.grid(row=0, column=1, columnspan=5, pady=20)

    # Create labels and entry fields row by row
    tk.Label(add_modify_window, text="Accession Number", bg="#0baaea", font=("calibri", 14), fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    global entry_accession
    entry_accession = tk.Entry(add_modify_window, font=("Arial", 14), width=30)
    entry_accession.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_modify_window, text="Subject Code", bg="#0baaea", font=("calibri", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    global entry_subject
    entry_subject = tk.Entry(add_modify_window, font=("Arial", 14), width=30)
    entry_subject.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_modify_window, text="Title", bg="#0baaea", font=("calibri", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    global entry_title
    entry_title = tk.Entry(add_modify_window, font=("Arial", 14), width=30)
    entry_title.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(add_modify_window, text="Author", bg="#0baaea", font=("calibri", 14)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    global entry_author
    entry_author = tk.Entry(add_modify_window, font=("Arial", 14), width=30)
    entry_author.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(add_modify_window, text="Publisher", bg="#0baaea", font=("calibri", 14)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
    global entry_publisher
    entry_publisher = tk.Entry(add_modify_window, font=("Arial", 14), width=30)
    entry_publisher.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(add_modify_window, text="Price", bg="#0baaea", font=("calibri", 14)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
    global entry_price
    entry_price = tk.Entry(add_modify_window, font=("Arial", 14), width=30)
    entry_price.grid(row=6, column=1, padx=10, pady=5)

    # Create buttons
    tk.Button(add_modify_window, text="Add Book", command=add_book, font=("Arial", 14), width=15).grid(row=9, column=0, padx=10, pady=20, sticky="e")
    tk.Button(add_modify_window, text="Clear", command=clear_fields, font=("Arial", 14), width=15).grid(row=9, column=1, padx=10, pady=20)
    tk.Button(add_modify_window, text="Modify A Book", command=modify_book_window, font=("Arial", 14), width=15).grid(row=10, column=1, padx=10, pady=20)
    tk.Button(add_modify_window, text="Exit", command=add_modify_window.destroy, font=("Arial", 14), width=15).grid(row=9, column=2, padx=10, pady=20, sticky="w")

#----------------------------------------------------------------------------------------------------------------------#

# Library Management System title
title = tk.Label(root, text="Library Management System", font=("Product Sans", 40, "bold"), bg="#0baaea", fg="white")
title.pack(pady=50)

# Using Frame for aligning buttons
frame_for_buttons = tk.Frame(root, bg="#0baaea")
frame_for_buttons.pack(pady=50)

# Adding buttons with grid() to align them in two rows
add_modify_book_button = tk.Button(frame_for_buttons, text="Add / Modify Book", font=("calibri", 16, "bold"), padx=15,
                                   pady=10, width=20, activeforeground="black", bg="white", fg="#0baaea",
                                   command=add_modify_book)
add_modify_book_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

add_modify_member_button = tk.Button(frame_for_buttons, text="Add Member", font=("calibri", 16, "bold"),
                                     padx=15, pady=10, width=20, activeforeground="black", bg="white", fg="#0baaea", command=add_modify_member)
add_modify_member_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

issue_book_button = tk.Button(frame_for_buttons, text="Issue Book", font=("calibri", 16, "bold"), padx=15, pady=10,
                              width=20, activeforeground="black", bg="white", fg="#0baaea", command= issue_book)
issue_book_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

return_book_button = tk.Button(frame_for_buttons, text="Return Book", font=("calibri", 16, "bold"), padx=15, pady=10,
                               width=20, activeforeground="black", bg="white", fg="#0baaea", command=return_book_window)
return_book_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

search_book_button = tk.Button(frame_for_buttons, text="Available Books", font=("calibri", 16, "bold"), padx=15, pady=10,
                               width=20, activeforeground="black", bg="white", fg="#0baaea", command=open_search_window)
search_book_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

generate_report_button = tk.Button(frame_for_buttons, text="Generate Report", font=("calibri", 16, "bold"), padx=15,
                                   pady=10, width=20, activeforeground="black", bg="white", fg="#0baaea", command = reports_window)
generate_report_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

# Configure grid weights to allow for expansion
frame_for_buttons.grid_columnconfigure(1, weight=1)
frame_for_buttons.grid_columnconfigure(2, weight=1)

root.mainloop()

