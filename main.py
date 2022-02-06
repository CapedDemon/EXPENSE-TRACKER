# importing the required  libraries
import sqlite3
import os
from turtle import width
import matplotlib.pyplot as plt

def mainActivity():
    conn = sqlite3.connect('expenses.db')
    cur = conn.cursor()

    # making the table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (expense TEXT, expenditure TEXT, idate TEXT)
        """)

    conn.commit()

    # saving the salary of the user
    if (os.path.isfile('./monthlySalary.txt')) == False:
        salary = input("Enter your salary: ")
        with open('monthlySalary.txt', 'w') as f:
            f.write(salary)
            f.close()

    else:
        if (os.path.getsize('./monthlySalary.txt')) == 0:
            salary = input("Enter your salary: ")
            with open('monthlySalary.txt', 'w') as f:
                f.write(salary)
                f.close()
    running = True

    while running:

        # main menu
        print('"""\nI = INSERT NEW EXPENSE\nR = SHOWS ALL YOUR DATA WITH DETAILS\nU = FOR UPDATING THE VALUES IN YOUR DATABASE\nD = FOR DELETING THE VLAUES IN YOUR DATABASE\nC = CHANGE YOUR SALARY\nQ = QUIT\n"""')

        choice = input().upper()

        # if the choice is to insert new expense
        if choice == 'I':

            # entry of data loop
            entry = True
            while entry:

                expense = input(
                    "PUT THE NAME OF YOUR EXPENDITURE OR FOR WHAT THING YOU HAVE SPENT YOUR MONEY: ")
                expenditure = input("HOW MUCH YOU HAVE SPENT ?: ")
                date = input(
                    "Put the date when you spend your money (Format = dd/mm/yyyy): ")

                cur.execute("""
                INSERT INTO expenses (expense, expenditure, idate) VALUES (?, ?, ?)""", (expense, expenditure, date))
                conn.commit()

                entryChoice = input(
                    "DO YOU STILL WANT TO ENTER DATA. TYPE 'Y' IF YOU WANT TO AND 'N' IF YOU WANT TO STOP: ")
                if entryChoice == 'N':
                    entry = False

        # if user wants to change the salary
        if choice == 'C':
            newSalary = input("Enter your new salary: ")
            with open('monthlySalary.txt', "w") as f:
                f.write(newSalary)

                f.close()
            print("Salary changed\n")

        # if user wants to see all the data in the command line only
        if choice == 'R':

            # extracting the salary
            f = open('monthlySalary.txt', "r")
            extSalary = int(f.read())
            f.close()

            print('\n')
            print(20 * '*')
            print("Your expenses are as follows:- \n\n")
            recieveData = cur.execute("""
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
            print("Total salary = " + str(extSalary))
            if totalExpenditureSum <= extSalary:
                print("Money Saved = " + str(extSalary - totalExpenditureSum))
            else:
                print("Extra Money Spend = " +
                      str(totalExpenditureSum - extSalary))

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


        # if user want to update data from the database
        if choice == 'U':
            print("(You want to update your data. Theses are the steps to follow - )\n")
            print("i. You need to first give which thing to change.\n")
            print("ii. You then need to specify for which rowid or date or expense reason or expenditure you need to change and give its value\n\n")
            
            changeValue = input("Enter the value which you want to change (expense - For changing the expense reason, expenditure - For changing the expenditure or the amount, date - For changing the data) - ")
            newvalue = input("Enter the new value: ")
            changeValueID = input("Enter any one of the value as an identification for changing the value which you give before it(expense, expenditure, date)- ")
            idvalue = input("Enter the value of the identification - ")
                
            if changeValue == "expense":
                if changeValueID == "expenditure":
                    cur.execute(
                        """UPDATE expenses SET expense = ? where expenditure = ?""", (newvalue, idvalue))

                elif changeValueID == "date":
                    cur.execute(
                        """UPDATE expenses SET expense = ? where idate = ?""", (newvalue, idvalue))
 
            elif changeValue == "expenditure":
                if changeValueID == "expense":
                    cur.execute(
                        """UPDATE expenses SET expenditure = ? where expense = ?""", (newvalue, idvalue))

                if changeValueID == "date":
                    cur.execute(
                        """UPDATE expenses SET expenditure = ? where idate = ?""", (newvalue, idvalue))

            elif changeValue == "date":
                if changeValueID == "expenditure":
                    cur.execute(
                        """UPDATE expenses SET idate = ? where expenditure = ?""", (newvalue, idvalue))

                if changeValueID == "expense":
                    cur.execute(
                        """UPDATE expenses SET idate = ? where expense = ?""", (newvalue, idvalue))

            
            conn.commit()

        # if user wants to delete something
        if choice == 'D':
            print("Deleting means you will delete the whole one record. Suppose you give an identification for deletion as date then the whole row where the date \nalong with expense, expenditure will eb deleted\n")
            identification = input("Enter one identity for deleting the record(expense, expenditure, date): ")
            valueid = input("Enter the value of the identity: ")

            cur.execute("""DELETE from expenses where expenditure = ?""", (valueid,))
            conn.commit()

        # quitting the main while loop
        if choice == 'Q':
            running = False


def main():
    # first check whether the database to store expenses is present or not
    if (os.path.isfile('./expenses.db')) == False:
        print('WELCOME TO EXPENSE TRACKER. HERE YOU CAN STORE YOUR EXPENSES AND KEEP A TRACK OF THEM.\n')
                                                         
        mainActivity()

    else:
        mainActivity()

if __name__ == '__main__':
    main()
