import json
import sqlite3
from datetime import datetime

Current_date = datetime.now().strftime('%d.%m.%Y')

class Bank:
    def __init__(self, ID='NBP', password=5225, balance=500):
        self.ID = ID
        self.db_name = 'BankManegement.db'
        self.password = password
        self.balance = balance
        self.create_table()
        
    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def change_password(self, accounts):
        o_password = int(input("Enter your Old password :"))
        if o_password == self.password:
            re_password = int(input("Reenter your old Password :"))
            if re_password == o_password:
                new_password = int(input("Enter your new password :"))
                self.password = new_password
                save_accounts(accounts)
                self.save_history(Rs='Password successfully Change')
            else:
                print("Re enter password Wrong!")
        else:
            print("Password is Wrong")
            
    def deposit(self, accounts):
        amount = int(input("Enter your amount to deposit :"))
        
        self.balance += amount
        if self.ID == 'NBP':
            print("Hello")
            accounts['NBP'].balance -= amount

        accounts['NBP'].balance += amount
        print(f"Rs {amount} deposit")
        print(f"Your current balance is {self.balance}")
        self.save_history(Rs=amount, Type='Deposit')
        save_accounts(accounts)
    
    def withdraw(self, accounts):
        amount = int(input("Enter your amount to with draw :"))
        
        self.balance -= amount
        if self.ID == 'NBP':
            print("Hello")
            accounts['NBP'].balance += amount

        accounts['NBP'].balance -= amount
        print(f"Rs {amount} with draw")
        print(f"Your current balance is {self.balance}")
        self.save_history(Rs=amount, Type='with draw')
        save_accounts(accounts)
    
    def send_money(self, accounts):
        ID = input("Enter ID to send  money :")
        
        if ID not in accounts:
            print("ID is wrong try again.")
            return ID
        
        amount = int(input("Enter your amount to send :"))
        
        if self.balance < amount:
            print("Insufficient balance.")
            return
        
        self.balance -= amount
        accounts[ID].balance += amount
        
        print(f"Rs {amount} send to {ID}")
        print(f"Your current balance is {self.balance}")
        self.save_history(Rs=amount, Type='Send Money', Receiver_id=ID)
        accounts[ID].save_history(Rs=amount, Type='Receive Balance', Receiver_id=self.ID)
        
    def show_balance(self):
        print(f"Your current balance is {self.balance}")
    
    def to_dict(self):
        return {'password': self.password, 'balance' : self.balance}

    def create_table(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS TRS(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                User_id TEXT,
                Rs INTEGER,
                Type TEXT,
                Date TEXT,
                Receiver_id TEXT
            )''')
            conn.commit()
    
    def save_history(self, Rs, Type=None,Receiver_id=None):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TRS (User_id, Rs, Type, Date, Receiver_id) VALUES (?,?,?,?,?)", (self.ID, Rs, Type, Current_date, Receiver_id))
            conn.commit()
    
    def load_history(self):
        with self.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM TRS WHERE user_id=?", (self.ID,))
            
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    if row[3] == 'Send Money':
                        print(f"ID : {row[0]} {row[1]} Rs {row[2]} {row[3]} to {row[5]} ON {row[4]}")
                    elif row[3] == 'Receive Balance':
                        print(f"ID : {row[0]} {row[1]} Rs {row[2]} {row[3]} From {row[5]} ON {row[4]}")
                    elif row[3] == None:
                        print(f"ID : {row[0]} {row[2]} ON {row[4]}")
                    else:
                        print(f"ID : {row[0]} {row[1]} Rs {row[2]} {row[3]} ON {row[4]}")
            else:
                print("NO Transaction history found")
        
def create_account(accounts):
    ID = input("Enter your ID :")
    password = int(input("Enter your password :"))
    
    if ID in accounts and accounts[ID].password == password:
        print("Account already create.")
        return
    new_account = Bank(ID=ID,password=password)
    accounts[ID] = new_account
    save_accounts(accounts)
    print("Account create successfully")

def save_accounts(accounts):
    data = {ide : account.to_dict() for ide, account in accounts.items()}
    with open('accounts.json', 'w') as file:
        json.dump(data, file, indent=4)

def load_accounts():
    try:
        with open('accounts.json', 'r') as file:
            data = json.load(file)
        
        accounts = {}
        
        for ID, detail in data.items():
            new = Bank(ID=ID, password=detail['password'], balance=detail['balance'])
            accounts[ID] = new
        return accounts
    except FileNotFoundError:
        print("file does not exist. Creating a file...")
        accounts = {'NBP': Bank()}
        save_accounts(accounts)
        return accounts

def main():
    accounts = load_accounts()
    while True:
        print("Main Menu".center(30, '='))
        print("1. Log in.")
        print("2. Create account")
        print("3. Exit")
        print(''.center(30, '='))
        
        choice = int(input("Enter you choice :"))
        
        if choice == 1 :
            ID =  input("Enter your ID :")
            password = int(input("Enter your password :"))
            
            if ID in accounts and accounts[ID].password == password:
                print("Log in successfully")
                active_account = accounts[ID]
                print("Welcome " + active_account.ID)
                while True:
                    print("Log in Menu".center(30, '='))
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Send Money")
                    print("4. Show balance")
                    print("5. View History")
                    print("6. Change Password")
                    print("7. Exit")
                    print(''.center(30, '='))
                    
                    choice = int(input("Enter your choice :"))
                    
                    action = {
                        1: lambda: active_account.deposit(accounts),
                        2: lambda: active_account.withdraw(accounts),
                        3: lambda: active_account.send_money(accounts),
                        4: lambda: active_account.show_balance(),
                        5: lambda: active_account.load_history(),
                        6: lambda: active_account.change_password(accounts),
                    }
                    
                    if choice in action:
                        action[choice]()
                    if choice == 7:
                        break
            else:
                print("ID or password is wrong")
        elif choice == 2:
            create_account(accounts)
        elif choice == 3:
            print("By!")
            break
        else:
            print("Invalid choice try again.")
if __name__ == '__main__':
    main()