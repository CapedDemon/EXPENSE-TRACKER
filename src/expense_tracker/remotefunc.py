import requests
import json
import bcrypt
import hashlib

class RemoteFunc:
    loginUsername = None
    loginPassword = None

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
        userName = input("Username: ")
        loginPassword = input("Password: ")

        password = self.enCrypt(loginPassword)

        data = {'username': userName, "password": password}

        #response
        response = requests.post(self.url+"login", data=json.dumps(data), headers=self.headers)

        if response.status_code == 200:
            self.loggedIn = True
            print(response.json())
            saveLogin = input("Do you want to save login preferences (y/n) ? (It would not work if you would close the program, the data is stored till the program is opened): ")

            if (saveLogin == "y"):
                self.loginUsername = userName
                self.loginPassword = loginPassword
        
        else:
            print(response.json())