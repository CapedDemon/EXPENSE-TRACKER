# importing the required  libraries
import sqlite3
import os
import matplotlib.pyplot as plt
from requests import get
from pprint import PrettyPrinter

class ExpenseTracker():

    def __init__(self):
        self.salary = None
        
        print("""
                            INITIALISED EXPENSE TRACKER
                                track your expenses
                                                  __      
                         __|__               __  |  |     
                        "  |            __  |  | |  |      
                        "--|--     __  |  | |  | |  |      
                           |  "   |  | |  | |  | |  |       
                        ---|--"   |__| |__| |__| |__|        


        """)
        print('WELCOME TO EXPENSE TRACKER. HERE YOU CAN STORE YOUR EXPENSES AND KEEP A TRACK OF THEM.\n')


    def h_et(self):
        print("""
                           HELP GUIDE
                    TAKE HELP ANYTIME YOU NEED
                 CONTACT - dolaishreejan@gmail.com

                1. First, press 1 to load or create your database
                2. Press 2 to load your salary
                3. Press 7 to change your salary
                4. Press 3 to insert expenses - the reason you are inserting,
                    amount, date
                5. Press 4 to see the expenses with core details
                6. Press 5 to update your expenses
                7. Press 6 to delete your expenses
                8. Press 8 to see your expenses with other currency
                9. To see the help guide
                10. Press 10 to quit
                11. At first, press H to take help.
                12. Press C to continue at first.
        """)

    def l_et(self):
        print("""

            1. CREATE THE DATABASE/STORAGE OR WORK WITH PREVIOUS DATABASE TO STORE YOUR EXPENSES = 1
            2. LOAD YOUR SALARY = 2
            3. INSERT NEW EXPENSES = 3
            4. SHOWS ALL YOUR DATA WITH CORE DETAILS = 4
            5. UPDATE YOUR EXPENSES = 5
            6. DELETE YOUR EXPENSES = 6
            7. CHANGE YOUR SALARY = 7
            8. CURRENCY CONVERTER = 8
            9. HELP = 9
            10. QUIT = Q

        """)

        menu = input(":- ")
        return menu

    def c_et(self):
        #creating the database
        createdb = input("Create new database (C) | Work with previous database (P) - ").upper()
        if createdb == 'C':
            name = input("Enter the name of your database (Expense.db, mongo.db, etc) - ")
            self.conn = sqlite3.connect(name)
            self.cur = self.conn.cursor()

        elif createdb == 'P':
            name = input("Enter the name of your database (Expense.db, mongo.db, etc) - ")
            self.conn = sqlite3.connect(name)
            self.cur = self.conn.cursor()
        
        # making the table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (expense TEXT, expenditure TEXT, idate TEXT)
            """)

        self.conn.commit()
    
    def s_et(self):
        # working with salary
        salaryWork = input("Enter new salary (E) | Load your salary (L) - ").upper()

        if salaryWork == 'E':   
            salaryFile = input("Enter the path of the file where your salary will be saved (Ex- salary.txt) - ")
            self.salary = input("Enter your salary - ")
            with open(salaryFile, 'w') as f:
                f.write(self.salary)
                f.close()

        elif salaryWork == 'L':
            salaryFile = input(
                "Enter the path of the file where your salary is saved (Ex- salary.txt) - ")
            
            if (os.path.getsize(salaryFile)) == 0:
                self.salary = input("Your salary file is empty. Put your salary - ")
                with open(salaryFile, 'w') as f:
                    f.write(self.salary)
                    f.close()
            else:
                with open(salaryFile, 'r') as f:
                    self.salary = f.read()
                    f.close()

        print("SALARY LOADED\n")

    def i_et(self):
        # entry of data loop
        entry = True
        while entry:

            expense = input(
                "PUT THE NAME OF YOUR EXPENDITURE OR FOR WHAT THING YOU HAVE SPENT YOUR MONEY: ")
            expenditure = input("HOW MUCH YOU HAVE SPENT ?: ")
            date = input(
                "Put the date when you spend your money (Format = dd/mm/yyyy): ")

            self.cur.execute("""
                INSERT INTO expenses (expense, expenditure, idate) VALUES (?, ?, ?)""", (expense, expenditure, date))
            self.conn.commit()

            entryChoice = input(
                "DO YOU STILL WANT TO ENTER DATA. TYPE 'Y' IF YOU WANT TO AND 'N' IF YOU WANT TO STOP: ").upper()
            if entryChoice == 'N':
                entry = False

    def sc_et(self):
        # changing the salary
        salaryFile = input(
            "Enter the path of the file where your salary will be saved (Ex- salary.txt) - ")
        self.salary = input("Enter your new salary: ")
        with open(salaryFile, "w") as f:
            f.write(self.salary)

            f.close()
        print("SALARY CHANGED\n")

    def r_et(self):
        # showing the expenses with core details
        print(20 * '*')
        print("Your expenses are as follows:- \n\n")
        recieveData = self.cur.execute("""
                SELECT * FROM expenses
                """)

        # printing the expenditure and calculating the total expenditure and stroing the data in lists for plotting the graph
        totalExpenditureSum = 0
        index = 1
        x_axis = []
        y_axis = []
        print('S.no  Reason/Expense/Service  Expenditure  Date\n')
        for x in recieveData:
            print(str(index) + '. ' + x[0] + ' -> ' + x[1] + ' -> ' + x[2])
            totalExpenditureSum = totalExpenditureSum + int(x[1])
            index += 1
            x_axis.append(x[0])
            y_axis.append(int(x[1]))

        print('\n')

        # printing the total salary and total money saved or extra spend
        print("Total salary = " + (self.salary))
        if totalExpenditureSum <= int(self.salary):
            print("Money Saved = " + str(int(self.salary) - totalExpenditureSum))
        else:
            print("Extra Money Spend = " + str(totalExpenditureSum - int(self.salary)))

        print(20 * '*')
        print('\n')
        print("(See the graph for more clear vision of your expense.)")

            # plotting th graph
            # This is a bar graph
            # In the x-axis there are the names or the reasons of your expense
            # In the y-axis there are the values of the expense
            # The title of the graph is 'Expense View'
        graphChoice = input("Do you want to see the graph(Y/N) - ").upper()
        if graphChoice == 'Y':
            plt.bar(x_axis, y_axis, width=0.3)
            plt.title("Expense View")
            plt.xlabel("<- Expense Name ->")
            plt.ylabel("<- Expenditures ->")
            plt.show()

    #updating the expenses
    def u_et(self):
        print("i. You need to first give which thing to change.\n")
        print("ii. You then need to specify for which rowid or date or expense reason or expenditure you need to change and give its value\n\n")

        changeValue = input(
            "Enter the value which you want to change (expense - For changing the expense reason, expenditure - For changing the expenditure or the amount, date - For changing the date) - ")
        newvalue = input("Enter the new value: ")
        changeValueID = input(
              "Enter any one of the value as an identification for changing the value which you give before it(expense, expenditure, date)- ")
        idvalue = input("Enter the value of the identification - ")

        if changeValue == "expense":
            if changeValueID == "expenditure":
                self.cur.execute(
                        """UPDATE expenses SET expense = ? where expenditure = ?""", (newvalue, idvalue))

            elif changeValueID == "date":
                self.cur.execute(
                        """UPDATE expenses SET expense = ? where idate = ?""", (newvalue, idvalue))

        elif changeValue == "expenditure":
            if changeValueID == "expense":
                self.cur.execute(
                        """UPDATE expenses SET expenditure = ? where expense = ?""", (newvalue, idvalue))

            elif changeValueID == "date":
                self.cur.execute(
                        """UPDATE expenses SET expenditure = ? where idate = ?""", (newvalue, idvalue))

        elif changeValue == "date":
            if changeValueID == "expenditure":
                self.cur.execute(
                        """UPDATE expenses SET idate = ? where expenditure = ?""", (newvalue, idvalue))

            elif changeValueID == "expense":
                self.cur.execute(
                        """UPDATE expenses SET idate = ? where expense = ?""", (newvalue, idvalue))

        self.conn.commit()

    # deleting the expenses
    def d_et(self):
        print("Deleting means you will delete the whole one record. Suppose you give an identification for deletion as date then the whole row where the date \nalong with expense, expenditure will eb deleted\n")
        identification1 = input("Enter one identity for deleting the record(expense, expenditure, date): ")
        valueid1 = input("Enter the value of the identity: ")

        identification2 = input(
            "Enter another identity for deleting the record(expense, expenditure, date) [This need to be not same as the previous input given]: ")
        valueid2 = input("Enter the value of the identity: ")

        if identification1 == "expense":
            if identification2 == "expenditure":
                self.cur.execute(
                    """DELETE from expenses where expense = ? AND expenditure = ?""", (valueid1,valueid2))

            elif identification2 == "date":
                self.cur.execute(
                    """DELETE from expenses where expense = ? AND idate = ?""", (valueid1,valueid2))

        elif identification1 == "expenditure":
            if identification2 == "expense":
                self.cur.execute(
                    """DELETE from expenses where expenditure = ? AND expense = ?""", (valueid1, valueid2))
            
            elif identification2 == "date":
                self.cur.execute(
                    """DELETE from expenses where expenditure = ? AND idate = ?""", (valueid1, valueid2))

        elif identification1 == "date":
            if identification2 == "expense":
                self.cur.execute(
                    """DELETE from expenses where idate = ? AND expense = ?""", (valueid1, valueid2))

            elif identification2 == "expenditure":
                self.cur.execute(
                    """DELETE from expenses where idate = ? AND expenditure = ?""", (valueid1, valueid2))
        self.conn.commit()

    # currency converter
    def cov_et(self):
        
        #base url
        BASE_URL = "https://free.currconv.com/"
        API_KEY = "9ed7b0de375985de7037"

        printer = PrettyPrinter()

        endpoint = f"api/v7/currencies?apiKey={API_KEY}"
        url = BASE_URL + endpoint
        data = get(url).json()['results']

        data = list(data.items())
        data.sort()

        print("THESE ARE THE LIST OF CURRENCY - \n")

        for name, currency in data:
            name = currency['currencyName']
            _id = currency['id']
            symbol = currency.get("currencySymbol", "")
            print(f"{_id} - {name} - {symbol}")

        print("\n")
        conchoice = input("Do you want to change currency (y/n) - ")

        if conchoice == 'n':
            print("BYE\n")
        
        else:
            curr1 = input("Enter the base currency - ").upper()
            curr2 = input("Enter a currency to convert to: - ").upper()

            endpoint = f"api/v7/convert?q={curr1}_{curr2}&compact=ultra&apiKey={API_KEY}"
            url = BASE_URL + endpoint
            data = get(url).json()

            if len(data) == 0:
                print('Invalid currencies.\n')

            else:
                rate = list(data.values())[0]
                print(f"{curr1} -> {curr2} = {rate}\n")

                recieveData = self.cur.execute("""
                SELECT * FROM expenses
                """)

                print("Your expenses after the conversion - \n")
                index = 1
                for x in recieveData:
                    print(str(index) + '. ' + curr1 + " " + x[1] + " converted -> " + curr2 + " " + str(rate*int(x[1])))
                
                print("\n\n")

def main():
    et = ExpenseTracker()
    starter = input("Press 'C' to continue or 'H' to see the help guide...\n").upper()
    
    if starter == 'H':
        et.h_et()
    
    if starter == 'C':
        menuchoice =  et.l_et()
        while menuchoice != 'Q':
            if menuchoice == '1':
                et.c_et()

            elif menuchoice == '2':
                et.s_et()

            elif menuchoice == '3':
                et.i_et()

            elif menuchoice == '4':
                et.r_et()

            elif menuchoice == '5':
                et.u_et()

            elif menuchoice == '6':
                et.d_et()

            elif menuchoice == '7':
                et.sc_et()

            elif menuchoice == '8':
                et.cov_et()
            
            elif menuchoice == '9':
                et.h_et()
            
            menuchoice = et.l_et()