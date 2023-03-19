import requests
import json
import matplotlib.pyplot as plt
import hashlib

class RemoteFunc:
    loginUsername = None
    loginPassword = None
    loggedIn = False

    url = 'http://localhost:5000/'
    headers = {'Content-type': 'application/json'}

    def __init__(self):
        print("Initialized the remote...")
    
    #hashing the passwords
    def enCrypt(self, userPassword):
        bytesPassword = userPassword.encode('utf-8') # converting password to array of bytes

        #hashing it
        hash_object = hashlib.sha256(bytesPassword)
        hex_dig = hash_object.hexdigest()


        return hex_dig

    #register
    def Register(self):
        newUsername = input("Username: ")
        newPassword = input("Password: ")

        #hashing
        password = self.enCrypt(newPassword)

        # data to be registered
        data = {'username': newUsername, 'password': password}
        
        # response
        response = requests.post(self.url+"register", data=json.dumps(data), headers=self.headers)

        if response.status_code == 200:
            print(response.json())
        else:
            print(response.json())

    #login
    def Login(self):
        if self.loggedIn == True:
            print("You are already logged in. Press 'O' to logout..")
        
        else:
            userName = input("Username: ")
            loginPassword = input("Password: ")

            password = self.enCrypt(loginPassword)

            data = {'username': userName, "password": password}

            #response
            response = requests.post(self.url+"login", data=json.dumps(data), headers=self.headers)

            if response.status_code == 200:
                self.loggedIn = True
                print(response.json())

                self.loginUsername = userName
                self.loginPassword = loginPassword
            
            else:
                print(response.json())
    
    #logout
    def Logout(self):
        self.loggedIn = False
        self.loginUsername = None
        self.loginPassword = None
        print("Logged Out..")

    #inserting expenses into expense table in database remotely
    def InsertExpenses(self):
        if self.loggedIn == False:
            print("Please login first..")
        
        entry = True
        while entry:

            expense = input(
                "PUT THE NAME OF YOUR EXPENDITURE OR FOR WHAT THING YOU HAVE SPENT YOUR MONEY: ")
            expenditure = input("HOW MUCH YOU HAVE SPENT ? (without commas - 34000000 - 34 million/3 crore 40 lakhs): ")
            date = input(
                "Put the date when you spend your money (Format = dd/mm/yyyy): ")

            expenseData = {'username':self.loginUsername, 'expense':expense, 'expenditure':expenditure, "date":date}

            #response
            response = requests.post(self.url+"createExpenses", data=json.dumps(expenseData), headers=self.headers)
            print(response.json())

            entryChoice = input(
                "DO YOU STILL WANT TO ENTER DATA. TYPE 'Y' IF YOU WANT TO AND 'N' IF YOU WANT TO STOP: ").upper()
            if entryChoice == 'N':
                entry = False

    # showing the data
    def ShowExpenses(self):
        if self.loggedIn == False:
            print("Please login first..")
            
        data = {'username':self.loginUsername}
        
        #response
        response = requests.get(self.url+"showExpenses", data=json.dumps(data), headers=self.headers)

        if response == 404:
            print("Username not found. An error occured. Please try again")

        else:
            moneySpend = 0
            index = 1
            x_axis = []
            y_axis = []

            #expense data
            expense = response.json()

            print('S.no  Reason/Expense/Service  Expenditure  Date\n')

            for x in expense["expenses"]:
                print(str(index) + '. ' + x["expense"] + ' -> ' + x["expenditure"] + ' -> ' + x["date"])
                moneySpend += int(x["expenditure"])
                x_axis.append(x["expense"])
                y_axis.append(int(x["expenditure"]))
                index += 1
            
            print(f"TOTAL MONEY SPEND = {moneySpend}")

            # giving more assistance to the user by showing graph
            # each bar represent the amount of money in each object

            graphChoice = input("Do you want to see the graph(Y/N) - ").upper()
            if graphChoice == 'Y':
                plt.bar(x_axis, y_axis, width=0.3)
                plt.title("Expense View")
                plt.xlabel("<- Expense Name ->")
                plt.ylabel("<- Expenditures ->")
                plt.show()

    # deleting the data
    def deleteExpense(self):
        print("Deleting means you will delete the whole one record. Suppose you give an identification for deletion as date then the whole row where the date \nalong with expense, expenditure will be deleted\n")
        identification1 = input("Enter one identity for deleting the record(expense, expenditure, date): ").lower()
        valueid1 = input("Enter the value of the identity: ")

        identification2 = input(
            "Enter another identity for deleting the record(expense, expenditure, date) [This need to be not same as the previous input given]: ").lower()
        valueid2 = input("Enter the value of the identity: ")

        # identification send as json
        data = {'identification1': identification1, "identification2":identification2, 'value1':valueid1, 'value2':valueid2}

        #response
        response = requests.get(self.url+"deleteExpenses", data=json.dumps(data), headers=self.headers)