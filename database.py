import mysql.connector as sql

database = sql.connect(host="localhost", user="root")

cursor = database.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Bank_Database")
cursor.execute("USE Bank_Database")
cursor.execute("CREATE TABLE IF NOT EXISTS Accounts (Acc_No VARCHAR(16) PRIMARY KEY, Acc_Name VARCHAR(50) NOT NULL, Acc_Balance DECIMAL(15,2), Acc_opn_date TIMESTAMP)")
cursor.execute("CREATE TABLE IF NOT EXISTS Employees (Emp_ID VARCHAR(6) PRIMARY KEY, Emp_Name VARCHAR(50) NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS Account_Credentials (Acc_No VARCHAR(16) PRIMARY KEY, Usrnm VARCHAR(10) NOT NULL, Psswd VARCHAR(64) NOT NULL, FOREIGN KEY (Acc_No) REFERENCES Accounts(Acc_No) ON DELETE CASCADE)")
cursor.execute("CREATE TABLE IF NOT EXISTS Employee_Credentials (Emp_ID VARCHAR(6) PRIMARY KEY, Emp_Psswd VARCHAR(64) NOT NULL, FOREIGN KEY (Emp_ID) REFERENCES Employees(Emp_ID) ON DELETE CASCADE)")
cursor.execute("CREATE TABLE IF NOT EXISTS Transactions (Trnsc_ID VARCHAR(30) PRIMARY KEY, Sender VARCHAR(16), Reciever VARCHAR(16), Trns_Amt DECIMAL(15,2), Trns_Time DATETIME)")

database.commit()
database.close()
print("Done")