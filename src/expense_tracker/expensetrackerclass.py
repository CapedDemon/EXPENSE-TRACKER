# importing the required  libraries
import sqlite3
import os
import matplotlib.pyplot as plt
from requests import get
from pprint import PrettyPrinter
import remotefunc

class ExpenseTracker:

    __salary = 0


    def __init__(self):
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
        self.remote = remotefunc.RemoteFunc()
        print('WELCOME TO EXPENSE TRACKER. HERE YOU CAN STORE YOUR EXPENSES AND KEEP A TRACK OF THEM.\n\t\t\t\tPress H for help\n')


    # function that shows the user
    # the list of commands he/she can use
    def helpGuide(self):
        print("""
                           HELP GUIDE
                    TAKE HELP ANYTIME YOU NEED
                 CONTACT - dolaishreejan@gmail.com

                        This Guide is for local 
                        management of expenses

                1. First, press 1 to load or create your database
                2. Press 2 to load your salary
                3. Press 7 to change your salary
                4. Press 3 to insert expenses - the reason you are inserting,
                    amount, date
                5. Press 4 to see the expenses with core details
                6. Press 5 to update your expenses
                7. Press 6 to delete your expenses
                8. Press 8 to see your expenses with other currency
                9. To see the help guide press H



                        For Remote Management - 
                        
                A. If you have already have login username and password, login
                    using it by pressing "L"
                B. To register press "R"
                C. To insert data remotely - "I"
                D. To delete - "D"
                E. To update - "U"
                F. To get records - "S"
                G. To logout - "O"
                H. To delete your account and other expenses - "DEL"

                Press "Q" for quitting the program
        """)
    
    def createDB(self):
            #creating the database
            createdb = input("Create new database (C) | Work with previous database (P) - ").upper()
            name = input("Enter the name of your database (Expense.db, mongo.db, etc) - ")# seeking name
            if createdb == 'C':
                self.conn = sqlite3.connect(name)
                self.cur = self.conn.cursor()

            elif createdb == 'P':
                self.conn = sqlite3.connect(name)
                self.cur = self.conn.cursor()
            
            # making the table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses (expense TEXT, expenditure TEXT, idate TEXT)
                """)

            self.conn.commit()
    
    def salaryWork(self):
        # working with salary
        salaryChoice = input("Enter new salary (E) | Load your salary (L) - ").upper()

        if salaryChoice == 'E':   
            salaryFile = input("Enter the path of the file where your salary will be saved (Ex- salary.txt) - ")
            self.salary = input("Enter your salary - ")
            with open(salaryFile, 'w') as f:
                f.write(self.salary)
                f.close()

        elif salaryChoice == 'L':
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

    def insertDB(self):
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

    def changeSalary(self):
        # changing the salary
        salaryFile = input(
            "Enter the path of the file where your salary will be saved (Ex- salary.txt) - ")
        self.salary = input("Enter your new salary: ")
        with open(salaryFile, "w") as f:
            f.write(self.salary)

            f.close()
        print("SALARY CHANGED\n")

    def showDB(self):
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
        if self.salary != 0:
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
    def updateDB(self):
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
    def deleteDB(self):
        print("Deleting means you will delete the whole one record. Suppose you give an identification for deletion as date then the whole row where the date \nalong with expense, expenditure will be deleted\n")
        identification1 = input("Enter one identity for deleting the record(expense, expenditure, date): ").lower()
        valueid1 = input("Enter the value of the identity: ")

        identification2 = input(
            "Enter another identity for deleting the record(expense, expenditure, date) [This need to be not same as the previous input given]: ").lower()
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
    def currencyConverter(self):
        
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


    # function to load functions
    def loadFunc(self):
        self.FunctionMaps = {
            #offline
            "1": self.createDB,
            "2": self.salaryWork,
            "3": self.insertDB,
            "4": self.showDB,
            "5": self.updateDB,
            "6": self.deleteDB,
            "7": self.changeSalary,
            "8": self.currencyConverter,
            "H": self.helpGuide,

            #online
            "R": self.remote.Register,
            "L": self.remote.Login,
            "O": self.remote.Logout,
            "I": self.remote.InsertExpenses,
            "S": self.remote.ShowExpenses,
            "D": self.remote.deleteExpense,
            "U": self.remote.updateExpense,
            "DEL": self.remote.delAccount
        }

    # assign users's command to function
    def assignFunc(self):
        if (self.command not in self.FunctionMaps):
            print("Give write command\n")
        else :
            self.FunctionMaps[self.command]()

    # the function that takes user input
    def takeCommand(self):
        self.command = input("expense-tracker $: ");

        while self.command != "Q":
            if (self.command == "Q"):
                print("Bye\n")
                break
            self.assignFunc()
            self.command = input("expense-tracker $: ")