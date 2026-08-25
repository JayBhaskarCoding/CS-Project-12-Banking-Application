import tkinter as tk
from tkinter import messagebox
import mysql.connector as sql
import random
import string
import datetime

class PlaceHolderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", is_password=False, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.is_password = is_password
        self.default_fg = self.cget("fg")

        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        self.show_placeholder()

    def show_placeholder(self):
        self.delete(0, tk.END)
        if self.is_password:
            self.config(show="")
        self.config(fg="grey")
        self.insert(0, self.placeholder)

    def on_focus_in(self, event):
        if self.cget("fg") == "grey":
            self.delete(0, tk.END)
            self.config(fg=self.default_fg)
            if self.is_password:
                self.config(show="*")

    def on_focus_out(self, event):
        if not super().get():
            self.show_placeholder()

    def get(self):
        content = super().get()
        if self.cget("fg") == "grey" and content == self.placeholder:
            return ""
        return content

db = sql.connect(host="localhost", user="root", password="1234", database="Bank_Mng")
cursor = db.cursor(buffered=True)

def random_account_gen():
    first_digit = str(random.randint(1,9))
    remainng_digits = "".join(str(random.randint(0,9)) for i in range(15))
    return first_digit + remainng_digits

def gen_unique_acc_no(cursor):
    while True:
        potential_number = random_account_gen()

        cursor.execute("SELECT Acc_No FROM Accounts WHERE Acc_No = %s", (potential_number,))
        if cursor.fetchone() is None:
            return potential_number

def random_emp_gen():
    emp_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return emp_id

def gen_unique_emp_id(cursor):
    while True:
            potential_id = random_emp_gen()
    
            cursor.execute("SELECT Emp_ID FROM Employee_Credentials WHERE Emp_ID = %s", (potential_id,))
            if cursor.fetchone() is None:
                return potential_id

def gen_unique_trnsc_id():
    time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    return f"{prefix}{time}{suffix}"

def clear_window():
    for widget in main_window.winfo_children():
        widget.destroy()

def draw_homepage():
    clear_window()
    main_window.title("Bank Management")

    Header = tk.Label(main_window, text="Welcome to Bank Management", font=("Helvetica", 28, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(60, 30))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, padx=40, ipadx=40, ipady=40)

    Split_Frame = tk.Frame(Card_Frame, bg="white")
    Split_Frame.pack(expand=True, fill="both")

    Customer_Frame = tk.Frame(Split_Frame, bg="white")
    Customer_Frame.pack(side="left", padx=(60, 20))

    Cus_Title = tk.Label(Customer_Frame, text="For Customers", font=("Helvetica", 16, "bold"), bg="white", fg="#333333")
    Cus_Title.pack(pady=(0, 10))

    Cus_Desc = tk.Label(Customer_Frame, text="Access your personal accounts,\ntransfer funds, and view balances.", font=("Helvetica", 11), bg="white", fg="#777777", justify="center")
    Cus_Desc.pack(pady=(0, 25))

    Cus_Btn = tk.Button(Customer_Frame, text="Customer Portal", font=("Helvetica", 12, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", command=draw_login_screen, width=20, pady=5)
    Cus_Btn.pack()

    Divider = tk.Frame(Split_Frame, bg="#E0E0E0", width=2)
    Divider.pack(side="left", fill="y", padx=50)

    Employee_Frame = tk.Frame(Split_Frame, bg="white")
    Employee_Frame.pack(side="right", padx=(20, 60))

    Emp_Title = tk.Label(Employee_Frame, text="For Employees", font=("Helvetica", 16, "bold"), bg="white", fg="#333333")
    Emp_Title.pack(pady=(0, 10))

    Emp_Desc = tk.Label(Employee_Frame, text="Manage user accounts, verify\ntransactions, and assist customers.", font=("Helvetica", 11), bg="white", fg="#777777", justify="center")
    Emp_Desc.pack(pady=(0, 25))

    Emp_Btn = tk.Button(Employee_Frame, text="Employee Portal", font=("Helvetica", 12, "bold"), bg="#4A5568", fg="white", relief="flat", cursor="hand2", command=draw_emp_login_screen, width=20, pady=5)
    Emp_Btn.pack()

def draw_login_screen():
    clear_window()
    main_window.title("Bank Management - Login")

    Header = tk.Label(main_window, text="Log Into Your Account", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Username_Label = tk.Label(Card_Frame, text="Username", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Username_Label.pack(anchor="center", pady=(30, 2), padx=(0,250))
    Username_Input = PlaceHolderEntry(Card_Frame, placeholder="Enter Your Username", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Username_Input.pack(anchor="center", pady=(0, 15))

    Password_Label = tk.Label(Card_Frame, text="Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Password_Label.pack(anchor="center", pady=(20, 2), padx=(0,250))
    Password_Input = PlaceHolderEntry(Card_Frame, placeholder="Enter Your Password", is_password=True, font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Password_Input.pack(anchor="center", pady=(0, 30))

    def attempt_login():
        username = Username_Input.get()
        password = Password_Input.get()

        if not username.strip()or not password.strip():
            messagebox.showwarning("Invalid Input", "Please Enter Both Your Username And Password Correctly !")
            return
        try:
            cursor.execute("SELECT Psswd, Acc_No FROM Account_Credentials WHERE Usrnm = %s", (username,))
            result = cursor.fetchone()

            if result is not None and result[0] == password:
                ac_no = result[1]
                
                cursor.execute("SELECT Acc_Name, Acc_Balance FROM Accounts WHERE Acc_No = %s", (ac_no,))
                data = cursor.fetchone()

                if data is not None:
                    acc_name = data[0]
                    acc_balance = data[1]
                else:
                    messagebox.showerror("Error", "Account data not found.")
                    return
                
                draw_dashboard(acc_name, acc_balance, ac_no)
                print(f"Logged In Succesfully {username}")
            else:
                messagebox.showerror("Login Failed", "Invalid Username Or Password !! \n\n Please Check Your Username And Password")
        except sql.Error as err:
            print(f"Databse Error: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(30,0))

    Login_Btn = tk.Button(Button_Frame, text="Login", font=("Helvetica", 13, "bold"), bg="#009933", fg="white", relief="flat", cursor="hand2", command=attempt_login, width=32)
    Login_Btn.grid(row=0, column=0, columnspan=2, pady=(0, 18))

    Back_Homepage = tk.Button(Button_Frame, text="Back To Homepage", font=("Helvetica", 13), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=draw_homepage, width=30)
    Back_Homepage.grid(row=1, column=1, padx=(0, 15))

def draw_create_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Create Account")

    Header = tk.Label(main_window, text="Create A New Account", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Acc_Name_Label = tk.Label(Card_Frame, text="Enter Your Full Name", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Acc_Name_Label.pack(anchor="center", pady=(30, 2), padx=(0,170))
    Acc_Name_Input = PlaceHolderEntry(Card_Frame, placeholder="*Required", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Acc_Name_Input.pack(anchor="center", pady=(0, 15))

    Username_Label = tk.Label(Card_Frame, text="Choose A Username", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Username_Label.pack(anchor="center", pady=(20, 2), padx=(0,180))
    Username_Input = PlaceHolderEntry(Card_Frame, placeholder="*Required", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Username_Input.pack(anchor="center", pady=(0, 15))

    Password_Label = tk.Label(Card_Frame, text="Create A Strong Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Password_Label.pack(anchor="center", pady=(20, 2), padx=(0,135))
    Password_Input = PlaceHolderEntry(Card_Frame, placeholder="*Required", is_password=True, font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Password_Input.pack(anchor="center", pady=(0, 30))

    def attempt_create():
        username = Username_Input.get()
        password = Password_Input.get()
        acc_name = Acc_Name_Input.get()

        if not username.strip() or not password.strip() or not acc_name.strip():
            messagebox.showerror("Invalid Input", "Please Fill All Required Fields Properly !")
            return
            
        try:
            cursor.execute("SELECT Usrnm FROM Account_Credentials WHERE Usrnm = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user is not None:
                messagebox.showerror("Username Taken", "Please Use A Different Username. This Username Is Already Taken")
                return
                
            acc_no = gen_unique_acc_no(cursor)
            cursor.execute("INSERT INTO Accounts (Acc_No, Acc_Name, Acc_Balance, Acc_opn_date) VALUES (%s, %s, %s, NOW())", (acc_no, acc_name, 0.00,))
            cursor.execute("INSERT INTO Account_Credentials (Acc_No, Usrnm, Psswd) VALUES (%s, %s, %s)", (acc_no, username, password))
            db.commit()
            print(f"Account Created Successfully With Account Number: {acc_no}")
            messagebox.showinfo("Account Created", f"Your Account Has Been Created Succesfully \n\n Your Account Number Is: {acc_no}")
            draw_employee_dashboard(emp_id, emp_name)
                
        except sql.Error as err:
            print(f"Database Error: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(20,0))

    Create_Btn = tk.Button(Button_Frame, text="Create Account", font=("Helvetica", 13, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", command=attempt_create, width=32)
    Create_Btn.grid(row=0, column=0, columnspan=2, pady=(0, 18))

    Back_Btn = tk.Button(Button_Frame, text="Back To Dashboard", font=("Helvetica", 13), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=lambda: draw_employee_dashboard(emp_id, emp_name), width=24)
    Back_Btn.grid(row=1, column=0, padx=(40,0))

def draw_withdraw_screen(acc_no):
    clear_window()
    main_window.title("Bank Management - Withdraw Funds")

    Header = tk.Label(main_window, text="Withdraw Funds", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Withdraw_Label = tk.Label(Card_Frame, text="Enter Withdrawal Amount (₹)", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Withdraw_Label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    
    Withdraw_Entry = PlaceHolderEntry(Card_Frame, placeholder="0.00", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Withdraw_Entry.pack(anchor="center", pady=(0, 30))

    # Helper function to reload the dashboard safely
    def go_back():
        cursor.execute("SELECT Acc_Name, Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
        data = cursor.fetchone()
        if data:
            draw_dashboard(data[0], data[1], acc_no)

    def attempt_withdraw():
        amt_str = Withdraw_Entry.get().strip()
        if not amt_str:
            messagebox.showwarning("Invalid Input", "Please enter an amount.")
            return

        try:
            amt = float(amt_str)
            if amt <= 0:
                messagebox.showwarning("Invalid Amount", "Withdrawal amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount.")
            return

        try:
            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
            result = cursor.fetchone()
            if result is None:
                messagebox.showerror("Error", "Account not found!")
                return
            
            current_balance = float(result[0])
            if current_balance < amt:
                messagebox.showerror("Declined", f"Insufficient funds. You only have ₹{current_balance:,.2f}")
                return

            new_balance = current_balance - amt
            trans_id = gen_unique_trnsc_id()

            cursor.execute("UPDATE Accounts SET Acc_Balance = %s WHERE Acc_No = %s", (new_balance, acc_no))
            cursor.execute("INSERT INTO Transactions (Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time) VALUES (%s, %s, %s, %s, NOW())", (trans_id, acc_no, "SELF_WITHDRAW", amt))
            db.commit()

            messagebox.showinfo("Withdrawal Successful", f"Successfully withdrew ₹{amt:,.2f}!\n\nTransaction ID: {trans_id}")
            go_back()

        except sql.Error as err:
            db.rollback()
            messagebox.showerror("Database Error", f"Withdrawal failed: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(10, 0))

    Withdraw_Btn = tk.Button(Button_Frame, text="Complete Withdrawal", font=("Helvetica", 13, "bold"), bg="#f44336", fg="white", relief="flat", cursor="hand2", command=attempt_withdraw, width=32)
    Withdraw_Btn.grid(row=0, column=0, pady=(0, 15))

    Back_Btn = tk.Button(Button_Frame, text="Back To Dashboard", font=("Helvetica", 11), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=go_back, width=20)
    Back_Btn.grid(row=1, column=0)

def draw_deposit_screen(acc_no):
    clear_window()
    main_window.title("Bank Management - Deposit Funds")

    Header = tk.Label(main_window, text="Deposit Funds", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Deposit_Label = tk.Label(Card_Frame, text="Enter Deposit Amount (₹)", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Deposit_Label.pack(anchor="center", pady=(10, 2), padx=(0, 155))
    
    Deposit_Entry = PlaceHolderEntry(Card_Frame, placeholder="0.00", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Deposit_Entry.pack(anchor="center", pady=(0, 30))

    def go_back():
        cursor.execute("SELECT Acc_Name, Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
        data = cursor.fetchone()
        if data:
            draw_dashboard(data[0], data[1], acc_no)

    def attempt_deposit():
        amt_str = Deposit_Entry.get().strip()
        if not amt_str:
            messagebox.showwarning("Invalid Input", "Please enter an amount.")
            return

        try:
            amt = float(amt_str)
            if amt <= 0:
                messagebox.showwarning("Invalid Amount", "Deposit amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount.")
            return

        try:
            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
            result = cursor.fetchone()
            if result is None:
                messagebox.showerror("Error", "Account not found!")
                return
            
            new_balance = float(result[0]) + amt
            trans_id = gen_unique_trnsc_id()

            cursor.execute("UPDATE Accounts SET Acc_Balance = %s WHERE Acc_No = %s", (new_balance, acc_no))
            cursor.execute("INSERT INTO Transactions (Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time) VALUES (%s, %s, %s, %s, NOW())", (trans_id, "SELF_DEPOSIT", acc_no, amt))
            db.commit()

            messagebox.showinfo("Deposit Successful", f"Successfully deposited ₹{amt:,.2f}!\n\nTransaction ID: {trans_id}")
            go_back()

        except sql.Error as err:
            db.rollback()
            messagebox.showerror("Database Error", f"Deposit failed: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(10, 0))

    Deposit_Btn = tk.Button(Button_Frame, text="Complete Deposit", font=("Helvetica", 13, "bold"), bg="#4CAF50", fg="white", relief="flat", cursor="hand2", command=attempt_deposit, width=32)
    Deposit_Btn.grid(row=0, column=0, pady=(0, 15))

    Back_Btn = tk.Button(Button_Frame, text="Back To Dashboard", font=("Helvetica", 11), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=go_back, width=20)
    Back_Btn.grid(row=1, column=0)

def draw_dashboard(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title(f"Bank Management - Dashboard For {acc_name}")

    Header = tk.Label(main_window, text=f"Welcome Back {acc_name} !", font=("Helvetica", 22, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40,15))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(padx=80, pady=10, fill="x", ipady=15)

    Balance_Title = tk.Label(Card_Frame, text="Available Balance", font=("Helvetica", 15, "bold"), bg="white", fg="#777777")
    Balance_Title.pack(pady=(15, 0))

    Formatted_Balance = f"₹{acc_balance:,.2f}" if acc_balance is not None else "₹0.00"
    Balance = tk.Label(Card_Frame, text=Formatted_Balance, font=("Helvetica", 28, "bold"), bg="white", fg="#009933")
    Balance.pack(pady=(5,15))

    Separator = tk.Frame(Card_Frame, height=1, bg="#e0e0e0")
    Separator.pack(fill="x", padx=40, pady=10)

    Info_Frame = tk.Frame(Card_Frame, bg="white")
    Info_Frame.pack(pady=5)

    Acc_no = tk.Label(Info_Frame, text=f"Your Account Number: {acc_no}", font=("Helvetica", 11, "bold"), bg="white", fg="#333333")
    Acc_no.pack(anchor="w", pady=2)

    Action_Frame = tk.Frame(main_window, bg="#AAF2F2")
    Action_Frame.pack(pady=25)

    Deposit_Btn = tk.Button(Action_Frame, text="Deposit", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", width=12, relief="flat", cursor="hand2", command=lambda: draw_deposit_screen(acc_no))
    Deposit_Btn.grid(row=0, column=0, padx=12)

    Withdraw_Btn = tk.Button(Action_Frame, text="Withdraw", font=("Helvetica", 11, "bold"), bg="#f44336", fg="white", width=12, relief="flat", cursor="hand2", command=lambda: draw_withdraw_screen(acc_no))
    Withdraw_Btn.grid(row=0, column=1, padx=12)

    Mini_Stmt_Btn = tk.Button(Action_Frame, text="Mini Statement", font=("Helvetica", 11, "bold"), bg="#007BFF", fg="white", width=12, relief="flat", cursor="hand2", command=lambda: draw_mini_statement(acc_name, acc_balance, acc_no))
    Mini_Stmt_Btn.grid(row=0, column=2, padx=12)

    Logout_Btn = tk.Button(main_window, text="Log Out", font=("Helvetica", 10), bg="#e0e0e0", fg="#333333", width=14, relief="flat", cursor="hand2", command=draw_homepage)
    Logout_Btn.pack(pady=5)

def draw_emp_login_screen():
    clear_window()
    main_window.title("Bank Management - Employee Login")

    Header = tk.Label(main_window, text="Employee Login", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Username_Label = tk.Label(Card_Frame, text="Employee ID", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Username_Label.pack(anchor="center", pady=(30, 2), padx=(0, 230))
    Username_Input = PlaceHolderEntry(Card_Frame, placeholder="Enter Your 10-Digit Employee ID", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Username_Input.pack(anchor="center", pady=(0, 15))

    Password_Label = tk.Label(Card_Frame, text="Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Password_Label.pack(anchor="center", pady=(20, 2), padx=(0, 250))
    Password_Input = PlaceHolderEntry(Card_Frame, placeholder="Enter Your Employee Password", is_password=True, font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Password_Input.pack(anchor="center", pady=(0, 30))

    def attempt_emp_login():
        username = Username_Input.get()
        password = Password_Input.get()

        if not username.strip()or not password.strip():
            messagebox.showwarning("Invalid Input", "Please Enter Both Your Username And Password Correctly !")
            return
        try:
            cursor.execute("SELECT Emp_Psswd FROM Employee_Credentials WHERE Emp_ID = %s", (username,))
            result = cursor.fetchone()

            if result is not None and result[0] == password:
                cursor.execute("SELECT Emp_Name FROM Employees WHERE Emp_ID = %s", (username,))
                result = cursor.fetchone()
                emp_name = result[0] if result else "[Employee-Name-Pending]"                
                draw_employee_dashboard(username, emp_name)
                print(f"Logged In Succesfully {username}")
            else:
                messagebox.showerror("Login Failed", "Invalid Username Or Password !! \n\n Please Check Your Username And Password")
        except sql.Error as err:
            print(f"Databse Error: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(30,0))

    Login_Btn = tk.Button(Button_Frame, text="Login", font=("Helvetica", 13, "bold"), bg="#009933", fg="white", relief="flat", cursor="hand2", command=attempt_emp_login, width=32)
    Login_Btn.grid(row=0, column=0, columnspan=2, pady=(0, 18))

    Acc_Create_selector = tk.Button(Button_Frame, text="Add Employee", font=("Helvetica", 13), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=draw_emp_create_screen, width=16)
    Acc_Create_selector.grid(row=1, column=0, padx=(0, 8))

    Back_Homepage = tk.Button(Button_Frame, text="Back To Homepage", font=("Helvetica", 13), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=draw_homepage, width=16)
    Back_Homepage.grid(row=1, column=1, padx=(8, 0))

def draw_emp_create_screen():
    clear_window()
    main_window.title("Bank Management - Add New Employee")

    Header = tk.Label(main_window, text="New Employee Admission", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Emp_Name_Label = tk.Label(Card_Frame, text="Enter Your Full Name", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Emp_Name_Label.pack(anchor="center", pady=(30, 2), padx=(0,170))
    Emp_Name_Input = PlaceHolderEntry(Card_Frame, placeholder="*Required", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Emp_Name_Input.pack(anchor="center", pady=(0, 15))

    Employer_Code_Label = tk.Label(Card_Frame, text="Employer Code", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Employer_Code_Label.pack(anchor="center", pady=(20, 2), padx=(0,215))
    Employer_Code_Input = PlaceHolderEntry(Card_Frame, placeholder="*Contact Employer For Code", is_password=True, font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Employer_Code_Input.pack(anchor="center", pady=(0, 15))

    Password_Label = tk.Label(Card_Frame, text="Create A Strong Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Password_Label.pack(anchor="center", pady=(20, 2), padx=(0,135))
    Password_Input = PlaceHolderEntry(Card_Frame, placeholder="*Required", is_password=True, font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    Password_Input.pack(anchor="center", pady=(0, 15))

    def attempt_emp_create():
        username = Emp_Name_Input.get()
        password = Password_Input.get()
        empr_code = Employer_Code_Input.get()

        if not username.strip() or not password.strip() or not empr_code.strip():
            messagebox.showerror("Invalid Input", "Please Fill All Required Fields Properly !")
            return

        if empr_code == "IAMEMPLOYER1234":    
            try:                
                emp_id = gen_unique_emp_id(cursor)
                cursor.execute("INSERT INTO Employees (Emp_ID, Emp_Name) VALUES (%s, %s)", (emp_id, username))
                cursor.execute("INSERT INTO Employee_Credentials (Emp_ID, Emp_Psswd) VALUES (%s, %s)", (emp_id, password))
                db.commit()
                print(f"Employee Registered Successfully Employee ID: {emp_id}")
                messagebox.showinfo("Employee Registered !", f"Employee Is Registered Successfully ! \n\n Employee ID Is: {emp_id}")
                draw_emp_login_screen()
                
            except sql.Error as err:
                print(f"Database Error: {err}")
        else:
            messagebox.showerror("Wrong Employer Code !!", "Please Input Correct Employer Code !!")
            print("Please Input Correct Employer Code !!")
            return

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(20,0))

    Create_Btn = tk.Button(Button_Frame, text="Add Employee", font=("Helvetica", 13, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", command=attempt_emp_create, width=32)
    Create_Btn.grid(row=0, column=0, columnspan=2, pady=(0, 18))

    Back_Btn = tk.Button(Button_Frame, text="Back To Login", font=("Helvetica", 13), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=draw_emp_login_screen, width=30)
    Back_Btn.grid(row=1, column=0, padx=(20,0))

def draw_edit_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Edit Customer Details")

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=40)

    acc_no_label = tk.Label(Card_Frame, text="Enter Customer Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    acc_no_label.pack(pady=(10, 5))
    acc_no_entry = PlaceHolderEntry(Card_Frame, placeholder="e.g. 512345678901234", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    acc_no_entry.pack(pady=(0, 20))

    def fetch_account():
        acc_no = acc_no_entry.get().strip()
        
        if not acc_no:
            messagebox.showwarning("Input Error", "Please enter an account number.")
            return

        try:
            cursor.execute("SELECT Acc_No FROM Accounts WHERE Acc_No = %s", (acc_no,))
            result = cursor.fetchone()

            if result is not None:
                # If found, move to Step 2!
                draw_update_fields(acc_no, emp_id, emp_name)
            else:
                messagebox.showerror("Not Found", "Invalid Account Number. Please try again.")
        except sql.Error as err:
            print(f"Database Error: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(10, 0))

    Search_Btn = tk.Button(Button_Frame, text="Search Account", font=("Helvetica", 12, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", command=fetch_account, width=20)
    Search_Btn.grid(row=0, column=0, pady=(0, 15), columnspan=2)

    Back_Btn = tk.Button(Button_Frame, text="Back to Dashboard", font=("Helvetica", 11), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=lambda: draw_employee_dashboard(emp_id, emp_name)) # Change "EMP" to actual current employee ID variable if you have it stored globally
    Back_Btn.grid(row=1, column=0, columnspan=2)

def draw_update_fields(acc_no, emp_id, emp_name):
    clear_window()
    main_window.title(f"Bank Management - Updating {acc_no}")

    Header = tk.Label(main_window, text=f"Updating Account: {acc_no}", font=("Helvetica", 20, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(30, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)
    
    Info_Label = tk.Label(Card_Frame, text="Leave fields blank if you do not want to change them.", font=("Helvetica", 10, "italic"), bg="white", fg="#777777")
    Info_Label.pack(pady=(10, 20))

    new_name_label = tk.Label(Card_Frame, text="New Customer Name", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    new_name_label.pack(anchor="w", padx=(30, 0), pady=(0, 2))
    new_name_input = PlaceHolderEntry(Card_Frame, placeholder="Enter New Name", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    new_name_input.pack(pady=(0, 15))

    new_usrnm_label = tk.Label(Card_Frame, text="New Username", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    new_usrnm_label.pack(anchor="w", padx=(30, 0), pady=(0, 2))
    new_usrnm_input = PlaceHolderEntry(Card_Frame, placeholder="Enter New Username", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    new_usrnm_input.pack(pady=(0, 15))

    new_password_label = tk.Label(Card_Frame, text="New Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    new_password_label.pack(anchor="w", padx=(30, 0), pady=(0, 2))
    new_password_input = PlaceHolderEntry(Card_Frame, placeholder="Enter New Password", is_password=True, font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    new_password_input.pack(pady=(0, 25))

    def attempt_update():
        new_name = new_name_input.get().strip()
        new_username = new_usrnm_input.get().strip()
        new_password = new_password_input.get().strip()

        if not new_name and not new_username and not new_password:
            messagebox.showinfo("No Changes", "No changes were entered.")
            return
        try:
            if new_name:
                cursor.execute("UPDATE Accounts SET Acc_Name = %s WHERE Acc_No = %s", (new_name, acc_no))
            
            if new_username:
                cursor.execute("UPDATE Account_Credentials SET Usrnm = %s WHERE Acc_No = %s", (new_username, acc_no))

            if new_password:
                cursor.execute("UPDATE Account_Credentials SET Psswd = %s WHERE Acc_No = %s", (new_password, acc_no))

            db.commit()
            messagebox.showinfo("Success", f"Account {acc_no} updated successfully!")
            draw_edit_screen(emp_id, emp_name)

        except sql.Error as err:
            print(f"Database Error: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack()

    Update_Btn = tk.Button(Button_Frame, text="Update Details", font=("Helvetica", 12, "bold"), bg="#009933", fg="white", relief="flat", cursor="hand2", command=attempt_update, width=18)
    Update_Btn.grid(row=0, column=0, padx=10)

    Cancel_Btn = tk.Button(Button_Frame, text="Cancel", font=("Helvetica", 12), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=lambda: draw_edit_screen(emp_id, emp_name), width=12)
    Cancel_Btn.grid(row=0, column=1, padx=10)

def draw_transfer_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Transfer Funds")

    Header = tk.Label(main_window, text="Transfer Funds", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    sender_label = tk.Label(Card_Frame, text="Sender Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    sender_label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    sender_entry = PlaceHolderEntry(Card_Frame, placeholder="e.g. 512345678901234", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    sender_entry.pack(anchor="center", pady=(0, 15))

    receiver_label = tk.Label(Card_Frame, text="Receiver Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    receiver_label.pack(anchor="center", pady=(10, 2), padx=(0, 135))
    receiver_entry = PlaceHolderEntry(Card_Frame, placeholder="e.g. 512345678901234", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    receiver_entry.pack(anchor="center", pady=(0, 15))

    transfer_amt_label = tk.Label(Card_Frame, text="Amount To Transfer (₹)", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    transfer_amt_label.pack(anchor="center", pady=(10, 2), padx=(0, 150))
    transfer_amt_entry = PlaceHolderEntry(Card_Frame, placeholder="0.00", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    transfer_amt_entry.pack(anchor="center", pady=(0, 30))

    def attempt_transfer():

        sender_acc = sender_entry.get().strip()
        reciever_acc = receiver_entry.get().strip()
        amt_str = transfer_amt_entry.get().strip()

        if not sender_acc or not reciever_acc or not amt_str:
            messagebox.showwarning("Invalid Input", "Please Fill All Required Fields")
            return

        if sender_acc == reciever_acc:
            messagebox.showwarning("Invalid Transfer", "Sender and Receiver accounts cannot be the same.")
            return

        try:
            amt = float(amt_str)
            if amt <= 0:
                messagebox.showwarning("Invalid Amount", "Transfer amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount.")
            return

        try:
            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (sender_acc,))
            sender = cursor.fetchone()

            if sender is None:
                messagebox.showerror("Error", "Sender account not found!")
                return

            sender_balance = float(sender[0])

            if sender_balance < amt:
                messagebox.showerror("Declined", f"Insufficient funds. Sender only has ₹{sender_balance:,.2f}")
                return

            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (reciever_acc,))
            reciever = cursor.fetchone()

            if reciever is None:
                messagebox.showerror("Error", "Receiver account not found!")
                return

            reciever_balance = float(reciever[0])

            new_sender_balance = sender_balance - amt
            new_reciever_balance = reciever_balance + amt
            trans_id = gen_unique_trnsc_id()

            cursor.execute("UPDATE Accounts SET Acc_Balance = %s WHERE Acc_No = %s", (new_sender_balance, sender_acc))
            cursor.execute("UPDATE Accounts SET Acc_Balance = %s WHERE Acc_No = %s", (new_reciever_balance, reciever_acc))
            cursor.execute("INSERT INTO Transactions (Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time) VALUES (%s, %s, %s, %s, NOW())", (trans_id, sender_acc, reciever_acc, amt)) 
            db.commit()
            messagebox.showinfo("Transfer Successful", f"Successfully transferred ₹{amt:,.2f}!\n\nTransaction ID: {trans_id}")
            draw_employee_dashboard(emp_id, emp_name)
        except sql.Error as err:
            db.rollback()
            messagebox.showerror("Database Error", f"Transfer failed: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(10, 0))

    trnsf_btn = tk.Button(Button_Frame, text="Complete Transfer", font=("Helvetica", 13, "bold"), bg="#009933", fg="white", relief="flat", cursor="hand2", command=attempt_transfer, width=32)
    trnsf_btn.grid(row=0, column=0, pady=(0, 15))

    back_btn = tk.Button(Button_Frame, text="Back To Dashboard", font=("Helvetica", 11), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=lambda: draw_employee_dashboard(emp_id, emp_name), width=20)
    back_btn.grid(row=1, column=0)

def draw_statement_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Get Account Statement")

    Header = tk.Label(main_window, text="Account Statement", font=("Helvetica", 24, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(40, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    acc_no_label = tk.Label(Card_Frame, text="Customer Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    acc_no_label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    acc_no_entry = PlaceHolderEntry(Card_Frame, placeholder="e.g. 512345678901234", font=("Helvetica", 12), width=35, bg="#F9F9F9", relief="flat", highlightthickness=1, highlightbackground="#CCCCCC")
    acc_no_entry.pack(anchor="center", pady=(0, 25))

    def fetch_statement():
        acc_no = acc_no_entry.get().strip()
        if not acc_no:
            messagebox.showwarning("Input Error", "Please enter an account number.")
            return

        try:
            cursor.execute("SELECT Acc_Name, Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
            acc_info = cursor.fetchone()
            
            if acc_info is None:
                messagebox.showerror("Not Found", "Account Number not found.")
                return

            # Fetch transactions where the user is either the sender or the receiver
            cursor.execute("SELECT Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time FROM Transactions WHERE Sender = %s OR Reciever = %s ORDER BY Trns_Time DESC", (acc_no, acc_no))
            transactions = cursor.fetchall()

            # Wipe screen and draw statement output
            clear_window()
            main_window.title(f"Bank Management - Statement for {acc_no}")

            St_Header = tk.Label(main_window, text=f"Statement for {acc_info[0]}", font=("Helvetica", 22, "bold"), bg="#AAF2F2", fg="#003366")
            St_Header.pack(pady=(20, 5))

            Bal_Header = tk.Label(main_window, text=f"Current Balance: ₹{acc_info[1]:,.2f}", font=("Helvetica", 16, "bold"), bg="#AAF2F2", fg="#009933")
            Bal_Header.pack(pady=(0, 20))

            List_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
            List_Frame.pack(padx=40, fill="both", expand=True, pady=(0, 20))

            scrollbar = tk.Scrollbar(List_Frame)
            scrollbar.pack(side="right", fill="y")

            # Using a Text widget to cleanly display fixed-width data
            txt = tk.Text(List_Frame, font=("Courier", 10), yscrollcommand=scrollbar.set, bg="#F9F9F9", padx=10, pady=10)
            txt.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=txt.yview)

            txt.insert(tk.END, f"{'Date & Time':<19} | {'Transaction ID':<30} | {'Type':<6} | {'Amount (₹)'}\n")
            txt.insert(tk.END, "-"*84 + "\n")

            if not transactions:
                txt.insert(tk.END, "No transactions found for this account.\n")
                txt.config(state="disabled")
            else:
                for t in transactions:
                    t_id, t_send, t_recv, t_amt, t_time = t
                    t_date_str = t_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    if t_send == acc_no:
                        t_type = "DEBIT"
                    else:
                        t_type = "CREDIT"
                        
                    txt.insert(tk.END, f"{t_date_str:<19} | {t_id:<30} | {t_type:<6} | {t_amt:,.2f}\n")

            txt.config(state="disabled") # Make text read-only

            Back_Btn = tk.Button(main_window, text="Back To Dashboard", font=("Helvetica", 12, "bold"), bg="#4A5568", fg="white", relief="flat", cursor="hand2", command=lambda: draw_employee_dashboard(emp_id, emp_name), width=25)
            Back_Btn.pack(pady=(0, 20))

        except sql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch statement: {err}")

    Button_Frame = tk.Frame(Card_Frame, bg="white")
    Button_Frame.pack(pady=(10, 0))

    Search_Btn = tk.Button(Button_Frame, text="Get Statement", font=("Helvetica", 12, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", command=fetch_statement, width=32)
    Search_Btn.grid(row=0, column=0, pady=(0, 15))

    Back_Btn = tk.Button(Button_Frame, text="Back to Dashboard", font=("Helvetica", 11), bg="#E0E0E0", fg="#333333", relief="flat", cursor="hand2", command=lambda: draw_employee_dashboard(emp_id, emp_name), width=20)
    Back_Btn.grid(row=1, column=0)

def draw_employee_dashboard(Emp_ID, Emp_Name):
    clear_window()
    main_window.title(f"Bank Management - Employee Dashboard ({Emp_ID})")

    Header = tk.Label(main_window, text="Employee Dashboard", font=("Helvetica", 26, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(30, 5))

    SubHeader = tk.Label(main_window, text=f"Logged in: {Emp_Name}", font=("Helvetica", 13), bg="#AAF2F2", fg="#555555")
    SubHeader.pack(pady=(0, 20))

    Card_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
    Card_Frame.pack(padx=80, pady=10, ipadx=40, ipady=30, fill="x")

    Action_Title = tk.Label(Card_Frame, text="Administrative Actions", font=("Helvetica", 16, "bold"), bg="white", fg="#333333")
    Action_Title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

    crt_new_cus = tk.Label(Card_Frame, text="Create New Customer Account", font=("Helvetica", 13), bg="white", fg="#555555")
    crt_new_cus.grid(row=1, column=0, sticky="w", pady=10)
    crt_new_cus_btn = tk.Button(Card_Frame, text="Create", font=("Helvetica", 11, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", width=15, command=lambda: draw_create_screen(Emp_ID, Emp_Name))
    crt_new_cus_btn.grid(row=1, column=1, sticky="e", pady=10)

    edit_cus_details = tk.Label(Card_Frame, text="Edit Existing Customer Details", font=("Helvetica", 13), bg="white", fg="#555555")
    edit_cus_details.grid(row=2, column=0, sticky="w", pady=10)
    edit_cus_details_btn = tk.Button(Card_Frame, text="Edit", font=("Helvetica", 11, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", width=15, command=lambda: draw_edit_screen(Emp_ID, Emp_Name))
    edit_cus_details_btn.grid(row=2, column=1, sticky="e", pady=10)

    trnsfr_money = tk.Label(Card_Frame, text="Transfer Money Between Customer Accounts", font=("Helvetica", 13), bg="white", fg="#555555")
    trnsfr_money.grid(row=3, column=0, sticky="w", pady=10)
    trnsfr_money_btn = tk.Button(Card_Frame, text="Transfer", font=("Helvetica", 11, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", width=15, command=lambda: draw_transfer_screen(Emp_ID, Emp_Name))
    trnsfr_money_btn.grid(row=3, column=1, sticky="e", pady=10)

    stmnt = tk.Label(Card_Frame, text="Generate Account Statement For Customer", font=("Helvetica", 13), bg="white", fg="#555555")
    stmnt.grid(row=5, column=0, sticky="w", pady=10)
    stmnt_btn = tk.Button(Card_Frame, text="Get Statement", font=("Helvetica", 11, "bold"), bg="#007BFF", fg="white", relief="flat", cursor="hand2", width=15, command=lambda: draw_statement_screen(Emp_ID, Emp_Name))
    stmnt_btn.grid(row=5, column=1, sticky="e", pady=10)

    Card_Frame.grid_columnconfigure(0, weight=1)

    Logout_Btn = tk.Button(main_window, text="Log Out", font=("Helvetica", 12, "bold"), bg="#f44336", fg="white", relief="flat", cursor="hand2", width=20, command=draw_homepage)
    Logout_Btn.pack(pady=25)

def draw_mini_statement(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title(f"Bank Management - Mini Statement for {acc_no}")

    Header = tk.Label(main_window, text=f"Mini Statement for Account: {acc_no}", font=("Helvetica", 22, "bold"), bg="#AAF2F2", fg="#003366")
    Header.pack(pady=(20, 5))

    try:
        cursor.execute("SELECT Acc_Name, Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
        acc_info = cursor.fetchone()

        if acc_info is None:
            messagebox.showerror("Not Found", "Account Number not found.")
            draw_homepage()
            return

        # Fetch last 10 transactions where the user is either the sender or the receiver
        cursor.execute("SELECT Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time FROM Transactions WHERE Sender = %s OR Reciever = %s ORDER BY Trns_Time DESC LIMIT 10", (acc_no, acc_no))
        transactions = cursor.fetchall()

        List_Frame = tk.Frame(main_window, bg="white", bd=1, relief="solid")
        List_Frame.pack(padx=40, fill="both", expand=True, pady=(0, 20))

        txt = tk.Text(List_Frame, font=("Courier", 10), bg="#F9F9F9", padx=10, pady=10)
        txt.pack(side="left", fill="both", expand=True)

        txt.insert(tk.END, f"{'Date & Time':<20} | {'Transaction ID':<31} | {'Type':<7} | {'Amount (₹)'}\n")
        txt.insert(tk.END, "-"*87 + "\n")

        if not transactions:
            txt.insert(tk.END, "No recent transactions found for this account.\n")
            txt.config(state="disabled")
        else:
            for t in transactions:
                t_id, t_send, t_recv, t_amt, t_time = t
                t_date_str = t_time.strftime("%Y-%m-%d %H:%M:%S")
                
                if t_send == acc_no:
                    t_type = "DEBIT"
                else:
                    t_type = "CREDIT"
                txt.insert(tk.END, f"{t_date_str:<20} | {t_id:<31} | {t_type:<7} | {t_amt:,.2f}\n")
        txt.insert(tk.END, "\n\n" +"-"*21 + "*For Older Transactions Please Contact Bank*" + "-"*22 + "\n")
        txt.config(state="disabled") # Make text read-only

        Back_Btn = tk.Button(main_window, text="Back To Dashboard", font=("Helvetica", 12, "bold"), bg="#4A5568", fg="white", relief="flat", cursor="hand2", command=lambda: draw_dashboard(acc_name, acc_balance, acc_no), width=25)
        Back_Btn.pack(pady=(0, 20))

    except sql.Error as err:
        messagebox.showerror("Database Error", f"Failed to fetch mini statement: {err}")
        draw_dashboard(acc_name, acc_balance, acc_no)

main_window = tk.Tk() #The main program window
main_window.title("Bank Management")
main_window.resizable(False,False)
main_window.geometry("800x600+550+200") #To set the window size to 800 by 600 pixels and to pop it in the middle of the screen
main_window.configure(background="#AAF2F2") #Setting the background colour

draw_homepage()

"""acc_create_mode = False

def change_mode(acc_create_mode):
    acc_create_mode = True

#Input Window Design
if acc_create_mode is False:
    Header = tk.Label(main_window, text="Log Into Existing Account", font=("Helvetica", 25)).pack(anchor="center", pady=80, fill="x")
    Username_Label = tk.Label(main_window, text="Please Enter Your Username", font=("Helvetica", 12)).pack(anchor="w", padx=90, pady=30)
    Username_Input = tk.Entry(main_window)
    Username_Input.pack(anchor="w", padx=90)
    Password = tk.Label(main_window, text="Please Enter Your Password", font=("Helvetica", 12)).pack(anchor="w", padx=90, pady=30)
    Password_Input = tk.Entry(main_window)
    Password_Input.pack(anchor="w", padx=90)
    Acc_Create_selector = tk.Label(main_window, text="Create A New Account", fg="blue", font=("Arial", 12))
    Acc_Create_selector.pack(pady=50)
    Acc_Create_selector.bind("<Button-1>", lambda e: change_mode(acc_create_mode))
    Acc_Create_selector.bind("<Enter>", lambda e: Acc_Create_selector.config(fg="red", cursor="hand2"))
    Acc_Create_selector.bind("<Leave>", lambda e: Acc_Create_selector.config(fg="blue", cursor=""))
    try:
        username = Username_Input.get()
        password = Password_Input.get()
        password_check = cursor.fetchone("SELECT Psswd FROM Account_Credentials WHERE Usrnm = %s", (username,))
        if password_check == password:
            print(f"Logged In Succesfully {username}")
        elif password_check != password:
            print("Please check username and password")
    except sql.Error as err:
        print(f"Database Error: {err}")

#Account Creation Code
elif acc_create_mode is True:
    Header = tk.Label(main_window, text="Create A New Account", font=("Helvetica", 25)).pack(anchor="center", pady=80, fill="x")
    Acc_Name_Label = tk.Label(main_window, text="Please Enter Your Full Name", font=("Helvetica", 12)).pack()
    Acc_Name_Input = tk.Entry(main_window).pack(anchor="w", padx=90)
    Username_Label = tk.Label(main_window, text="Please Enter Your Username", font=("Helvetica", 12)).pack(anchor="w", padx=90, pady=30)
    Username_Input = tk.Entry(main_window)
    Username_Input.pack(anchor="w", padx=90)
    Password = tk.Label(main_window, text="Please Enter Your Password", font=("Helvetica", 12)).pack(anchor="w", padx=90, pady=30)
    Password_Input = tk.Entry(main_window)
    Password_Input.pack(anchor="w", padx=90)
    username = Username_Input.get()
    password = Password_Input.get()
    acc_name = Acc_Name_Input.get()
    try:
        acc_no = gen_unique_acc_no(cursor)
        cursor.execute("INSERT INTO Accounts (Acc_No, Acc_Name, Acc_Balance, Acc_opn_date) VALUES (%s, %s, %s, NOW())", (acc_no, acc_name, 0.00,))
        cursor.execute("INSERT INTO Account_Credentials (Acc_No, Usrnm, Psswd) VALUES (%s, %s, %s)", (acc_no, username, password))
        db.commit()
    except sql.Error as err:
        print(f"Databse Error: {err}")"""

main_window.mainloop() #Running the main program to genrate the window