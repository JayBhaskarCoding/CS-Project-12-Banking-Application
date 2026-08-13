import customtkinter as ctk
import tkinter.messagebox as messagebox
import mysql.connector as sql
import random
import string
import datetime

ctk.set_appearance_mode("Light")  # Can be "Light", "Dark", or "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

"""class PlaceHolderEntry(ctk.CTkEntry):
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
        return content"""

db = sql.connect(host="localhost", user="root", password="1234", database="Bank_Mng")
cursor = db.cursor(buffered=True)

# ==========================================
# GLOBAL UI THEME SETTINGS
# ==========================================
COLORS = {
    "bg": "#F4F7F6",          # A very modern, soft grey-blue background
    "card_bg": "#FFFFFF",     # Pure white for the center cards
    "primary": "#0056B3",
    "primary_hover": "#004085",    # Professional Bank Blue
    "success": "#28A745",     # Modern Green (Deposit/Success)
    "danger": "#DC3545",      # Modern Red (Withdraw/Logout)
    "text_main": "#2C3E50",   # Dark Slate for main text (easier on eyes than pure black)
    "text_muted": "#7F8C8D",  # Subtle grey for descriptions/placeholders
    "border": "#E2E8F0",      # Clean grey for borders
    "dark_btn": "#4A5568",    # NEW: Employee button color
    "dark_hover": "#2D3748"   # NEW: Darker grey for hover
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

def bind_hover(widget, hover_bg, default_bg):
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
    widget.bind("<Leave>", lambda e: widget.config(bg=default_bg))

def draw_homepage():
    clear_window()
    main_window.title("Bank Management")

    Header = ctk.CTkLabel(main_window, text="Welcome to Bank Management", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(60, 40))

    #Border_Frame = ctk.CTkFrame(main_window, bg=COLORS["border"], padx=1, pady=1)
    #Border_Frame.pack(pady=10, padx=60, fill="x") # fill="x" gives it a nice wide stance

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, padx=60, fill="both", expand=True)

    Customer_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Customer_Frame.pack(side="left", expand=True, fill="both", padx=20, pady=40)

    Cus_Title = ctk.CTkLabel(Customer_Frame, text="For Customers", font=("Helvetica", 20, "bold"), text_color="#333333")
    Cus_Title.pack(pady=(0, 10))

    Cus_Desc = ctk.CTkLabel(Customer_Frame, text="Access your personal accounts,\ntransfer funds, and view balances.", font=("Helvetica", 14), text_color="#777777", justify="center")
    Cus_Desc.pack(pady=(0, 30))

    Cus_Btn = ctk.CTkButton(Customer_Frame, text="Customer Portal", font=("Helvetica", 14, "bold"), corner_radius=8, height=40, command=draw_login_screen)
    Cus_Btn.pack()
    bind_hover(Cus_Btn, COLORS["primary_hover"], COLORS["primary"]) # Add Hover Animation!

    Divider = ctk.CTkFrame(Card_Frame, width=2, fg_color="#E0E0E0")
    Divider.pack(side="left", fill="y", pady=40)

    Employee_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Employee_Frame.pack(side="right", expand=True, fill="both", padx=20, pady=40)

    Emp_Title = ctk.CTkLabel(Employee_Frame, text="For Employees", font=("Helvetica", 20, "bold"), text_color="#333333")
    Emp_Title.pack(pady=(0, 10))

    Emp_Desc = ctk.CTkLabel(Employee_Frame, text="Manage user accounts, verify\ntransactions, and assist customers.", font=("Helvetica", 14), text_color="#777777", justify="center")
    Emp_Desc.pack(pady=(0, 30))

    Emp_Btn = ctk.CTkButton(Employee_Frame, text="Employee Portal", font=("Helvetica", 14, "bold"), corner_radius=8, height=40, fg_color="#4A5568", hover_color="#2D3748", command=draw_emp_login_screen)
    Emp_Btn.pack()
    bind_hover(Emp_Btn, COLORS["dark_hover"], COLORS["dark_btn"])

def draw_login_screen():
    clear_window()
    main_window.title("Bank Management - Login")

    Header = ctk.CTkLabel(main_window, text="Customer Login", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    Username_Label = ctk.CTkLabel(Card_Frame, text="Username", font=("Helvetica", 14, "bold"), text_color="#555555")
    Username_Label.pack(anchor="w", padx=(30, 0), pady=(20, 5))
    Username_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Enter Your Username", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC")
    Username_Input.pack(pady=(0, 15))

    Password_Label = ctk.CTkLabel(Card_Frame, text="Password", font=("Helvetica", 14, "bold"), text_color="#555555")
    Password_Label.pack(anchor="w", padx=(30, 0), pady=(10, 5))
    Password_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Enter Your Password", show="*", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC")
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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(30,0))

    Login_Btn = ctk.CTkButton(Card_Frame, text="Login", font=("Helvetica", 15, "bold"), fg_color="#28A745", hover_color="#218838", height=40, width=300, corner_radius=8, command=attempt_login)
    Login_Btn.pack(pady=(0, 15))

    Back_Homepage = ctk.CTkButton(Card_Frame, text="Back To Homepage", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=draw_homepage)
    Back_Homepage.pack()

def draw_create_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Create Account")

    Header = ctk.CTkLabel(main_window, text="Create Customer Account", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    Acc_Name_Label = ctk.CTkLabel(Card_Frame, text="Enter Your Full Name", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Acc_Name_Label.pack(anchor="center", pady=(30, 2), padx=(0,170))
    Acc_Name_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Customer Full Name", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    Acc_Name_Input.pack(pady=(20, 15))

    Username_Label = ctk.CTkLabel(Card_Frame, text="Choose A Username", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Username_Label.pack(anchor="center", pady=(20, 2), padx=(0,180))
    Username_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Choose A Username", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    Username_Input.pack(pady=(0, 15))

    Password_Label = ctk.CTkLabel(Card_Frame, text="Create A Strong Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Password_Label.pack(anchor="center", pady=(20, 2), padx=(0,135))
    Password_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Create Password", show="*", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    Password_Input.pack(pady=(0, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(20,0))

    Create_Btn = ctk.CTkButton(Card_Frame, text="Create Account", font=("Helvetica", 15, "bold"), fg_color="#007BFF", hover_color="#0056B3", height=40, width=300, corner_radius=8, command=attempt_create)
    Create_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.pack()

def draw_withdraw_screen(acc_no):
    clear_window()
    main_window.title("Bank Management - Withdraw Funds")

    Header = ctk.CTkLabel(main_window, text="Withdraw Funds", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, ipadx=40, ipady=30)

    Withdraw_Label = ctk.CTkLabel(Card_Frame, text="Enter Withdrawal Amount (₹)", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Withdraw_Label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    Withdraw_Entry = ctk.CTkEntry(Card_Frame, placeholder_text="Withdrawal Amount (₹)", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    Withdraw_Entry.pack(pady=(20, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(10, 0))

    Withdraw_Btn = ctk.CTkButton(Card_Frame, text="Complete Withdrawal", font=("Helvetica", 15, "bold"), fg_color="#DC3545", hover_color="#C82333", height=40, width=300, corner_radius=8, command=attempt_withdraw)
    Withdraw_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=go_back)
    Back_Btn.pack()

def draw_deposit_screen(acc_no):
    clear_window()
    main_window.title("Bank Management - Deposit Funds")

    Header = ctk.CTkLabel(main_window, text="Deposit Funds", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, ipadx=40, ipady=30)

    Deposit_Label = ctk.CTkLabel(Card_Frame, text="Enter Deposit Amount (₹)", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Deposit_Label.pack(anchor="center", pady=(10, 2), padx=(0, 155))
    
    Deposit_Entry = ctk.CTkEntry(Card_Frame, placeholder_text="Deposit Amount (₹)", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    Deposit_Entry.pack(pady=(20, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
   #Button_Frame.pack(pady=(10, 0))

    Deposit_Btn = ctk.CTkButton(Card_Frame, text="Complete Deposit", font=("Helvetica", 15, "bold"), fg_color="#28A745", hover_color="#218838", height=40, width=300, corner_radius=8, command=attempt_deposit)
    Deposit_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=go_back)
    Back_Btn.pack()

def draw_dashboard(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title(f"Bank Management - Dashboard For {acc_name}")

    Header = ctk.CTkLabel(main_window, text=f"Welcome Back, {acc_name}!", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 15))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(padx=80, pady=10, fill="x", ipady=20)

    Balance_Title = ctk.CTkLabel(Card_Frame, text="Available Balance", font=("Helvetica", 16, "bold"), text_color="#777777")
    Balance_Title.pack(pady=(20, 0))

    Formatted_Balance = f"₹{float(acc_balance):,.2f}" if acc_balance is not None else "₹0.00"
    Balance = ctk.CTkLabel(Card_Frame, text=Formatted_Balance, font=("Helvetica", 36, "bold"), text_color="#28A745")
    Balance.pack(pady=(5, 15))

    Separator = ctk.CTkFrame(Card_Frame, height=1, fg_color="#E0E0E0")
    Separator.pack(fill="x", padx=60, pady=15)

    Acc_no_lbl = ctk.CTkLabel(Card_Frame, text=f"Account Number: {acc_no}", font=("Helvetica", 14, "bold"), text_color="#333333")
    Acc_no_lbl.pack(pady=(0, 10))

    Action_Frame = ctk.CTkFrame(main_window, fg_color="transparent")
    Action_Frame.pack(pady=25)

    Deposit_Btn = ctk.CTkButton(Action_Frame, text="Deposit", font=("Helvetica", 14, "bold"), fg_color="#28A745", hover_color="#218838", height=45, width=130, corner_radius=8, command=lambda: draw_deposit_screen(acc_no))
    Deposit_Btn.grid(row=0, column=0, padx=15)

    Withdraw_Btn = ctk.CTkButton(Action_Frame, text="Withdraw", font=("Helvetica", 14, "bold"), fg_color="#DC3545", hover_color="#C82333", height=45, width=130, corner_radius=8, command=lambda: draw_withdraw_screen(acc_no))
    Withdraw_Btn.grid(row=0, column=1, padx=15)

    Mini_Stmt_Btn = ctk.CTkButton(Action_Frame, text="Mini Statement", font=("Helvetica", 14, "bold"), fg_color="#007BFF", hover_color="#0056B3", height=45, width=130, corner_radius=8, command=lambda: draw_mini_statement(acc_name, acc_balance, acc_no))
    Mini_Stmt_Btn.grid(row=0, column=2, padx=15)

    Logout_Btn = ctk.CTkButton(main_window, text="Log Out", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=150, corner_radius=8, command=draw_homepage)
    Logout_Btn.pack(pady=10)

def draw_emp_login_screen():
    clear_window()
    main_window.title("Bank Management - Employee Login")

    Header = ctk.CTkLabel(main_window, text="Employee Login", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    Username_Label = ctk.CTkLabel(Card_Frame, text="Employee ID", font=("Helvetica", 14, "bold"), text_color="#555555")
    Username_Label.pack(anchor="w", padx=(30, 0), pady=(20, 5))
    Username_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Enter Your 6-Digit ID", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC")
    Username_Input.pack(pady=(0, 15))

    Password_Label = ctk.CTkLabel(Card_Frame, text="Password", font=("Helvetica", 14, "bold"), text_color="#555555")
    Password_Label.pack(anchor="w", padx=(30, 0), pady=(10, 5))
    Password_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Enter Your Password", show="*", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC")
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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(30,0))

    Login_Btn = ctk.CTkButton(Card_Frame, text="Login", font=("Helvetica", 15, "bold"), fg_color="#28A745", hover_color="#218838", height=40, width=300, corner_radius=8, command=attempt_emp_login)
    Login_Btn.pack(pady=(0, 15))

    Split_Btn_Frame = ctk.CTkFrame(Card_Frame, fg_color="transparent")
    Split_Btn_Frame.pack(fill="x", padx=30)

    Acc_Create_selector = ctk.CTkButton(Split_Btn_Frame, text="Add Employee", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=145, corner_radius=8, command=draw_emp_create_screen)
    Acc_Create_selector.pack(side="left")

    Back_Homepage = ctk.CTkButton(Split_Btn_Frame, text="Back To Home", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=145, corner_radius=8, command=draw_homepage)
    Back_Homepage.pack(side="right")

def draw_emp_create_screen():
    clear_window()
    main_window.title("Bank Management - Add New Employee")

    Header = ctk.CTkLabel(main_window, text="New Employee Admission", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    Emp_Name_Label = ctk.CTkLabel(Card_Frame, text="Enter Your Full Name", font=("Helvetica", 11, "bold"), text_color="#555555")
    Emp_Name_Label.pack(anchor="center", pady=(30, 2), padx=(0,170))
    Emp_Name_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Enter Full Name", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC")
    Emp_Name_Input.pack(pady=(20, 15))

    Employer_Code_Label = ctk.CTkLabel(Card_Frame, text="Employer Code", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Employer_Code_Label.pack(anchor="center", pady=(20, 2), padx=(0,215))
    Employer_Code_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Employer Code", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC", show="*")
    Employer_Code_Input.pack(pady=(0, 15))

    Password_Label = ctk.CTkLabel(Card_Frame, text="Create A Strong Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    Password_Label.pack(anchor="center", pady=(20, 2), padx=(0,135))
    Password_Input = ctk.CTkEntry(Card_Frame, placeholder_text="Create Password", show="*", font=("Helvetica", 14), width=300, height=40, corner_radius=8, border_color="#CCCCCC")
    Password_Input.pack(pady=(0, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(20,0))

    Create_Btn = ctk.CTkButton(Card_Frame, text="Add Employee", font=("Helvetica", 15, "bold"), fg_color="#007BFF", hover_color="#0056B3", height=40, width=300, corner_radius=8, command=attempt_emp_create)
    Create_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Card_Frame, text="Back To Login", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=draw_emp_login_screen)
    Back_Btn.pack()

def draw_edit_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Edit Customer Details")

    Header = ctk.CTkLabel(main_window, text="Edit Customer Details", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(50, 30))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    acc_no_label = ctk.CTkLabel(Card_Frame, text="Enter Customer Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    acc_no_label.pack(pady=(10, 5))
    acc_no_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Enter Customer Account Number", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    acc_no_entry.pack(pady=(20, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(10, 0))

    Search_Btn = ctk.CTkButton(Card_Frame, text="Search Account", font=("Helvetica", 15, "bold"), fg_color="#007BFF", hover_color="#0056B3", height=40, width=300, corner_radius=8, command=fetch_account)
    Search_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.pack()

def draw_update_fields(acc_no, emp_id, emp_name):
    clear_window()
    main_window.title(f"Bank Management - Updating {acc_no}")

    Header = ctk.CTkLabel(main_window, text=f"Updating Account: {acc_no}", font=("Helvetica", 24, "bold"), text_color="#0056B3")
    Header.pack(pady=(30, 10))
    
    Info_Label = ctk.CTkLabel(main_window, text="Leave fields blank if you do not want to change them.", font=("Helvetica", 12, "italic"), text_color="#777777")
    Info_Label.pack(pady=(0, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    new_name_label = ctk.CTkLabel(Card_Frame, text="New Customer Name", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    new_name_label.pack(anchor="w", padx=(30, 0), pady=(0, 2))
    new_name_input = ctk.CTkEntry(Card_Frame, placeholder_text="New Customer Name", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    new_name_input.pack(pady=(10, 15))

    new_usrnm_label = ctk.CTkLabel(Card_Frame, text="New Username", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    new_usrnm_label.pack(anchor="w", padx=(30, 0), pady=(0, 2))
    new_usrnm_input = ctk.CTkEntry(Card_Frame, placeholder_text="New Username", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    new_usrnm_input.pack(pady=(0, 15))

    new_password_label = ctk.CTkLabel(Card_Frame, text="New Password", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    new_password_label.pack(anchor="w", padx=(30, 0), pady=(0, 2))
    new_password_input = ctk.CTkEntry(Card_Frame, placeholder_text="New Password", show="*", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    new_password_input.pack(pady=(0, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack()

    Update_Btn = ctk.CTkButton(Card_Frame, text="Save Details", font=("Helvetica", 15, "bold"), fg_color="#28A745", hover_color="#218838", height=40, width=300, corner_radius=8, command=attempt_update)
    Update_Btn.pack(pady=(0, 15))

    Cancel_Btn = ctk.CTkButton(Card_Frame, text="Cancel", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=lambda: draw_edit_screen(emp_id, emp_name))
    Cancel_Btn.pack()

def draw_transfer_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Transfer Funds")

    Header = ctk.CTkLabel(main_window, text="Transfer Funds", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(ipadx=40, ipady=30)

    sender_label = ctk.CTkLabel(Card_Frame, text="Sender Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    sender_label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    sender_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Sender Account Number", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    sender_entry.pack(pady=(15, 15))

    receiver_label = ctk.CTkLabel(Card_Frame, text="Receiver Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    receiver_label.pack(anchor="center", pady=(10, 2), padx=(0, 135))
    receiver_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Receiver Account Number", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    receiver_entry.pack(pady=(0, 15))

    transfer_amt_label = ctk.CTkLabel(Card_Frame, text="Amount To Transfer (₹)", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    transfer_amt_label.pack(anchor="center", pady=(10, 2), padx=(0, 150))
    transfer_amt_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Amount To Transfer (₹)", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    transfer_amt_entry.pack(pady=(0, 30))

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

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(10, 0))

    trnsf_btn = ctk.CTkButton(Card_Frame, text="Complete Transfer", font=("Helvetica", 15, "bold"), fg_color="#009933", hover_color="#218838", height=40, width=300, corner_radius=8, command=attempt_transfer)
    trnsf_btn.pack(pady=(0, 15))

    back_btn = ctk.CTkButton(Card_Frame, text="Back To Dashboard", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    back_btn.pack()

def draw_statement_screen(emp_id, emp_name):
    clear_window()
    main_window.title("Bank Management - Get Account Statement")

    Header = ctk.CTkLabel(main_window, text="Account Statement", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(40, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(pady=10, ipadx=40, ipady=30)

    acc_no_label = ctk.CTkLabel(Card_Frame, text="Customer Account Number", font=("Helvetica", 11, "bold"), bg="white", fg="#555555")
    acc_no_label.pack(anchor="center", pady=(10, 2), padx=(0, 145))
    acc_no_entry = ctk.CTkEntry(Card_Frame, placeholder_text="Customer Account Number", font=("Helvetica", 14), width=300, height=40, corner_radius=8)
    acc_no_entry.pack(pady=(20, 25))

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

            St_Header = ctk.CTkLabel(main_window, text=f"Statement for {acc_info[0]}", font=("Helvetica", 24, "bold"), text_color="#0056B3")
            St_Header.pack(pady=(20, 5))

            Bal_Header = ctk.CTkLabel(main_window, text=f"Current Balance: ₹{acc_info[1]:,.2f}", font=("Helvetica", 18, "bold"), text_color="#28A745")
            Bal_Header.pack(pady=(0, 20))

            # Using a Text widget to cleanly display fixed-width data
            txt = ctk.CTkTextbox(main_window, font=("Courier", 12), width=700, height=300, corner_radius=10, fg_color="white", text_color="#333333")
            txt.pack(padx=40, pady=(0, 20))

            txt.insert("end", f"{'Date & Time':<24} | {'Transaction ID':<34} | {'Type':<7} | {'Amount (₹)'}\n")
            txt.insert("end", "-"*87 + "\n")

            if not transactions:
                txt.insert("end", "No transactions found for this account.\n")
            else:
                for t in transactions:
                    t_id, t_send, t_recv, t_amt, t_time = t
                    t_date_str = t_time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    if t_send == acc_no:
                        t_type = "DEBIT"
                    else:
                        t_type = "CREDIT"
                        
                    txt.insert("end", f"{t_date_str:<24} | {t_id:<34} | {t_type:<7} | {float(t_amt):,.2f}\n")

            txt.config(state="disabled") # Make text read-only

            Back_Btn = ctk.CTkButton(main_window, text="Back To Dashboard", font=("Helvetica", 14, "bold"), fg_color="#4A5568", hover_color="#2D3748", height=40, width=250, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
            Back_Btn.pack(pady=(0, 20))

        except sql.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch statement: {err}")

    #Button_Frame = tk.Frame(Card_Frame, bg="white")
    #Button_Frame.pack(pady=(10, 0))

    Search_Btn = ctk.CTkButton(Card_Frame, text="Get Statement", font=("Helvetica", 15, "bold"), fg_color="#007BFF", hover_color="#0056B3", height=40, width=300, corner_radius=8, command=fetch_statement)
    Search_Btn.pack(pady=(0, 15))

    Back_Btn = ctk.CTkButton(Card_Frame, text="Back to Dashboard", font=("Helvetica", 14), fg_color="#E2E8F0", text_color="#333333", hover_color="#CBD5E1", height=40, width=300, corner_radius=8, command=lambda: draw_employee_dashboard(emp_id, emp_name))
    Back_Btn.pack()

def draw_employee_dashboard(Emp_ID, Emp_Name):
    clear_window()
    main_window.title(f"Bank Management - Employee Dashboard ({Emp_ID})")

    Header = ctk.CTkLabel(main_window, text="Employee Dashboard", font=("Helvetica", 28, "bold"), text_color="#0056B3")
    Header.pack(pady=(30, 5))

    SubHeader = ctk.CTkLabel(main_window, text=f"Logged in: {Emp_Name}", font=("Helvetica", 14), text_color="#777777")
    SubHeader.pack(pady=(0, 20))

    Card_Frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=15)
    Card_Frame.pack(padx=80, pady=10, ipadx=40, ipady=30, fill="x")

    Action_Title = ctk.CTkLabel(Card_Frame, text="Administrative Actions", font=("Helvetica", 18, "bold"), text_color="#333333")
    Action_Title.pack(anchor="w", pady=(0, 20))

    def create_action_row(parent, text, button_text, command):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=10)
        lbl = ctk.CTkLabel(row, text=text, font=("Helvetica", 15), text_color="#555555")
        lbl.pack(side="left")
        btn = ctk.CTkButton(row, text=button_text, font=("Helvetica", 13, "bold"), fg_color="#007BFF", hover_color="#0056B3", width=120, height=35, corner_radius=8, command=command)
        btn.pack(side="right")

    create_action_row(Card_Frame, "Create New Customer Account", "Create", lambda: draw_create_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Edit Existing Customer Details", "Edit", lambda: draw_edit_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Transfer Money Between Accounts", "Transfer", lambda: draw_transfer_screen(Emp_ID, Emp_Name))
    create_action_row(Card_Frame, "Generate Account Statement", "Get Statement", lambda: draw_statement_screen(Emp_ID, Emp_Name))

    Logout_Btn = ctk.CTkButton(main_window, text="Log Out", font=("Helvetica", 14, "bold"), fg_color="#DC3545", hover_color="#C82333", height=40, width=200, corner_radius=8, command=draw_homepage)
    Logout_Btn.pack(pady=25)

def draw_mini_statement(acc_name, acc_balance, acc_no):
    clear_window()
    main_window.title(f"Bank Management - Mini Statement for Account: {acc_no}")

    Header = ctk.CTkLabel(main_window, text=f"Last 10 Transactions Of Account: {acc_no}", font=("Helvetica", 22, "bold"), text_color="#0056B3")
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

        txt = ctk.CTkTextbox(main_window, font=("Courier", 12), width=700, height=300, corner_radius=10, fg_color="white", text_color="#333333")
        txt.pack(padx=40, pady=(10, 20))

        txt.insert("end", f"{'Date & Time':<24} | {'Transaction ID':<34} | {'Type':<7} | {'Amount (₹)'}\n")
        txt.insert("end", "-"*96 + "\n")

        if not transactions:
            txt.insert("end", "No recent transactions found for this account.\n")

        else:
            for t in transactions:
                t_id, t_send, t_recv, t_amt, t_time = t
                t_date_str = t_time.strftime("%Y-%m-%d %H:%M:%S")
                
                if t_send == acc_no:
                    t_type = "DEBIT"
                else:
                    t_type = "CREDIT"
                txt.insert("end", f"{t_date_str:<24} | {t_id:<34} | {t_type:<7} | {float(t_amt):,.2f}\n")

        txt.insert("end", "\n\n" +"-"*25 + " *For Older Transactions Please Contact Bank* " + "-"*25 + "\n")
        txt.configure(state="disabled") # Make text read-only

        Back_Btn = ctk.CTkButton(main_window, text="Back To Dashboard", font=("Helvetica", 14, "bold"), fg_color="#4A5568", hover_color="#2D3748", height=40, width=250, corner_radius=8, command=lambda: draw_dashboard(acc_name, acc_balance, acc_no))
        Back_Btn.pack(pady=(0, 20))

    except sql.Error as err:
        messagebox.showerror("Database Error", f"Failed to fetch mini statement: {err}")
        draw_dashboard(acc_name, acc_balance, acc_no)

main_window = ctk.CTk() #The main program window
main_window.title("Bank Management")
main_window.resizable(False,False)
main_window.geometry("800x600+550+200") #To set the window size to 800 by 600 pixels and to pop it in the middle of the screen
main_window.configure(background=COLORS["bg"]) #Setting the background colour

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