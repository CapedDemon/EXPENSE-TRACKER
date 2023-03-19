import requests
import json
import bcrypt
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
            expenditure = input("HOW MUCH YOU HAVE SPENT ?: ")
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

        print(response.json())
