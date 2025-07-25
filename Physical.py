import datetime
import sqlite3

class Database:
    def __init__(self):
        self.create_table()
    
    def create_table(self):
        with sqlite3.connect("Physical Body.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS PBT(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Push_up INTEGER,
                Chin_up INTEGER,
                Set_up INTEGER,
                Mile TEXT,
                Date TEXT
            )''')
            conn.commit()
    
    def save_data(self, Name, Push_up, Chin_up, Set_up, Mile, Date):
        with sqlite3.connect("Physical Body.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO PBT (Name, Push_up, Chin_up, Set_up, Mile, Date) VALUES (?,?,?,?,?,?)", 
                           (Name, Push_up, Chin_up, Set_up, Mile, Date))
            conn.commit()


class PhysicalBodyTest:
    def __init__(self):
        self.db = Database()
    
    def print_result_row(self, row):
        try:
            a = datetime.datetime.strptime(row[5], '%M:%S')
            b = datetime.datetime.strptime('07:30', '%M:%S')
        except ValueError:
            print(f"⚠️ Invalid time format in record: {row[5]}")
            return
        
        result = 'Pass ✅' if row[2] >= 40 and row[3] >= 35 and row[4] >= 40 and a <= b else 'Fail ❌'
        print("{:<7} {:<10} {:<10} {:<10} {:<8} {:<7} {:<10} {:<7}".format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], result
        ))
        print("="*80)

    def Add_test(self):
        try:
            Name = input("Enter your name: ")
            Push_up = int(input("Push ups done: "))
            Chin_up = int(input("Chin ups done: "))
            Set_up = int(input("Set ups done: "))
            Mile = input("Enter mile time (MM:SS): ")
            Date = input("Enter date (dd.mm.yyyy): ")

            # Validate time format
            datetime.datetime.strptime(Mile, '%M:%S')
        except ValueError:
            print("⚠️ Please enter values in correct format!")
            return

        self.db.save_data(Name, Push_up, Chin_up, Set_up, Mile, Date)
        print("✅ Test data saved successfully!")

    def Show_tests(self):
        with sqlite3.connect("Physical Body.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PBT")
            row = cursor.fetchall()

            choice = input("1 for Date Wise, 2 for Name Wise: ")

            print("="*80)
            print("{:<7} {:<10} {:<10} {:<10} {:<8} {:<7} {:<10} {:<7}".format(
                'ID', 'Name', 'Push UP', 'Chin UP', 'Set UP', 'Mile', 'Date', 'Result'))
            print("="*80)

            found = False
            if choice == '1':
                date = input("Enter date (dd.mm.yyyy): ")
                for r in row:
                    if r[6] == date:
                        self.print_result_row(r)
                        found = True
                if not found:
                    print("❌ No data found for this date.")

            elif choice == '2':
                name = input("Enter name: ")
                for r in row:
                    if r[1].lower() == name.lower():
                        self.print_result_row(r)
                        found = True
                if not found:
                    print("❌ No data found for this name.")
            else:
                print("⚠️ Invalid choice!")


def main():
    PhysicalBody = PhysicalBodyTest()
    while True:
        print("\n1. Add Test")
        print("2. View Test")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            PhysicalBody.Add_test()
        elif choice == '2':
            PhysicalBody.Show_tests()
        elif choice == '3':
            print("👋 Exiting the program. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, try again.")

main()
