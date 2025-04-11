import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import cv2
from pyzbar import pyzbar
import datetime

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        
        self.create_main_page()
    
    def create_main_page(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Library Management System", font=("Arial", 24))
        title_label.pack(pady=50)
        
        # Admin Button
        admin_img = Image.open("admin_icon.png").resize((150, 150))
        self.admin_photo = ImageTk.PhotoImage(admin_img)
        admin_btn = tk.Button(self.root, image=self.admin_photo, text="Admin", compound=tk.TOP,
                             command=self.admin_interface)
        admin_btn.pack(side=tk.LEFT, padx=50, pady=20)
        
        # Library Button
        lib_img = Image.open("library_icon.png").resize((150, 150))
        self.lib_photo = ImageTk.PhotoImage(lib_img)
        lib_btn = tk.Button(self.root, image=self.lib_photo, text="Library", compound=tk.TOP,
                            command=self.library_interface)
        lib_btn.pack(side=tk.RIGHT, padx=50, pady=20)
    
    def library_interface(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Library Operations", font=("Arial", 24))
        title_label.pack(pady=30)
        
        # Issue Button
        issue_img = Image.open("issue_icon.png").resize((100, 100))
        self.issue_photo = ImageTk.PhotoImage(issue_img)
        issue_btn = tk.Button(self.root, image=self.issue_photo, text="Issue Book", compound=tk.TOP,
                             command=self.issue_book)
        issue_btn.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Renew Button
        renew_img = Image.open("renew_icon.png").resize((100, 100))
        self.renew_photo = ImageTk.PhotoImage(renew_img)
        renew_btn = tk.Button(self.root, image=self.renew_photo, text="Renew Book", compound=tk.TOP,
                             command=self.renew_book)
        renew_btn.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Submit Button
        submit_img = Image.open("submit_icon.png").resize((100, 100))
        self.submit_photo = ImageTk.PhotoImage(submit_img)
        submit_btn = tk.Button(self.root, image=self.submit_photo, text="Submit Book", compound=tk.TOP,
                               command=self.submit_book)
        submit_btn.pack(side=tk.LEFT, padx=30, pady=20)
        
        back_btn = tk.Button(self.root, text="Back to Main", command=self.create_main_page)
        back_btn.pack(pady=20)
    
    def issue_book(self):
        self.scan_qr_codes("issue")
    
    def renew_book(self):
        self.scan_qr_codes("renew")
    
    def submit_book(self):
        self.scan_qr_codes("submit")
    
    def scan_qr_codes(self, operation):
        # This function will handle scanning of both student and book QR codes
        self.scan_window = tk.Toplevel(self.root)
        self.scan_window.title(f"Scan QR Codes - {operation.capitalize()}")
        self.scan_window.geometry("600x400")
        
        self.current_operation = operation
        self.student_data = None
        self.book_data = None
        
        tk.Label(self.scan_window, text=f"Please scan Student ID and Book QR codes", font=("Arial", 16)).pack(pady=20)
        
        # Student ID Frame
        student_frame = tk.Frame(self.scan_window)
        student_frame.pack(pady=10)
        tk.Label(student_frame, text="Student ID:").pack(side=tk.LEFT)
        self.student_entry = tk.Entry(student_frame, width=30)
        self.student_entry.pack(side=tk.LEFT, padx=10)
        scan_student_btn = tk.Button(student_frame, text="Scan", command=lambda: self.scan_code("student"))
        scan_student_btn.pack(side=tk.LEFT)
        
        # Book ID Frame
        book_frame = tk.Frame(self.scan_window)
        book_frame.pack(pady=10)
        tk.Label(book_frame, text="Book ID:").pack(side=tk.LEFT)
        self.book_entry = tk.Entry(book_frame, width=30)
        self.book_entry.pack(side=tk.LEFT, padx=10)
        scan_book_btn = tk.Button(book_frame, text="Scan", command=lambda: self.scan_code("book"))
        scan_book_btn.pack(side=tk.LEFT)
        
        # Process Button
        process_btn = tk.Button(self.scan_window, text=f"Process {operation.capitalize()}",
                               command=self.process_operation, state=tk.DISABLED)
        process_btn.pack(pady=20)
        self.process_btn = process_btn
        
        # Details Frame
        self.details_frame = tk.Frame(self.scan_window)
        self.details_frame.pack(pady=10)
        
        back_btn = tk.Button(self.scan_window, text="Back", command=self.scan_window.destroy)
        back_btn.pack(pady=10)
    
    def scan_code(self, code_type):
        # Initialize the camera
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Find and decode QR codes
            decoded_objects = pyzbar.decode(frame)
            
            # Draw rectangles around QR codes
            for obj in decoded_objects:
                cv2.rectangle(frame, (obj.rect.left, obj.rect.top),
                             (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height),
                             (0, 255, 0), 2)
                
            # Display the frame
            cv2.imshow('QR Code Scanner', frame)
            
            # Check for QR code detection
            if decoded_objects:
                code = decoded_objects[0].data.decode('utf-8')
                cap.release()
                cv2.destroyAllWindows()
                
                if code_type == "student":
                    self.student_entry.delete(0, tk.END)
                    self.student_entry.insert(0, code)
                    self.student_data = self.get_student_details(code)
                    self.display_details()
                else:
                    self.book_entry.delete(0, tk.END)
                    self.book_entry.insert(0, code)
                    self.book_data = self.get_book_details(code)
                    self.display_details()
                
                # Enable process button if both codes are scanned
                if self.student_data and self.book_data:
                    self.process_btn.config(state=tk.NORMAL)
                
                break
                
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()
    
    def get_student_details(self, student_id):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        student = cursor.fetchone()
        
        conn.close()
        
        if student:
            return {
                'id': student[0],
                'name': student[1],
                'email': student[2],
                'phone': student[3],
                'books_issued': student[4]
            }
        return None
    
    def get_book_details(self, book_id):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        book = cursor.fetchone()
        
        conn.close()
        
        if book:
            return {
                'id': book[0],
                'title': book[1],
                'author': book[2],
                'publisher': book[3],
                'year': book[4],
                'available': book[5],
                'due_date': book[6]
            }
        return None
    
    def display_details(self):
        # Clear previous details
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        
        # Display student details
        if self.student_data:
            tk.Label(self.details_frame, text="Student Details", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
            tk.Label(self.details_frame, text=f"Name: {self.student_data['name']}").grid(row=1, column=0, sticky="w")
            tk.Label(self.details_frame, text=f"ID: {self.student_data['id']}").grid(row=2, column=0, sticky="w")
            tk.Label(self.details_frame, text=f"Books Issued: {self.student_data['books_issued']}").grid(row=3, column=0, sticky="w")
        
        # Display book details
        if self.book_data:
            tk.Label(self.details_frame, text="Book Details", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w", padx=20)
            tk.Label(self.details_frame, text=f"Title: {self.book_data['title']}").grid(row=1, column=1, sticky="w", padx=20)
            tk.Label(self.details_frame, text=f"Author: {self.book_data['author']}").grid(row=2, column=1, sticky="w", padx=20)
            tk.Label(self.details_frame, text=f"Available: {'Yes' if self.book_data['available'] else 'No'}").grid(row=3, column=1, sticky="w", padx=20)
            
            if not self.book_data['available']:
                tk.Label(self.details_frame, text=f"Due Date: {self.book_data['due_date']}").grid(row=4, column=1, sticky="w", padx=20)
    
    def process_operation(self):
        if self.current_operation == "issue":
            self.process_issue()
        elif self.current_operation == "renew":
            self.process_renew()
        elif self.current_operation == "submit":
            self.process_submit()
        
        self.scan_window.destroy()
    
    def process_issue(self):
        if not self.book_data['available']:
            messagebox.showerror("Error", "Book is already issued to another student")
            return
        
        # Calculate due date (14 days from today)
        issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            # Update book status
            cursor.execute("UPDATE books SET available=0, due_date=? WHERE book_id=?", 
                          (due_date, self.book_data['id']))
            
            # Update student's books count
            cursor.execute("UPDATE students SET books_issued=books_issued+1 WHERE student_id=?", 
                          (self.student_data['id'],))
            
            # Create transaction record
            cursor.execute('''
            INSERT INTO transactions (student_id, book_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, ?)
            ''', (self.student_data['id'], self.book_data['id'], issue_date, due_date, "issued"))
            
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to issue book: {str(e)}")
        finally:
            conn.close()
    
    def process_renew(self):
        if self.book_data['available']:
            messagebox.showerror("Error", "Book is not currently issued")
            return
        
        # Check if the book is issued to this student
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM transactions 
        WHERE student_id=? AND book_id=? AND status='issued'
        ORDER BY transaction_id DESC LIMIT 1
        ''', (self.student_data['id'], self.book_data['id']))
        
        transaction = cursor.fetchone()
        
        if not transaction:
            messagebox.showerror("Error", "This book is not issued to this student")
            conn.close()
            return
        
        # Calculate new due date (14 days from current due date)
        current_due_date = datetime.datetime.strptime(self.book_data['due_date'], "%Y-%m-%d")
        new_due_date = (current_due_date + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
        
        try:
            # Update book due date
            cursor.execute("UPDATE books SET due_date=? WHERE book_id=?", 
                          (new_due_date, self.book_data['id']))
            
            # Update transaction
            cursor.execute('''
            UPDATE transactions SET due_date=? 
            WHERE transaction_id=?
            ''', (new_due_date, transaction[0]))
            
            conn.commit()
            messagebox.showinfo("Success", "Book renewed successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to renew book: {str(e)}")
        finally:
            conn.close()
    
    def process_submit(self):
        if self.book_data['available']:
            messagebox.showerror("Error", "Book is not currently issued")
            return
        
        # Check if the book is issued to this student
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM transactions 
        WHERE student_id=? AND book_id=? AND status='issued'
        ORDER BY transaction_id DESC LIMIT 1
        ''', (self.student_data['id'], self.book_data['id']))
        
        transaction = cursor.fetchone()
        
        if not transaction:
            messagebox.showerror("Error", "This book is not issued to this student")
            conn.close()
            return
        
        return_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Update book status
            cursor.execute("UPDATE books SET available=1, due_date=NULL WHERE book_id=?", 
                          (self.book_data['id'],))
            
            # Update student's books count
            cursor.execute("UPDATE students SET books_issued=books_issued-1 WHERE student_id=?", 
                          (self.student_data['id'],))
            
            # Update transaction
            cursor.execute('''
            UPDATE transactions SET return_date=?, status='returned' 
            WHERE transaction_id=?
            ''', (return_date, transaction[0]))
            
            conn.commit()
            messagebox.showinfo("Success", "Book submitted successfully")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to submit book: {str(e)}")
        finally:
            conn.close()
    
    def admin_interface(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Admin Panel", font=("Arial", 24))
        title_label.pack(pady=30)
        
        # Dashboard Button
        dashboard_btn = tk.Button(self.root, text="Dashboard", width=20, height=2,
                                command=self.admin_dashboard)
        dashboard_btn.pack(pady=10)
        
        # Add Book Button
        add_book_btn = tk.Button(self.root, text="Add New Book", width=20, height=2,
                                command=self.add_books)
        add_book_btn.pack(pady=10)
        
        # Add Student Button
        add_student_btn = tk.Button(self.root, text="Add New Student", width=20, height=2,
                                   command=self.add_student)
        add_student_btn.pack(pady=10)
        
        # Manage Books Button
        manage_books_btn = tk.Button(self.root, text="Manage Books", width=20, height=2,
                                   command=self.manage_books)
        manage_books_btn.pack(pady=10)
        
        # Manage Students Button
        manage_students_btn = tk.Button(self.root, text="Manage Students", width=20, height=2,
                                      command=self.manage_students)
        manage_students_btn.pack(pady=10)
        
        back_btn = tk.Button(self.root, text="Back to Main", command=self.create_main_page)
        back_btn.pack(pady=20)

    def admin_dashboard(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Admin Dashboard", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Get statistics from database
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        # Total books
        cursor.execute("SELECT COUNT(*) FROM books")
        total_books = cursor.fetchone()[0]
        
        # Available books
        cursor.execute("SELECT COUNT(*) FROM books WHERE available=1")
        available_books = cursor.fetchone()[0]
        
        # Total students
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        
        # Books issued
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE status='issued'")
        issued_books = cursor.fetchone()[0]
        
        # Overdue books
        cursor.execute("SELECT COUNT(*) FROM books WHERE available=0 AND due_date < date('now')")
        overdue_books = cursor.fetchone()[0]
        
        conn.close()
        
        # Dashboard metrics frame
        metrics_frame = tk.Frame(self.root)
        metrics_frame.pack(pady=20)
        
        # Metrics display
        tk.Label(metrics_frame, text="Total Books:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(metrics_frame, text=total_books, font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(metrics_frame, text="Available Books:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(metrics_frame, text=available_books, font=("Arial", 12, "bold")).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(metrics_frame, text="Total Students:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(metrics_frame, text=total_students, font=("Arial", 12, "bold")).grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(metrics_frame, text="Books Issued:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        tk.Label(metrics_frame, text=issued_books, font=("Arial", 12, "bold")).grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(metrics_frame, text="Overdue Books:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(metrics_frame, text=overdue_books, font=("Arial", 12, "bold")).grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        # Recent transactions frame
        trans_frame = tk.LabelFrame(self.root, text="Recent Transactions", padx=10, pady=10)
        trans_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Treeview for transactions
        columns = ("Transaction ID", "Student ID", "Book ID", "Issue Date", "Due Date", "Status")
        self.trans_tree = ttk.Treeview(trans_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.trans_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load recent transactions
        self.load_recent_transactions()
        
        back_btn = tk.Button(self.root, text="Back to Admin", command=self.admin_interface)
        back_btn.pack(pady=10)
    
    def load_recent_transactions(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT transaction_id, student_id, book_id, issue_date, due_date, status 
        FROM transactions 
        ORDER BY transaction_id DESC 
        LIMIT 10
        ''')
        
        transactions = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.trans_tree.get_children():
            self.trans_tree.delete(item)
        
        # Add new data
        for trans in transactions:
            self.trans_tree.insert("", tk.END, values=trans)
    
    def add_books(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Add New Book", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        # Book ID
        tk.Label(form_frame, text="Book ID (Barcode):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.book_id_entry = tk.Entry(form_frame, width=30)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Generate QR Button
        gen_qr_btn = tk.Button(form_frame, text="Generate QR", command=self.generate_book_qr)
        gen_qr_btn.grid(row=0, column=2, padx=10)
        
        # Title
        tk.Label(form_frame, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Author
        tk.Label(form_frame, text="Author:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.author_entry = tk.Entry(form_frame, width=30)
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Publisher
        tk.Label(form_frame, text="Publisher:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.publisher_entry = tk.Entry(form_frame, width=30)
        self.publisher_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Year
        tk.Label(form_frame, text="Year:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.year_entry = tk.Entry(form_frame, width=30)
        self.year_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="Add Book", command=self.submit_new_book)
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(btn_frame, text="Cancel", command=self.admin_interface)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def generate_book_qr(self):
        # Generate a unique book ID (you can customize this)
        book_id = "BK" + str(int(datetime.datetime.now().timestamp()))[-6:]
        self.book_id_entry.delete(0, tk.END)
        self.book_id_entry.insert(0, book_id)
        
        # In a real implementation, you would generate and save a QR code image
        messagebox.showinfo("Info", f"Book ID generated: {book_id}\nQR code can be printed later.")
    
    def submit_new_book(self):
        book_id = self.book_id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        publisher = self.publisher_entry.get()
        year = self.year_entry.get()
        
        if not all([book_id, title, author]):
            messagebox.showerror("Error", "Book ID, Title, and Author are required fields")
            return
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO books (book_id, title, author, publisher, year)
            VALUES (?, ?, ?, ?, ?)
            ''', (book_id, title, author, publisher, year))
            
            conn.commit()
            messagebox.showinfo("Success", "Book added successfully")
            self.admin_interface()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Book ID already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")
        finally:
            conn.close()
    
    def add_student(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Add New Student", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        # Student ID
        tk.Label(form_frame, text="Student ID (Barcode):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.student_id_entry = tk.Entry(form_frame, width=30)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Generate QR Button
        gen_qr_btn = tk.Button(form_frame, text="Generate QR", command=self.generate_student_qr)
        gen_qr_btn.grid(row=0, column=2, padx=10)
        
        # Name
        tk.Label(form_frame, text="Full Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Email
        tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Phone
        tk.Label(form_frame, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        submit_btn = tk.Button(btn_frame, text="Add Student", command=self.submit_new_student)
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(btn_frame, text="Cancel", command=self.admin_interface)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def generate_student_qr(self):
        # Generate a unique student ID (you can customize this)
        student_id = "ST" + str(int(datetime.datetime.now().timestamp()))[-6:]
        self.student_id_entry.delete(0, tk.END)
        self.student_id_entry.insert(0, student_id)
        
        # In a real implementation, you would generate and save a QR code image
        messagebox.showinfo("Info", f"Student ID generated: {student_id}\nQR code can be printed later.")
    
    def submit_new_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        
        if not all([student_id, name]):
            messagebox.showerror("Error", "Student ID and Name are required fields")
            return
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO students (student_id, name, email, phone)
            VALUES (?, ?, ?, ?)
            ''', (student_id, name, email, phone))
            
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully")
            self.admin_interface()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student ID already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
        finally:
            conn.close()
    
    def manage_books(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Manage Books", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.book_search_entry = tk.Entry(search_frame, width=40)
        self.book_search_entry.pack(side=tk.LEFT, padx=5)
        search_btn = tk.Button(search_frame, text="Search", command=self.search_books)
        search_btn.pack(side=tk.LEFT)
        
        # Books treeview
        self.books_tree = ttk.Treeview(self.root, columns=("ID", "Title", "Author", "Status"), show="headings", height=15)
        self.books_tree.heading("ID", text="Book ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Status", text="Status")
        
        self.books_tree.column("ID", width=100, anchor=tk.CENTER)
        self.books_tree.column("Title", width=200, anchor=tk.W)
        self.books_tree.column("Author", width=150, anchor=tk.W)
        self.books_tree.column("Status", width=100, anchor=tk.CENTER)
        
        self.books_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        edit_btn = tk.Button(btn_frame, text="Edit Book", command=self.edit_book)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Delete Book", command=self.delete_book)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.load_all_books)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(btn_frame, text="Back", command=self.admin_interface)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        # Load all books initially
        self.load_all_books()
    
    def load_all_books(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT book_id, title, author, available FROM books")
        books = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Add new data
        for book in books:
            status = "Available" if book[3] else "Issued"
            self.books_tree.insert("", tk.END, values=(book[0], book[1], book[2], status))
    
    def search_books(self):
        search_term = self.book_search_entry.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT book_id, title, author, available 
        FROM books 
        WHERE book_id LIKE ? OR title LIKE ? OR author LIKE ?
        ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        books = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Add new data
        for book in books:
            status = "Available" if book[3] else "Issued"
            self.books_tree.insert("", tk.END, values=(book[0], book[1], book[2], status))
    
    def edit_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return
        
        book_id = self.books_tree.item(selected_item)['values'][0]
        
        # Open edit window
        self.edit_book_window = tk.Toplevel(self.root)
        self.edit_book_window.title("Edit Book")
        self.edit_book_window.geometry("400x300")
        
        # Get book details
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        book = cursor.fetchone()
        conn.close()
        
        if not book:
            messagebox.showerror("Error", "Book not found")
            self.edit_book_window.destroy()
            return
        
        # Form frame
        form_frame = tk.Frame(self.edit_book_window)
        form_frame.pack(pady=20)
        
        # Book ID (readonly)
        tk.Label(form_frame, text="Book ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(form_frame, text=book[0]).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Title
        tk.Label(form_frame, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.edit_title_entry = tk.Entry(form_frame, width=30)
        self.edit_title_entry.insert(0, book[1])
        self.edit_title_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Author
        tk.Label(form_frame, text="Author:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.edit_author_entry = tk.Entry(form_frame, width=30)
        self.edit_author_entry.insert(0, book[2])
        self.edit_author_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Publisher
        tk.Label(form_frame, text="Publisher:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.edit_publisher_entry = tk.Entry(form_frame, width=30)
        self.edit_publisher_entry.insert(0, book[3] if book[3] else "")
        self.edit_publisher_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Year
        tk.Label(form_frame, text="Year:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.edit_year_entry = tk.Entry(form_frame, width=30)
        self.edit_year_entry.insert(0, book[4] if book[4] else "")
        self.edit_year_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.edit_book_window)
        btn_frame.pack(pady=10)
        
        save_btn = tk.Button(btn_frame, text="Save Changes", command=lambda: self.save_book_changes(book_id))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.edit_book_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def save_book_changes(self, book_id):
        title = self.edit_title_entry.get()
        author = self.edit_author_entry.get()
        publisher = self.edit_publisher_entry.get()
        year = self.edit_year_entry.get()
        
        if not all([title, author]):
            messagebox.showerror("Error", "Title and Author are required fields")
            return
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE books 
            SET title=?, author=?, publisher=?, year=?
            WHERE book_id=?
            ''', (title, author, publisher, year, book_id))
            
            conn.commit()
            messagebox.showinfo("Success", "Book updated successfully")
            self.edit_book_window.destroy()
            self.load_all_books()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")
        finally:
            conn.close()
    
    def delete_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        
        book_id = self.books_tree.item(selected_item)['values'][0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete book {book_id}?"):
            return
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            # Check if book is issued
            cursor.execute("SELECT available FROM books WHERE book_id=?", (book_id,))
            available = cursor.fetchone()[0]
            
            if not available:
                messagebox.showerror("Error", "Cannot delete an issued book")
                return
            
            # Delete book
            cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
            conn.commit()
            
            messagebox.showinfo("Success", "Book deleted successfully")
            self.load_all_books()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to delete book: {str(e)}")
        finally:
            conn.close()
    
    def manage_students(self):
        self.clear_window()
        
        title_label = tk.Label(self.root, text="Manage Students", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.student_search_entry = tk.Entry(search_frame, width=40)
        self.student_search_entry.pack(side=tk.LEFT, padx=5)
        search_btn = tk.Button(search_frame, text="Search", command=self.search_students)
        search_btn.pack(side=tk.LEFT)
        
        # Students treeview
        self.students_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Email", "Books Issued"), show="headings", height=15)
        self.students_tree.heading("ID", text="Student ID")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.heading("Email", text="Email")
        self.students_tree.heading("Books Issued", text="Books Issued")
        
        self.students_tree.column("ID", width=100, anchor=tk.CENTER)
        self.students_tree.column("Name", width=200, anchor=tk.W)
        self.students_tree.column("Email", width=150, anchor=tk.W)
        self.students_tree.column("Books Issued", width=100, anchor=tk.CENTER)
        
        self.students_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Action buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        edit_btn = tk.Button(btn_frame, text="Edit Student", command=self.edit_student)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(btn_frame, text="Delete Student", command=self.delete_student)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        view_books_btn = tk.Button(btn_frame, text="View Issued Books", command=self.view_student_books)
        view_books_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.load_all_students)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(btn_frame, text="Back", command=self.admin_interface)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        # Load all students initially
        self.load_all_students()
    
    def load_all_students(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT student_id, name, email, books_issued FROM students")
        students = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Add new data
        for student in students:
            self.students_tree.insert("", tk.END, values=(student[0], student[1], student[2], student[3]))
    
    def search_students(self):
        search_term = self.student_search_entry.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT student_id, name, email, books_issued 
        FROM students 
        WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ?
        ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        students = cursor.fetchall()
        conn.close()
        
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Add new data
        for student in students:
            self.students_tree.insert("", tk.END, values=(student[0], student[1], student[2], student[3]))
    
    def edit_student(self):
        selected_item = self.students_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        student_id = self.students_tree.item(selected_item)['values'][0]
        
        # Open edit window
        self.edit_student_window = tk.Toplevel(self.root)
        self.edit_student_window.title("Edit Student")
        self.edit_student_window.geometry("400x300")
        
        # Get student details
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        
        if not student:
            messagebox.showerror("Error", "Student not found")
            self.edit_student_window.destroy()
            return
        
        # Form frame
        form_frame = tk.Frame(self.edit_student_window)
        form_frame.pack(pady=20)
        
        # Student ID (readonly)
        tk.Label(form_frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(form_frame, text=student[0]).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Name
        tk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.edit_student_name_entry = tk.Entry(form_frame, width=30)
        self.edit_student_name_entry.insert(0, student[1])
        self.edit_student_name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Email
        tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.edit_student_email_entry = tk.Entry(form_frame, width=30)
        self.edit_student_email_entry.insert(0, student[2] if student[2] else "")
        self.edit_student_email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Phone
        tk.Label(form_frame, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.edit_student_phone_entry = tk.Entry(form_frame, width=30)
        self.edit_student_phone_entry.insert(0, student[3] if student[3] else "")
        self.edit_student_phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(self.edit_student_window)
        btn_frame.pack(pady=10)
        
        save_btn = tk.Button(btn_frame, text="Save Changes", command=lambda: self.save_student_changes(student_id))
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.edit_student_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def save_student_changes(self, student_id):
        name = self.edit_student_name_entry.get()
        email = self.edit_student_email_entry.get()
        phone = self.edit_student_phone_entry.get()
        
        if not all([student_id, name]):
            messagebox.showerror("Error", "Student ID and Name are required fields")
            return
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE students 
            SET name=?, email=?, phone=?
            WHERE student_id=?
            ''', (name, email, phone, student_id))
            
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully")
            self.edit_student_window.destroy()
            self.load_all_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")
        finally:
            conn.close()
    
    def delete_student(self):
        selected_item = self.students_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        student_id = self.students_tree.item(selected_item)['values'][0]
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete student {student_id}?"):
            return
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        try:
            # Check if student has issued books
            cursor.execute("SELECT books_issued FROM students WHERE student_id=?", (student_id,))
            books_issued = cursor.fetchone()[0]
            
            if books_issued > 0:
                messagebox.showerror("Error", "Cannot delete a student with issued books")
                return
            
            # Delete student
            cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
            conn.commit()
            
            messagebox.showinfo("Success", "Student deleted successfully")
            self.load_all_students()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
        finally:
            conn.close()
    
    def view_student_books(self):
        selected_item = self.students_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a student")
            return
        
        student_id = self.students_tree.item(selected_item)['values'][0]
        student_name = self.students_tree.item(selected_item)['values'][1]
        
        # Open books window
        books_window = tk.Toplevel(self.root)
        books_window.title(f"Books Issued to {student_name}")
        books_window.geometry("800x400")
        
        # Title
        tk.Label(books_window, text=f"Books Issued to {student_name} ({student_id})", font=("Arial", 14)).pack(pady=10)
        
        # Books treeview
        books_tree = ttk.Treeview(books_window, columns=("Book ID", "Title", "Author", "Issue Date", "Due Date"), show="headings", height=10)
        books_tree.heading("Book ID", text="Book ID")
        books_tree.heading("Title", text="Title")
        books_tree.heading("Author", text="Author")
        books_tree.heading("Issue Date", text="Issue Date")
        books_tree.heading("Due Date", text="Due Date")
        
        books_tree.column("Book ID", width=100, anchor=tk.CENTER)
        books_tree.column("Title", width=200, anchor=tk.W)
        books_tree.column("Author", width=150, anchor=tk.W)
        books_tree.column("Issue Date", width=100, anchor=tk.CENTER)
        books_tree.column("Due Date", width=100, anchor=tk.CENTER)
        
        books_tree.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Load student's books
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT b.book_id, b.title, b.author, t.issue_date, t.due_date
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        WHERE t.student_id=? AND t.status='issued'
        ''')
        
        # self.clear_window()
        
        # title_label = tk.Label(self.root, text="Admin Panel", font=("Arial", 24))
        # title_label.pack(pady=30)
        
        # # Add Book Button
        # add_book_btn = tk.Button(self.root, text="Add New Book", width=20, height=2,
        #                         command=self.add_book)
        # add_book_btn.pack(pady=10)
        
        # # Add Student Button
        # add_student_btn = tk.Button(self.root, text="Add New Student", width=20, height=2,
        #                            command=self.add_student)
        # add_student_btn.pack(pady=10)
        
        # # View Reports Button
        # reports_btn = tk.Button(self.root, text="View Reports", width=20, height=2,
        #                        command=self.view_reports)
        # reports_btn.pack(pady=10)
        
        #Back Button 
        # back_btn = tk.Button(self.root, text="Back to Main", command=self.create_main_page)
        # back_btn.pack(pady=20)
    
    # def add_book(self):
    #     # Implementation for adding a new book
    #     pass
    
    # def add_student(self):
    #     # Implementation for adding a new student
    #     pass
    
    # def view_reports(self):
    #     # Implementation for viewing reports
    #     pass
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()