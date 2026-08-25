import customtkinter as ctk
import tkinter.messagebox as messagebox
import mysql.connector as sql
import random
import string
import datetime

ctk.set_appearance_mode("Light")  # Can be "Light", "Dark", or "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

db = sql.connect(host="localhost", user="root", password="1234", database="Bank_Mng")
cursor = db.cursor(buffered=True)

# ==========================================
# GLOBAL UI THEME SETTINGS
# ==========================================
COLORS = {
    "bg": "#AAF2F2",             # Brand Theme: Light airy cyan for the main app background
    "card_bg": "#FFFFFF",        # Pure White for floating cards to pop against the cyan
    
    "primary": "#00838F",        # Deep Teal for main buttons/headers (beautiful contrast to the cyan)
    "primary_hover": "#006064",  # Darker Teal for smooth hover effects
    
    "dark_btn": "#1E293B",       # Midnight Slate for Employee actions (adds professional gravity)
    "dark_hover": "#0F172A",     # Deeper Midnight
    
    "success": "#2A9D8F",        # Soft Emerald Green for Deposits/Success (calmer than harsh neon green)
    "danger": "#EF476F",         # Vibrant Coral Pink for Withdraw/Logout (modern alternative to pure red)
    
    "text_main": "#0F172A",      # Very dark slate blue for text (softer on the eyes than pure black)
    "text_muted": "#64748B",     # Cool grey for descriptions and placeholders
    "border": "#80D4D4",         # Slightly darker cyan for subtle dividers and borders
    "secondary": "#F1F5F9",      # Very light cool-grey for back/cancel buttons
    "secondary_hover": "#E2E8F0" # Slightly darker cool-grey for hover
}

FONTS = {
    "h1": ("Helvetica", 24, "bold"),
    "h2": ("Helvetica", 18, "bold"),
    "h3": ("Helvetica", 14, "bold"),
    "body": ("Helvetica", 12),
    "body_bold": ("Helvetica", 12, "bold"),
    "small": ("Helvetica", 10),
    "mono": ("Courier", 10)  # For the statement screen
}

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

    Header = ctk.CTkLabel(main_window, text="Welcome to Bank Management", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(60, 40))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=(10, 60), padx=60, fill="both", expand=True)

    Customer_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Customer_Frame.pack(side="left", expand=True, fill="both", padx=20)

    Cus_Inner = ctk.CTkFrame(Customer_Frame, fg_color="transparent")
    Cus_Inner.pack(expand=True)

    Cus_Title = ctk.CTkLabel(Cus_Inner, text="For Customers", font=("Helvetica", 24, "bold"), text_color=COLORS["text_main"])
    Cus_Title.pack(pady=(0, 10))

    Cus_Desc = ctk.CTkLabel(Cus_Inner, text="Access your personal accounts,\ntransfer funds, and view balances.", font=("Helvetica", 16), text_color=COLORS["text_muted"], justify="center")
    Cus_Desc.pack(pady=(0, 30))

    Cus_Btn = ctk.CTkButton(Cus_Inner, text="Customer Portal", font=("Helvetica", 16, "bold"), corner_radius=8, height=45, width=200, fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], command=draw_login_screen)
    Cus_Btn.pack()

    Divider = ctk.CTkFrame(Card_Frame, width=2, fg_color=COLORS["secondary_hover"])
    Divider.pack(side="left", fill="y", pady=40)

    Employee_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Employee_Frame.pack(side="right", expand=True, fill="both", padx=20)

    Emp_Inner = ctk.CTkFrame(Employee_Frame, fg_color="transparent")
    Emp_Inner.pack(expand=True)

    Emp_Title = ctk.CTkLabel(Emp_Inner, text="For Employees", font=("Helvetica", 24, "bold"), text_color=COLORS["text_main"])
    Emp_Title.pack(pady=(0, 10))

    Emp_Desc = ctk.CTkLabel(Emp_Inner, text="Manage user accounts, verify\ntransactions, and assist customers.", font=("Helvetica", 16), text_color=COLORS["text_muted"], justify="center")
    Emp_Desc.pack(pady=(0, 30))

    Emp_Btn = ctk.CTkButton(Emp_Inner, text="Employee Portal", font=("Helvetica", 16, "bold"), corner_radius=8, height=45, width=200, fg_color=COLORS["dark_btn"], hover_color=COLORS["dark_hover"], command=draw_emp_login_screen)
    Emp_Btn.pack()

def draw_login_screen():
    clear_window()
    main_window.title("Bank Management - Login")

    Header = ctk.CTkLabel(main_window, text="Customer Login", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    Username_Label = ctk.CTkLabel(Form_Frame, text="Username", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Username_Label.pack(anchor="w", pady=(0, 5))
    Username_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Enter Your Username", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Username_Input.pack(pady=(0, 20))

    Password_Label = ctk.CTkLabel(Form_Frame, text="Password", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Password_Label.pack(anchor="w", pady=(0, 5))
    Password_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Enter Your Password", show="*", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Password_Input.pack(pady=(0, 30))

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

    Login_Btn = ctk.CTkButton(Form_Frame, text="Login", font=("Helvetica", 18, "bold"), fg_color=COLORS["success"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=attempt_login)
    Login_Btn.pack(pady=(0, 15))

    Back_Homepage = ctk.CTkButton(Form_Frame, text="Back To Homepage", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=draw_homepage)
    Back_Homepage.pack()

def draw_create_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Create Account")

    Header = ctk.CTkLabel(main_window, text="Create Customer Account", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(25, 15))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=50, ipady=25)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    Acc_Name_Label = ctk.CTkLabel(Form_Frame, text="Enter Your Full Name", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Acc_Name_Label.pack(anchor="w", pady=(0, 5))
    Acc_Name_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Customer Full Name", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Acc_Name_Input.pack(pady=(0, 15))

    Username_Label = ctk.CTkLabel(Form_Frame, text="Choose A Username", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Username_Label.pack(anchor="w", pady=(0, 5))
    Username_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Choose A Username", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Username_Input.pack(pady=(0, 15))

    Password_Label = ctk.CTkLabel(Form_Frame, text="Create A Strong Password", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Password_Label.pack(anchor="w", pady=(0, 5))
    Password_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Create Password", show="*", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Password_Input.pack(pady=(0, 25))

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

    Create_Btn = ctk.CTkButton(Form_Frame, text="Create Account", font=("Helvetica", 18, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=attempt_create)
    Create_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.pack()

def draw_withdraw_screen(acc_no):
    clear_window()
    main_window.title("Bank Management - Withdraw Funds")

    try:
        cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
        balance_data = cursor.fetchone()
        current_balance = float(balance_data[0]) if balance_data else 0.00
    except sql.Error:
        current_balance = 0.00

    Header = ctk.CTkLabel(main_window, text="Withdraw Funds", font=("Helvetica", 36, "bold"), text_color=COLORS["danger"])
    Header.pack(pady=(60, 60))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    Withdraw_Label = ctk.CTkLabel(Form_Frame, text="Enter Withdrawal Amount (₹)", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Withdraw_Label.pack(anchor="w", pady=(0, 2))

    Balance_Label = ctk.CTkLabel(Form_Frame, text=f"Available Balance: ₹{current_balance:,.2f}", font=("Helvetica", 14), text_color=COLORS["text_muted"])
    Balance_Label.pack(anchor="w", pady=(0, 10))
    
    Withdraw_Entry = ctk.CTkEntry(Form_Frame, placeholder_text="Amount (₹)", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Withdraw_Entry.pack(pady=(0, 30))

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
            
            db_balance = float(result[0])
            if db_balance < amt:
                messagebox.showerror("Declined", f"Insufficient funds. You only have ₹{db_balance:,.2f}")
                return

            new_balance = db_balance - amt
            trans_id = gen_unique_trnsc_id()

            cursor.execute("UPDATE Accounts SET Acc_Balance = %s WHERE Acc_No = %s", (new_balance, acc_no))
            cursor.execute("INSERT INTO Transactions (Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time) VALUES (%s, %s, %s, %s, NOW())", (trans_id, acc_no, "SELF_WITHDRAW", amt))
            db.commit()

            messagebox.showinfo("Withdrawal Successful", f"Successfully withdrew ₹{amt:,.2f}!\n\nTransaction ID: {trans_id}")
            go_back()

        except sql.Error as err:
            db.rollback()
            messagebox.showerror("Database Error", f"Withdrawal failed: {err}")

    Withdraw_Btn = ctk.CTkButton(Form_Frame, text="Complete Withdrawal", font=("Helvetica", 18, "bold"), fg_color=COLORS["danger"], hover_color="#C82333", height=45, width=320, corner_radius=8, command=attempt_withdraw)
    Withdraw_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=go_back)
    Back_Btn.pack()

def draw_deposit_screen(acc_no):
    clear_window()
    main_window.title("Bank Management - Deposit Funds")

    try:
            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (acc_no,))
            balance_data = cursor.fetchone()
            current_balance = float(balance_data[0]) if balance_data else 0.00
    except sql.Error:
            current_balance = 0.00

    Header = ctk.CTkLabel(main_window, text="Deposit Funds", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(60, 60))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, ipadx=50, ipady=30)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    Deposit_Label = ctk.CTkLabel(Form_Frame, text="Enter Deposit Amount (₹)", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Deposit_Label.pack(anchor="w", pady=(0, 5))

    Balance_Label = ctk.CTkLabel(Form_Frame, text=f"Available Balance: ₹{current_balance:,.2f}", font=("Helvetica", 14), text_color=COLORS["text_muted"])
    Balance_Label.pack(anchor="w", pady=(0, 10))
    
    Deposit_Entry = ctk.CTkEntry(Form_Frame, placeholder_text="Deposit Amount (₹)", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Deposit_Entry.pack(pady=(0, 30))

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

    Deposit_Btn = ctk.CTkButton(Form_Frame, text="Complete Deposit", font=("Helvetica", 18, "bold"), fg_color=COLORS["success"], hover_color="#218838", height=45, width=320, corner_radius=8, command=attempt_deposit)
    Deposit_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=go_back)
    Back_Btn.pack()

def draw_dashboard(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title(f"Bank Management - Dashboard For {acc_name}")

    Header_Frame = ctk.CTkFrame(main_window, fg_color="transparent")
    Header_Frame.pack(fill="x", padx=60, pady=(30, 5))

    Header_Text_Frame = ctk.CTkFrame(Header_Frame, fg_color="transparent")
    Header_Text_Frame.pack(side="left", fill="both", expand=True)

    first_name = acc_name.split()[0] if acc_name else "Customer"

    Header = ctk.CTkLabel(Header_Text_Frame, text=f"Welcome Back, {first_name}!", font=("Helvetica", 32, "bold"), text_color=COLORS["primary"])
    Header.pack(anchor="w")

    Sub_Header = ctk.CTkLabel(Header_Text_Frame, text="Here Is Your Financial Summary Dashboard.", font=("Helvetica", 16), text_color=COLORS["text_muted"])
    Sub_Header.pack(anchor="w", pady=(0, 5))

    Logout_Btn = ctk.CTkButton(Header_Frame, text="Log Out", font=("Helvetica", 14, "bold"), fg_color=COLORS["secondary"], text_color=COLORS["danger"], hover_color=COLORS["secondary_hover"], height=35, width=100, corner_radius=8, command=draw_homepage)
    Logout_Btn.pack(side="right", anchor="n")

    Card_Frame = ctk.CTkFrame(main_window, fg_color=COLORS["primary"], corner_radius=15)
    Card_Frame.pack(padx=60, pady=10, fill="x", ipady=10)

    Balance_Title = ctk.CTkLabel(Card_Frame, text="AVAILABLE BALANCE", font=("Helvetica", 14, "bold"), text_color=COLORS["card_bg"])
    Balance_Title.pack(anchor="w", padx=30, pady=(15, 0))

    Formatted_Balance = f"₹{float(acc_balance):,.2f}" if acc_balance is not None else "₹0.00"
    Balance = ctk.CTkLabel(Card_Frame, text=Formatted_Balance, font=("Helvetica", 48, "bold"), text_color=COLORS["card_bg"])
    Balance.pack(anchor="w", padx=30, pady=(0, 5))

    Card_Footer = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Card_Footer.pack(fill="x", padx=30, pady=(5, 10))

    Acc_no_lbl = ctk.CTkLabel(Card_Footer, text=f"Account Number: {acc_no}", font=("Helvetica", 16, "bold"), text_color=COLORS["secondary"])
    Acc_no_lbl.pack(side="left")

    Action_Card = ctk.CTkFrame(main_window, fg_color=COLORS["dark_btn"], corner_radius=15)
    Action_Card.pack(fill="x", padx=60, pady=(15, 20))

    Action_Title = ctk.CTkLabel(Action_Card, text="Quick Actions", font=("Helvetica", 22, "bold"), text_color=COLORS["card_bg"])
    Action_Title.pack(anchor="w", padx=30, pady=(20, 0))

    Action_Frame = ctk.CTkFrame(Action_Card, fg_color="transparent")
    Action_Frame.pack(fill="both", expand=True, padx=15, pady=(5, 20))

    Action_Frame.grid_columnconfigure(0, weight=1)
    Action_Frame.grid_columnconfigure(1, weight=1)

    Deposit_Btn = ctk.CTkButton(Action_Frame, text="Deposit Funds", font=("Helvetica", 16, "bold"), fg_color=COLORS["success"], hover_color="#218838", height=50, corner_radius=10, command=lambda: draw_deposit_screen(acc_no))
    Deposit_Btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    Withdraw_Btn = ctk.CTkButton(Action_Frame, text="Withdraw Funds", font=("Helvetica", 16, "bold"), fg_color=COLORS["danger"], hover_color="#C82333", height=50, corner_radius=10, command=lambda: draw_withdraw_screen(acc_no))
    Withdraw_Btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    Mini_Stmt_Btn = ctk.CTkButton(Action_Frame, text="Account Statement", font=("Helvetica", 16, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=50, corner_radius=10, command=lambda: draw_mini_statement(acc_name, acc_balance, acc_no))
    Mini_Stmt_Btn.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    Txn_Search_Btn = ctk.CTkButton(Action_Frame, text="Search Transaction", font=("Helvetica", 16, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=50, corner_radius=10, command=lambda: draw_cus_transaction_details(acc_name, acc_balance, acc_no))
    Txn_Search_Btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

def draw_emp_login_screen():
    clear_window()
    main_window.title("Bank Management - Employee Login")

    Header = ctk.CTkLabel(main_window, text="Employee Login", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    Username_Label = ctk.CTkLabel(Form_Frame, text="Employee ID", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Username_Label.pack(anchor="w", pady=(0, 5))
    Username_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Enter Your 6-Digit ID", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Username_Input.pack(pady=(0, 20))

    Password_Label = ctk.CTkLabel(Form_Frame, text="Password", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Password_Label.pack(anchor="w", pady=(0, 5))
    Password_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Enter Your Password", show="*", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Password_Input.pack(pady=(0, 30))

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

    Login_Btn = ctk.CTkButton(Form_Frame, text="Login", font=("Helvetica", 18, "bold"), fg_color=COLORS["success"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=attempt_emp_login)
    Login_Btn.pack(pady=(0, 15))

    Split_Btn_Frame = ctk.CTkFrame(Form_Frame, fg_color="transparent")
    Split_Btn_Frame.pack(fill="x")

    Acc_Create_selector = ctk.CTkButton(Split_Btn_Frame, text="Add Employee", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=155, corner_radius=8, command=draw_emp_create_screen)
    Acc_Create_selector.pack(side="left")

    Back_Homepage = ctk.CTkButton(Split_Btn_Frame, text="Back To Home", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=155, corner_radius=8, command=draw_homepage)
    Back_Homepage.pack(side="right")

def draw_emp_create_screen():
    clear_window()
    main_window.title("Bank Management - Add New Employee")

    Header = ctk.CTkLabel(main_window, text="New Employee Admission", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(25, 15))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=50, ipady=25)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    Emp_Name_Label = ctk.CTkLabel(Form_Frame, text="Enter Your Full Name", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Emp_Name_Label.pack(anchor="w", pady=(0, 5))
    Emp_Name_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Enter Full Name", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Emp_Name_Input.pack(pady=(0, 15))

    Employer_Code_Label = ctk.CTkLabel(Form_Frame, text="Employer Code", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Employer_Code_Label.pack(anchor="w", pady=(0, 5))
    Employer_Code_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Employer Code", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"], show="*")
    Employer_Code_Input.pack(pady=(0, 15))

    Password_Label = ctk.CTkLabel(Form_Frame, text="Create A Strong Password", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Password_Label.pack(anchor="w", pady=(0, 5))
    Password_Input = ctk.CTkEntry(Form_Frame, placeholder_text="Create Password", show="*", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    Password_Input.pack(pady=(0, 25))

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

    Create_Btn = ctk.CTkButton(Form_Frame, text="Add Employee", font=("Helvetica", 16, "bold"), fg_color=COLORS["success"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=attempt_emp_create)
    Create_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Form_Frame, text="Back To Login", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=draw_emp_login_screen)
    Back_Btn.pack()

def draw_edit_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Edit Customer Details")

    Header = ctk.CTkLabel(main_window, text="Edit Customer Details", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(60, 60))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=50, ipady=40)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    acc_no_label = ctk.CTkLabel(Form_Frame, text="Enter Customer Account Number", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    acc_no_label.pack(anchor="w", pady=(0, 5))
    acc_no_entry = ctk.CTkEntry(Form_Frame, placeholder_text="Enter Customer Account Number", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    acc_no_entry.pack(pady=(0, 30))

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

    Search_Btn = ctk.CTkButton(Form_Frame, text="Search Account", font=("Helvetica", 18, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=fetch_account)
    Search_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.pack()

def draw_update_fields(acc_no, emp_id, emp_name):
    clear_window()
    main_window.title(f"Bank Management - Updating {acc_no}")

    try:
        cursor.execute("SELECT A.Acc_Name, C.Usrnm FROM Accounts A JOIN Account_Credentials C ON A.Acc_No = C.Acc_No WHERE A.Acc_No = %s", (acc_no,))
        data = cursor.fetchone()
        curr_name = data[0] if data else "Unknown"
        curr_usrnm = data[1] if data else "Unknown"
    except sql.Error as err:
        print(f"Database Error: {err}")
        curr_name, curr_usrnm = "Unknown", "Unknown"

    Header = ctk.CTkLabel(main_window, text="Update Customer Profile", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(30, 5))
    
    Info_Label = ctk.CTkLabel(main_window, text=f"Account Number: {acc_no}  •  Leave fields blank to keep current data", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    Info_Label.pack(pady=(0, 15))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(padx=60, pady=(5, 35), fill="both", expand=True)

    Card_Frame.grid_columnconfigure(0, weight=1)
    Card_Frame.grid_columnconfigure(1, weight=1)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.grid(row=0, column=0, padx=(40, 20), pady=20, sticky="n")

    name_var = ctk.StringVar()
    usrnm_var = ctk.StringVar()
    pass_var = ctk.StringVar()

    new_name_label = ctk.CTkLabel(Form_Frame, text="New Full Name", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    new_name_label.pack(anchor="w", pady=(0, 5))
    new_name_input = ctk.CTkEntry(Form_Frame, textvariable=name_var, placeholder_text="Enter new name...", font=("Helvetica", 16), width=320, height=40, corner_radius=8, border_color=COLORS["border"])
    new_name_input.pack(pady=(0, 10))

    new_usrnm_label = ctk.CTkLabel(Form_Frame, text="New Username", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    new_usrnm_label.pack(anchor="w", pady=(0, 5))
    new_usrnm_input = ctk.CTkEntry(Form_Frame, textvariable=usrnm_var, placeholder_text="Enter new username...", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    new_usrnm_input.pack(pady=(0, 15))

    new_password_label = ctk.CTkLabel(Form_Frame, text="New Password", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    new_password_label.pack(anchor="w", pady=(0, 5))
    new_password_input = ctk.CTkEntry(Form_Frame, textvariable=pass_var, placeholder_text="Enter new password...", show="*", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
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
            messagebox.showinfo("Success", f"Customer profile for Account {acc_no} updated successfully!")
            draw_edit_screen(emp_id, emp_name)

        except sql.Error as err:
            print(f"Database Error: {err}")

    Update_Btn = ctk.CTkButton(Form_Frame, text="Save Details", font=("Helvetica", 18, "bold"), fg_color=COLORS["success"], hover_color="#218838", height=45, width=320, corner_radius=8, command=attempt_update)
    Update_Btn.pack(pady=(0, 15))

    Cancel_Btn = ctk.CTkButton(Form_Frame, text="Cancel Changes", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_edit_screen(emp_id, emp_name))
    Cancel_Btn.pack()

    Preview_Frame = ctk.CTkFrame(Card_Frame, fg_color=COLORS["secondary"], corner_radius=15)
    Preview_Frame.grid(row=0, column=1, padx=(20, 40), pady=30, sticky="nwe")

    Preview_Title = ctk.CTkLabel(Preview_Frame, text="Live Profile Preview", font=("Helvetica", 20, "bold"), text_color=COLORS["primary"], anchor="w")
    Preview_Title.pack(fill="x", padx=25, pady=(25, 5))

    Tip_Label = ctk.CTkLabel(Preview_Frame, text="Pending changes will appear in green.", font=("Helvetica", 14, "italic"), text_color=COLORS["text_muted"], anchor="w", justify="left", wraplength=240)
    Tip_Label.pack(fill="x", padx=25, pady=(0, 15))

    preview_name = ctk.CTkLabel(Preview_Frame, text=f"Name: {curr_name}", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"], anchor="w")
    preview_name.pack(fill="x", padx=25, pady=(0, 15))

    preview_usrnm = ctk.CTkLabel(Preview_Frame, text=f"Username: {curr_usrnm}", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"], anchor="w")
    preview_usrnm.pack(fill="x", padx=25, pady=(0, 15))

    preview_pass = ctk.CTkLabel(Preview_Frame, text="Password: •••••••• (Unchanged)", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"], anchor="w")
    preview_pass.pack(fill="x", padx=25, pady=(0, 25))

    def update_preview(*args):
        n = name_var.get().strip()
        u = usrnm_var.get().strip()
        p = pass_var.get().strip()

        display_name = n if n else curr_name
        display_usrnm = u if u else curr_usrnm
        display_pass = "•" * len(p) if p else "•••••••• (Unchanged)"

        preview_name.configure(text=f"Name: {display_name}", text_color=COLORS["success"] if n else COLORS["text_main"])
        preview_usrnm.configure(text=f"Username: {display_usrnm}", text_color=COLORS["success"] if u else COLORS["text_main"])
        preview_pass.configure(text=f"Password: {display_pass}", text_color=COLORS["success"] if p else COLORS["text_main"])

    name_var.trace_add("write", update_preview)
    usrnm_var.trace_add("write", update_preview)
    pass_var.trace_add("write", update_preview)

def draw_transfer_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Transfer Funds")

    Header = ctk.CTkLabel(main_window, text="Transfer Funds", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(20, 5))

    Sub_Header = ctk.CTkLabel(main_window, text="Instantly move funds between customer accounts.", font=("Helvetica", 16), text_color=COLORS["text_muted"])
    Sub_Header.pack(pady=(0, 15))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(padx=60, pady=(5, 35), fill="both", expand=True)

    Card_Frame.grid_columnconfigure(0, weight=1)
    Card_Frame.grid_columnconfigure(1, weight=1)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.grid(row=0, column=0, padx=(40, 20), pady=30, sticky="nwe")

    sender_var = ctk.StringVar()
    receiver_var = ctk.StringVar()
    amt_var = ctk.StringVar()

    sender_label = ctk.CTkLabel(Form_Frame, text="Sender Account Number", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    sender_label.pack(anchor="w", pady=(0, 5))
    sender_entry = ctk.CTkEntry(Form_Frame, textvariable=sender_var, placeholder_text="Account sending money...", font=("Helvetica", 16), height=45, corner_radius=8, border_color=COLORS["border"])
    sender_entry.pack(fill="x", pady=(0, 15))

    receiver_label = ctk.CTkLabel(Form_Frame, text="Receiver Account Number", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    receiver_label.pack(anchor="w", pady=(0, 5))
    receiver_entry = ctk.CTkEntry(Form_Frame, textvariable=receiver_var, placeholder_text="Account receiving money...", font=("Helvetica", 16), height=45, corner_radius=8, border_color=COLORS["border"])
    receiver_entry.pack(fill="x", pady=(0, 15))

    transfer_amt_label = ctk.CTkLabel(Form_Frame, text="Amount To Transfer (₹)", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    transfer_amt_label.pack(anchor="w", pady=(0, 5))
    transfer_amt_entry = ctk.CTkEntry(Form_Frame, textvariable=amt_var, placeholder_text="Amount (₹)", font=("Helvetica", 16), height=45, corner_radius=8, border_color=COLORS["border"])
    transfer_amt_entry.pack(fill="x", pady=(0, 30))

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
            # Check Sender
            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (sender_acc,))
            sender = cursor.fetchone()
            if sender is None:
                messagebox.showerror("Error", "Sender account not found!")
                return
            sender_balance = float(sender[0])
            if sender_balance < amt:
                messagebox.showerror("Declined", f"Insufficient funds. Sender only has ₹{sender_balance:,.2f}")
                return

            # Check Receiver
            cursor.execute("SELECT Acc_Balance FROM Accounts WHERE Acc_No = %s", (reciever_acc,))
            reciever = cursor.fetchone()
            if reciever is None:
                messagebox.showerror("Error", "Receiver account not found!")
                return
            reciever_balance = float(reciever[0])

            # Execute Transfer
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

    trnsf_btn = ctk.CTkButton(Form_Frame, text="Complete Transfer", font=("Helvetica", 18, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, corner_radius=8, command=attempt_transfer)
    trnsf_btn.pack(fill="x", pady=(0, 15))

    back_btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    back_btn.pack(fill="x")

    Vis_Frame = ctk.CTkFrame(Card_Frame, fg_color=COLORS["secondary"], corner_radius=15)
    Vis_Frame.grid(row=0, column=1, padx=(20, 40), pady=30, sticky="nwe")

    Vis_Title = ctk.CTkLabel(Vis_Frame, text="Live Routing Preview", font=("Helvetica", 20, "bold"), text_color=COLORS["primary"])
    Vis_Title.pack(pady=(25, 20))

    Diagram_Frame = ctk.CTkFrame(Vis_Frame, fg_color="transparent")
    Diagram_Frame.pack(fill="x", padx=15, pady=(0, 25))

    Diagram_Frame.grid_columnconfigure(0, weight=3) # Sender Box
    Diagram_Frame.grid_columnconfigure(1, weight=1) # Arrow
    Diagram_Frame.grid_columnconfigure(2, weight=3) # Receiver Box

    Sender_Box = ctk.CTkFrame(Diagram_Frame, fg_color="white", corner_radius=10)
    Sender_Box.grid(row=0, column=0, sticky="nsew", padx=5)
    ctk.CTkLabel(Sender_Box, text="SENDER", font=("Helvetica", 12, "bold"), text_color=COLORS["text_muted"]).pack(pady=(15, 0))
    live_s_name = ctk.CTkLabel(Sender_Box, text="Waiting...", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"], wraplength=120)
    live_s_name.pack(pady=(5, 0), expand=True)
    live_s_acc = ctk.CTkLabel(Sender_Box, text="---", font=("Courier", 12), text_color=COLORS["text_muted"])
    live_s_acc.pack(pady=(0, 15))

    Arrow_Box = ctk.CTkFrame(Diagram_Frame, fg_color="transparent")
    Arrow_Box.grid(row=0, column=1, sticky="nsew")
    live_amt = ctk.CTkLabel(Arrow_Box, text="₹0.00", font=("Helvetica", 18, "bold"), text_color=COLORS["success"])
    live_amt.pack(side="top", pady=(20, 0))
    ctk.CTkLabel(Arrow_Box, text="━━━━➔", font=("Helvetica", 24, "bold"), text_color=COLORS["text_muted"]).pack(side="top")

    Receiver_Box = ctk.CTkFrame(Diagram_Frame, fg_color="white", corner_radius=10)
    Receiver_Box.grid(row=0, column=2, sticky="nsew", padx=5)
    ctk.CTkLabel(Receiver_Box, text="RECEIVER", font=("Helvetica", 12, "bold"), text_color=COLORS["text_muted"]).pack(pady=(15, 0))
    live_r_name = ctk.CTkLabel(Receiver_Box, text="Waiting...", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"], wraplength=120)
    live_r_name.pack(pady=(5, 0), expand=True)
    live_r_acc = ctk.CTkLabel(Receiver_Box, text="---", font=("Courier", 12), text_color=COLORS["text_muted"])
    live_r_acc.pack(pady=(0, 15))

    def update_visuals(*args):
        amt_val = amt_var.get().strip()
        if amt_val:
            try:
                formatted_amt = f"₹{float(amt_val):,.2f}"
                live_amt.configure(text=formatted_amt)
            except ValueError:
                live_amt.configure(text="Invalid")
        else:
            live_amt.configure(text="₹0.00")

        s_val = sender_var.get().strip()
        if s_val:
            try:
                cursor.execute("SELECT Acc_Name FROM Accounts WHERE Acc_No = %s", (s_val,))
                res = cursor.fetchone()
                live_s_name.configure(text=res[0] if res else "Not Found", text_color=COLORS["text_main"] if res else COLORS["danger"])
                live_s_acc.configure(text=s_val)
            except sql.Error:
                pass
        else:
            live_s_name.configure(text="Waiting...", text_color=COLORS["text_main"])
            live_s_acc.configure(text="---")

        r_val = receiver_var.get().strip()
        if r_val:
            try:
                cursor.execute("SELECT Acc_Name FROM Accounts WHERE Acc_No = %s", (r_val,))
                res = cursor.fetchone()
                live_r_name.configure(text=res[0] if res else "Not Found", text_color=COLORS["text_main"] if res else COLORS["danger"])
                live_r_acc.configure(text=r_val)
            except sql.Error:
                pass
        else:
            live_r_name.configure(text="Waiting...", text_color=COLORS["text_main"])
            live_r_acc.configure(text="---")

    sender_var.trace_add("write", update_visuals)
    receiver_var.trace_add("write", update_visuals)
    amt_var.trace_add("write", update_visuals)

    sender_label = ctk.CTkLabel(Card_Frame, text="Sender Account Number", font=("Helvetica", 11, "bold"), text_color="#555555")
    sender_label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    sender_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Sender Account Number", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    sender_entry.pack(pady=(15, 15))

    receiver_label = ctk.CTkLabel(Card_Frame, text="Receiver Account Number", font=("Helvetica", 11, "bold"), text_color="#555555")
    receiver_label.pack(anchor="center", pady=(10, 2), padx=(0, 135))
    receiver_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Receiver Account Number", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    receiver_entry.pack(pady=(0, 15))

    transfer_amt_label = ctk.CTkLabel(Card_Frame, text="Amount To Transfer (₹)", font=("Helvetica", 11, "bold"), text_color="#555555")
    transfer_amt_label.pack(anchor="center", pady=(10, 2), padx=(0, 150))
    transfer_amt_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Amount To Transfer (₹)", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    transfer_amt_entry.pack(pady=(0, 30))

    def attempt_transfer_fund():

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

    trnsf_btn = ctk.CTkButton(Card_Frame, text="Complete Transfer", font=("Helvetica", 15, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=40, width=300, corner_radius=8, command=attempt_transfer_fund)
    trnsf_btn.pack(pady=(0, 15))

    back_btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 14), fg_color=COLORS["secondary"], text_color=COLORS["text_main"], hover_color=COLORS["secondary_hover"], height=40, width=300, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    back_btn.pack()

def draw_statement_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Get Account Statement")

    Header = ctk.CTkLabel(main_window, text="Account Statement", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, ipadx=50, ipady=40)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    acc_no_label = ctk.CTkLabel(Form_Frame, text="Customer Account Number", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    acc_no_label.pack(anchor="w", pady=(0, 5))
    acc_no_entry = ctk.CTkEntry(Form_Frame, placeholder_text="Customer Account Number", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    acc_no_entry.pack(pady=(0, 30))

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

            Header_Frame = ctk.CTkFrame(main_window, fg_color="transparent")
            Header_Frame.pack(fill="x", padx=40, pady=(30, 10))

            St_Header = ctk.CTkLabel(Header_Frame, text=f"Statement for {acc_info[0]}", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
            St_Header.pack(anchor="w")

            Bal_Header = ctk.CTkLabel(Header_Frame, text=f"Account: {acc_no}   |   Current Balance: ₹{float(acc_info[1]):,.2f}", font=("Helvetica", 18), text_color=COLORS["text_muted"])
            Bal_Header.pack(anchor="w", pady=(0, 10))

            # Using a Text widget to cleanly display fixed-width data
            txt = ctk.CTkTextbox(main_window, font=("Courier", 16, "bold"), width=760, height=320, corner_radius=10, fg_color="white", text_color=COLORS["text_main"], border_width=2, border_color=COLORS["border"])
            txt.pack(padx=40, pady=(10, 20))

            txt.tag_config("credit", foreground=COLORS["success"])
            txt.tag_config("debit", foreground=COLORS["danger"])

            txt.insert("end", f"{'Date & Time':<18} | {'Transaction ID':<30} | {'Amount (₹)':>15}\n")
            txt.insert("end", "-"*69 + "\n")

            if not transactions:
                txt.insert("end", "No transactions found for this account.\n")
            else:
                for t in transactions:
                    t_id, t_send, t_recv, t_amt, t_time = t
                    t_date_str = t_time.strftime("%Y-%m-%d %H:%M:%S")

                    base_info = f"{t_date_str:<18}| {t_id:<30} |"
                                    
                    if t_send == acc_no:
                        amt_str = f"-{float(t_amt):,.2f}\n"
                        txt.insert("end", base_info)
                        txt.insert("end", f"{amt_str:>15}", "debit")
                    else:
                        amt_str = f"+{float(t_amt):,.2f}\n"
                        txt.insert("end", base_info)
                        txt.insert("end", f"{amt_str:>15}", "credit")

            txt.insert("end", "\n\n" +"-"*22 + "* End Of Transactions *" + "-"*24 + "\n")
            txt.configure(state="disabled") # Make text read-only

            Back_Btn_Output = ctk.CTkButton(main_window, text="Back To Dashboard", font=("Helvetica", 18, "bold"), fg_color=COLORS["secondary"], text_color=COLORS["text_main"], hover_color=COLORS["secondary_hover"], height=50, width=250, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
            Back_Btn_Output.pack(pady=(0, 15))

        except sql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch statement: {err}")

    Search_Btn = ctk.CTkButton(Form_Frame, text="Get Statement", font=("Helvetica", 18, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=fetch_statement)
    Search_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Form_Frame, text="Back to Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.pack()

def draw_close_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Close Customer Account")

    Header = ctk.CTkLabel(main_window, text="Close Customer Account", font=("Helvetica", 36, "bold"), text_color=COLORS["danger"])
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=50, ipady=40)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    acc_no_label = ctk.CTkLabel(Form_Frame, text="Enter Customer Account Number", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    acc_no_label.pack(anchor="w", pady=(0, 5))
    acc_no_entry = ctk.CTkEntry(Form_Frame, placeholder_text="Account Number To Close", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    acc_no_entry.pack(pady=(0, 30))

    def attempt_close():
        acc_no = acc_no_entry.get().strip()
        
        if not acc_no:
            messagebox.showwarning("Input Error", "Please enter an account number.")
            return

        try:
            cursor.execute("SELECT Acc_No FROM Accounts WHERE Acc_No = %s", (acc_no,))
            result = cursor.fetchone()

            if result is not None:
                confirm = messagebox.askyesno("Confirm Closure", f"Are you sure you want to CLOSE account: {acc_no}? \n\nThis will remove the account from the system and all the transactions and other details associated with it. \n\n!!! THIS ACTION CANNOT BE UNDONE !!!")
                if confirm:
                    cursor.execute("DELETE FROM Accounts WHERE Acc_No = %s", (acc_no,))
                    cursor.execute("DELETE FROM Account_Credentials WHERE Acc_No = %s", (acc_no,))
                    cursor.execute("DELETE FROM Transactions WHERE Sender = %s AND Reciever = %s", (acc_no, "SELF_WITHDRAW"))  # Assuming you want to delete self-withdrawal transactions as well
                    cursor.execute("DELETE FROM Transactions WHERE Sender = %s AND Reciever = %s", ("SELF_DEPOSIT", acc_no))
                    db.commit()
                    messagebox.showinfo("Account Closed", f"Account {acc_no} has been closed successfully.")
                    draw_employee_dashboard(emp_id, emp_name)
            else:
                messagebox.showerror("Not Found", "Invalid Account Number. Please try again.")
        except sql.Error as err:
            print(f"Database Error: {err}")

    Close_Btn = ctk.CTkButton(Form_Frame, text="Close Account", font=("Helvetica", 18, "bold"), fg_color=COLORS["danger"], hover_color="#C82333", height=45, width=320, corner_radius=8, command=attempt_close)
    Close_Btn.pack(pady=(0, 15))

    Back_btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_btn.pack()

def draw_transaction_details_screen(emp_id, emp_name, trnsc_id, sender, sender_name, receiver, receiver_name, amount, timestamp_str):
    clear_window()
    main_window.title(f"Bank Management - Transaction: {trnsc_id}")

    Header = ctk.CTkLabel(main_window, text="Transaction Receipt", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(40, 15))

    Receipt_Card = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Receipt_Card.pack(ipadx=30, ipady=30, fill="x", padx=80)

    Amount_Label = ctk.CTkLabel(Receipt_Card, text=f"₹{float(amount):,.2f}", font=("Helvetica", 52, "bold"), text_color=COLORS["success"])
    Amount_Label.pack(pady=(10, 0))

    Date_Label = ctk.CTkLabel(Receipt_Card, text=timestamp_str, font=("Helvetica", 18), text_color=COLORS["text_muted"])
    Date_Label.pack(pady=(5, 20))

    Divider = ctk.CTkFrame(Receipt_Card, height=1, fg_color=COLORS["border"])
    Divider.pack(fill="x", padx=30, pady=10)

    Details_Frame = ctk.CTkFrame(Receipt_Card, fg_color="transparent")
    Details_Frame.pack(fill="x", padx=40, pady=15)
    Details_Frame.grid_columnconfigure(0, weight=1)
    Details_Frame.grid_columnconfigure(1, weight=1)

    S_Title = ctk.CTkLabel(Details_Frame, text="FROM (SENDER)", font=("Helvetica", 14, "bold"), text_color=COLORS["text_muted"])
    S_Title.grid(row=0, column=0, sticky="w", pady=(0, 2))
    S_Name = ctk.CTkLabel(Details_Frame, text=sender_name, font=("Helvetica", 22, "bold"), text_color=COLORS["text_main"])
    S_Name.grid(row=1, column=0, sticky="w")
    S_Acc = ctk.CTkLabel(Details_Frame, text=f"Acc: {sender}", font=("Helvetica", 18), text_color=COLORS["text_muted"])
    S_Acc.grid(row=2, column=0, sticky="w")

    R_Title = ctk.CTkLabel(Details_Frame, text="TO (RECEIVER)", font=("Helvetica", 14, "bold"), text_color=COLORS["text_muted"])
    R_Title.grid(row=0, column=1, sticky="e", pady=(0, 2))
    R_Name = ctk.CTkLabel(Details_Frame, text=receiver_name, font=("Helvetica", 22, "bold"), text_color=COLORS["text_main"])
    R_Name.grid(row=1, column=1, sticky="e")
    R_Acc = ctk.CTkLabel(Details_Frame, text=f"Acc: {receiver}", font=("Helvetica", 18), text_color=COLORS["text_muted"])
    R_Acc.grid(row=2, column=1, sticky="e")

    ID_Label = ctk.CTkLabel(Receipt_Card, text=f"TRANSACTION ID: {trnsc_id}", font=("Courier", 16, "bold"), text_color=COLORS["text_muted"])
    ID_Label.pack(pady=(25, 0))

    Action_Frame = ctk.CTkFrame(main_window, fg_color="transparent")
    Action_Frame.pack(pady=25)

    Search_Again_Btn = ctk.CTkButton(Action_Frame, text="Search Another", font=("Helvetica", 16, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=220, corner_radius=8, command=lambda: draw_transaction_details(emp_id, emp_name))
    Search_Again_Btn.grid(row=0, column=0, padx=15)

    Back_Btn = ctk.CTkButton(Action_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color=COLORS["dark_btn"], border_width=2, border_color=COLORS["border"], hover_color=COLORS["dark_hover"], height=45, width=220, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.grid(row=0, column=1, padx=15)

def draw_transaction_details(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Search Transaction")

    Header = ctk.CTkLabel(main_window, text="Lookup Transaction", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=50, ipady=40)

    Form_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Form_Frame.pack(pady=10)

    trnsc_id_label = ctk.CTkLabel(Form_Frame, text="Transaction Reference ID", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    trnsc_id_label.pack(anchor="w", pady=(0, 5))
    trnsc_id_entry = ctk.CTkEntry(Form_Frame, placeholder_text="e.g., aB3x20260814...", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    trnsc_id_entry.pack(pady=(0, 30))

    def fetch_transaction():
        trnsc_id = trnsc_id_entry.get().strip()

        if not trnsc_id:
            messagebox.showwarning("Input Error", "Please Enter A Valid Transaction ID.")
            return

        try:
            cursor.execute("SELECT Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time FROM Transactions WHERE Trnsc_ID = %s", (trnsc_id,))
            transaction = cursor.fetchone()

            if transaction is None:
                messagebox.showerror("Not Found", "Transaction ID not found.")
                return

            trnsc_id, sender, receiver, amount, timestamp = transaction
            timestamp_str = timestamp.strftime("%b %d, %Y  •  %H:%M:%S")
            system_accounts = ["BANK", "SELF", "SELF_WITHDRAW", "SELF_DEPOSIT"]

            if sender in system_accounts:
                sender_name = "System / Self"
            else:
                cursor.execute("SELECT Acc_Name FROM Accounts WHERE Acc_No = %s", (transaction[1],))
                sender_n = cursor.fetchone()
                sender_name = sender_n[0] if sender_n else "No-Sender-Name"

            if receiver in system_accounts:
                receiver_name = "System / Self"
            else:
                cursor.execute("SELECT Acc_Name FROM Accounts WHERE Acc_No = %s", (transaction[2],))
                receiver_n = cursor.fetchone()
                receiver_name = receiver_n[0] if receiver_n else "No-Reciever-Name"

            # Display transaction details
            draw_transaction_details_screen(emp_id, emp_name, trnsc_id, sender, sender_name, receiver, receiver_name, amount, timestamp_str)

        except sql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch transaction details: {err}")

    Search_Btn = ctk.CTkButton(Form_Frame, text="Lookup Details", font=("Helvetica", 18, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=fetch_transaction)
    Search_Btn.pack(pady=(0, 15))

    Back_btn = ctk.CTkButton(Form_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_btn.pack()

def draw_cus_transaction_details(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title("Bank Management - Search Transaction")

    Header = ctk.CTkLabel(main_window, text="Lookup Transaction", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(60, 60))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    trnsc_id_label = ctk.CTkLabel(Card_Frame, text="Transaction ID", font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
    trnsc_id_label.pack(anchor="w", padx=(30, 0), pady=(10, 5))
    
    trnsc_id_entry = ctk.CTkEntry(Card_Frame, placeholder_text="e.g., aB3x20260814...", font=("Helvetica", 16), width=320, height=45, corner_radius=8, border_color=COLORS["border"])
    trnsc_id_entry.pack(pady=(0, 30))

    def fetch_transaction():
        trnsc_id = trnsc_id_entry.get().strip()

        if not trnsc_id:
            messagebox.showwarning("Input Error", "Please Enter A Valid Transaction ID.")
            return

        try:
            cursor.execute("SELECT Trnsc_ID, Sender, Reciever, Trns_Amt, Trns_Time FROM Transactions WHERE Trnsc_ID = %s", (trnsc_id,))
            transaction = cursor.fetchone()

            if transaction is None:
                messagebox.showerror("Not Found", "Transaction ID not found in the system.")
                return

            trnsc_id, sender, receiver, amount, timestamp = transaction

            if sender != acc_no and receiver != acc_no:
                messagebox.showerror("Access Denied", "You are only authorized to view your own transactions.")
                return

            timestamp_str = timestamp.strftime("%b %d, %Y  •  %H:%M:%S")

            system_accounts = ["BANK", "SELF", "SELF_WITHDRAW", "SELF_DEPOSIT"]
            
            if sender in system_accounts:
                sender_name = "System / Self"
            else:
                cursor.execute("SELECT Acc_Name FROM Accounts WHERE Acc_No = %s", (sender,))
                sender_n = cursor.fetchone()
                sender_name = sender_n[0] if sender_n else "Unknown Account"

            if receiver in system_accounts:
                receiver_name = "System / Self"
            else:
                cursor.execute("SELECT Acc_Name FROM Accounts WHERE Acc_No = %s", (receiver,))
                receiver_n = cursor.fetchone()
                receiver_name = receiver_n[0] if receiver_n else "Unknown Account"

            draw_cus_transaction_details_screen(acc_name, acc_balance, acc_no, trnsc_id, sender, sender_name, receiver, receiver_name, amount, timestamp_str)

        except sql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch transaction details: {err}")

    Search_Btn = ctk.CTkButton(Card_Frame, text="Lookup Details", font=("Helvetica", 18, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=320, corner_radius=8, command=fetch_transaction)
    Search_Btn.pack(pady=(0, 15))

    Back_btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color="transparent", border_width=2, border_color=COLORS["border"], text_color=COLORS["text_muted"], hover_color=COLORS["secondary_hover"], height=45, width=320, corner_radius=8, command=lambda: draw_dashboard(acc_name, acc_balance, acc_no))
    Back_btn.pack()

def draw_cus_transaction_details_screen(acc_name, acc_balance, acc_no, trnsc_id, sender, sender_name, receiver, receiver_name, amount, timestamp_str):
    clear_window()
    main_window.title(f"Bank Management - Transaction: {trnsc_id}")

    Header = ctk.CTkLabel(main_window, text="Transaction Details", font=("Helvetica", 32, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(40, 15))

    Receipt_Card = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Receipt_Card.pack(ipadx=30, ipady=30, fill="x", padx=80)

    amt_color = COLORS["danger"] if sender == acc_no else COLORS["success"]
    prefix = "-" if sender == acc_no else "+"
    
    Amount_Label = ctk.CTkLabel(Receipt_Card, text=f"{prefix}₹{float(amount):,.2f}", font=("Helvetica", 52, "bold"), text_color=amt_color)
    Amount_Label.pack(pady=(10, 0))

    Date_Label = ctk.CTkLabel(Receipt_Card, text=timestamp_str, font=("Helvetica", 18), text_color=COLORS["text_muted"])
    Date_Label.pack(pady=(5, 20))

    Divider = ctk.CTkFrame(Receipt_Card, height=1, fg_color=COLORS["border"])
    Divider.pack(fill="x", padx=30, pady=10)

    Details_Frame = ctk.CTkFrame(Receipt_Card, fg_color="transparent")
    Details_Frame.pack(fill="x", padx=40, pady=15)
    Details_Frame.grid_columnconfigure(0, weight=1)
    Details_Frame.grid_columnconfigure(1, weight=1)

    S_Title = ctk.CTkLabel(Details_Frame, text="FROM (SENDER)", font=("Helvetica", 14, "bold"), text_color=COLORS["text_muted"])
    S_Title.grid(row=0, column=0, sticky="w", pady=(0, 2))
    S_Name = ctk.CTkLabel(Details_Frame, text=sender_name, font=("Helvetica", 22, "bold"), text_color=COLORS["text_main"])
    S_Name.grid(row=1, column=0, sticky="w")
    S_Acc = ctk.CTkLabel(Details_Frame, text=f"Acc: {sender}", font=("Helvetica", 18), text_color=COLORS["text_muted"])
    S_Acc.grid(row=2, column=0, sticky="w")

    R_Title = ctk.CTkLabel(Details_Frame, text="TO (RECEIVER)", font=("Helvetica", 14, "bold"), text_color=COLORS["text_muted"])
    R_Title.grid(row=0, column=1, sticky="e", pady=(0, 2))
    R_Name = ctk.CTkLabel(Details_Frame, text=receiver_name, font=("Helvetica", 22, "bold"), text_color=COLORS["text_main"])
    R_Name.grid(row=1, column=1, sticky="e")
    R_Acc = ctk.CTkLabel(Details_Frame, text=f"Acc: {receiver}", font=("Helvetica", 18), text_color=COLORS["text_muted"])
    R_Acc.grid(row=2, column=1, sticky="e")

    ID_Label = ctk.CTkLabel(Receipt_Card, text=f"TRANSACTION ID: {trnsc_id}", font=("Courier", 16, "bold"), text_color=COLORS["text_muted"])
    ID_Label.pack(pady=(25, 0))

    Action_Frame = ctk.CTkFrame(main_window, fg_color="transparent")
    Action_Frame.pack(pady=25)

    Search_Again_Btn = ctk.CTkButton(Action_Frame, text="Search Another", font=("Helvetica", 16, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], height=45, width=200, corner_radius=8, command=lambda: draw_cus_transaction_details(acc_name, acc_balance, acc_no))
    Search_Again_Btn.grid(row=0, column=0, padx=15)

    Back_Btn = ctk.CTkButton(Action_Frame, text="Back To Dashboard", font=("Helvetica", 16, "bold"), fg_color=COLORS["dark_btn"], hover_color=COLORS["dark_hover"], height=45, width=200, corner_radius=8, command=lambda: draw_dashboard(acc_name, acc_balance, acc_no))
    Back_Btn.grid(row=0, column=1, padx=15)

def draw_employee_dashboard(Emp_ID, Emp_Name):
    clear_window()
    main_window.title(f"Bank Management - Employee Dashboard ({Emp_ID})")

    Header = ctk.CTkLabel(main_window, text="Employee Dashboard", font=("Helvetica", 32, "bold"), text_color=COLORS["primary"])
    Header.pack(pady=(15, 5))

    SubHeader = ctk.CTkLabel(main_window, text=f"Logged in: {Emp_Name}", font=("Helvetica", 20), text_color=COLORS["text_muted"])
    SubHeader.pack(pady=(0, 10))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(padx=80, pady=10, fill="x")

    Action_Title = ctk.CTkLabel(Card_Frame, text="Administrative Actions", font=("Helvetica", 22, "bold"), text_color=COLORS["text_main"])
    Action_Title.pack(anchor="w", pady=(15, 10), padx=30)

    def create_action_row(parent, text, button_text, command, custom_pady=(3, 3)):
        row = ctk.CTkFrame(parent, fg_color="transparent", border_width=2, border_color=COLORS["border"], corner_radius=10)
        row.pack(fill="x", pady=custom_pady, padx=30)
        lbl = ctk.CTkLabel(row, text=text, font=("Helvetica", 16, "bold"), text_color=COLORS["text_main"])
        lbl.pack(side="left", padx=20, pady=7)
        btn = ctk.CTkButton(row, text=button_text, font=("Helvetica", 15, "bold"), fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"], width=140, height=35, corner_radius=8, command=command)
        btn.pack(side="right", padx=20, pady=7)

    create_action_row(Card_Frame, "Create New Customer Account", "Create", lambda: draw_create_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Edit Existing Customer Details", "Edit", lambda: draw_edit_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Transfer Money Between Accounts", "Transfer", lambda: draw_transfer_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Generate Account Statement", "Get Statement", lambda: draw_statement_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Close Customer Account", "Close", lambda: draw_close_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Get Transaction Details", "Get Details", lambda: draw_transaction_details(Emp_ID, Emp_Name), custom_pady=(3, 20))

    Logout_Btn = ctk.CTkButton(main_window, text="Log Out", font=("Helvetica", 16, "bold"), fg_color=COLORS["danger"], hover_color="#C82333", height=45, width=200, corner_radius=8, command=draw_homepage)
    Logout_Btn.pack(pady=10)

def draw_mini_statement(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title(f"Bank Management - Mini Statement for Account: {acc_no}")

    Header_Frame = ctk.CTkFrame(main_window, fg_color="transparent")
    Header_Frame.pack(fill="x", padx=40, pady=(30, 10))

    Header = ctk.CTkLabel(Header_Frame, text="Recent Transactions", font=("Helvetica", 36, "bold"), text_color=COLORS["primary"])
    Header.pack(anchor="w")

    Sub_Header = ctk.CTkLabel(Header_Frame, text=f"Account: {acc_no}   |   Available Balance: ₹{float(acc_balance):,.2f}", font=("Helvetica", 18), text_color=COLORS["text_muted"])
    Sub_Header.pack(anchor="w", pady=(0, 10))

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

        txt = ctk.CTkTextbox(main_window, font=("Courier", 16, "bold"), width=760, height=320, corner_radius=10, fg_color="white", text_color=COLORS["text_main"], border_width=2, border_color=COLORS["border"])
        txt.pack(padx=40, pady=(10, 20))

        txt.tag_config("credit", foreground=COLORS["success"])
        txt.tag_config("debit", foreground=COLORS["danger"])

        txt.insert("end", f"{'Date & Time':<18} | {'Reference ID':<30} | {'Amount (₹)':>15}\n")
        txt.insert("end", "-"*69 + "\n")

        if not transactions:
            txt.insert("end", "No recent transactions found for this account.\n")

        else:
            for t in transactions:
                t_id, t_send, t_recv, t_amt, t_time = t
                t_date_str = t_time.strftime("%Y-%m-%d %H:%M:%S")

                base_info = f"{t_date_str:<18}| {t_id:<30} |"
                
                if t_send == acc_no:
                    amt_str = f"-{float(t_amt):,.2f}\n"
                    txt.insert("end", base_info)
                    txt.insert("end", f"{amt_str:>15}", "debit")
                else:
                    amt_str = f"+{float(t_amt):,.2f}\n"
                    txt.insert("end", base_info)
                    txt.insert("end", f"{amt_str:>15}", "credit")

        txt.insert("end", "\n\n" +"-"*17 + "* Contact Bank For Older Records *" + "-"*18 + "\n")
        txt.configure(state="disabled") # Make text read-only

        Back_Btn = ctk.CTkButton(main_window, text="Back To Dashboard", font=("Helvetica", 18, "bold"), fg_color=COLORS["secondary"], text_color=COLORS["text_main"], hover_color=COLORS["secondary_hover"], height=50, width=250, corner_radius=8, command=lambda: draw_dashboard(acc_name, acc_balance, acc_no))
        Back_Btn.pack(pady=(0, 15))

    except sql.Error as err:
        messagebox.showerror("Database Error", f"Failed to fetch mini statement: {err}")
        draw_dashboard(acc_name, acc_balance, acc_no)

main_window = ctk.CTk() #The main program window
main_window.title("Bank Management")
main_window.resizable(False,False)
main_window.geometry("800x600+550+200") #To set the window size to 800 by 600 pixels and to pop it in the middle of the screen
main_window.configure(fg_color=COLORS["bg"]) #Setting the background colour

draw_homepage()

main_window.mainloop() #Running the main program to genrate the window