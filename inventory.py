import pymysql

connect = pymysql.connect(host="localhost", user="root", password="root", database="pythondb")
cursor = connect.cursor()

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def checkAdmin(self):
        result = cursor.execute("select * from admin where username = %s and password = %s", (self.username, self.password))
        return True if result > 0 else False

class User:
    def __init__(self, user_Name, user_pwd):
        self.user_Name = user_Name
        self.user_pwd = user_pwd

    def checkUser(self):
        result = cursor.execute("select * from users where username = %s and password = %s",(self.user_Name, self.user_pwd))
        return True if result > 0 else False

def register(name, password, phone, address):
    z = cursor.execute("Insert into users (username, password, phone, address) select * from (select %s,%s,%s,%s) as tmp where not exists(SELECT username FROM users WHERE username = %s) limit 1",
    (name, password, phone, address, name))
    connect.commit()
    return "You have succcessfull Registered" if z else "There is a duplicate entry"


while True:
    print("A-admin")
    print("C-customer")
    print("Q-Quit")
    firstInput = input("Enter as shown above: ")
    if firstInput == "A":
        adminUsername = input("Enter Admin Username: ")
        adminPassword = input("Enter admin Password: ")
        admin = Admin(adminUsername, adminPassword)
        if admin.checkAdmin():
            print("Welcome to inventory management system")
            adminInput = "P"
            while adminInput != "L":
                print("P - Products")
                print("O - Orders")
                print("L - Logout")
                adminInput = input("Enter from above: ")
                if adminInput == "P":
                    print("A - Add Products")
                    print("U - Update")
                    print("D - Delete")
                    
                    addUpdateDel = input("Enter what to do: ")
                    if addUpdateDel == "A":
                        pass
        else:
            print("You have entered wrong credentials")   

    elif firstInput == "C":
        print("N - New Customer Please Register")
        print("O - Old customer")
        newOrOld = input("Enter New or Old: ")
        if newOrOld == "N":
            print("Please Enter Your details To Register")
            newUserName = input("Enter Username: ")
            newUserPass = input("Enter Password: ")
            newUserPhone = input("Enter Phone: ")
            newUserAddress = input("Enter Address:")
            print(register(newUserName, newUserPass, newUserPhone, newUserAddress))
        else:
            oldUserName = input("Enter username: ")
            oldPassword = input("Enter password: ")
            user = User(oldUserName, oldPassword)
            if user.checkUser():
                print("You have successFully logged In")
            else:
                print("You have entered wrong credentials")
    elif firstInput == "Q":
        break                     

