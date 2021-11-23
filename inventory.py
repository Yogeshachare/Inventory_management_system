import pymysql
from tabulate import tabulate

connect = pymysql.connect(host="localhost", user="root", password="root", database="pythondb")
cursor = connect.cursor()

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def checkAdmin(self):
        result = cursor.execute("select * from admin where username = %s and password = %s", (self.username, self.password))
        return True if result > 0 else False

    def showProducts(self):
        cursor.execute("select * from products")
        result = cursor.fetchall()
        if len(result) < 1:
            return print("There is no product add products")
        head = ["product_id ", "product_Name ", "product_price ", "product_Quantity", "Description"]
        mydata = []
        for i in result:
            mydata.append([i[0], i[1], i[2], i[3], i[4]])
        print(tabulate(mydata, headers=head, tablefmt="grid"))    

    def addProducts(self, name, price, quantity, description):
        cursor.execute("Insert into products (product_Name, product_price, product_Quantity, product_desc) values(%s,%s,%s,%s)", (name, price, quantity, description))
        connect.commit()
        return "Product added successfully"
    
    def updateProduct(self, id, name, price, quantity, description):
        cursor.execute("Update products set product_Name = %s, product_price = %s, product_Quantity = %s, product_desc = %s where product_id = %s", (name, price, quantity, description, id)) 
        connect.commit()
        return "Data Updated Successfully"   

    def deleteProduct(self,id):
        cursor.execute("Delete from products where product_id = %s", (id))
        connect.commit()
        return "Deleted successfully" 

    def showOrders(self): 
        cursor.execute("select * from orders")
        result = cursor.fetchall()
        if len(result) < 1:
            return print("There are no orders")
        head = ["order_id ", "user_id", "product_id ", "product_name ", "quantity", "price"]
        mydata = []
        for i in result:
            mydata.append([i[0], i[1], i[2], i[3], i[4], i[5]])
        print(tabulate(mydata, headers=head, tablefmt="grid"))    


class User:
    def __init__(self, user_Name, user_pwd):
        self.user_Name = user_Name
        self.user_pwd = user_pwd

    def checkUser(self):
        result = cursor.execute("select * from users where username = %s and password = %s",(self.user_Name, self.user_pwd))
        return True if result > 0 else False

    def showProducts(self):
        cursor.execute("select * from products")
        result = cursor.fetchall()
        if len(result) < 1:
            return print("There is no product add products")
        head = ["product_id ", "product_Name ", "product_price ", "product_Quantity", "Description"]
        mydata = []
        for i in result:
            mydata.append([i[0], i[1], i[2], i[3], i[4]])
        print(tabulate(mydata, headers=head, tablefmt="grid"))   

    def addToCart(self,username, productId, productQuantity):
        cursor.execute("select id from users where username = %s", (username))
        resid = cursor.fetchall()
        userId = resid[0][0]
        cursor.execute("Select product_Name, product_price from products where product_id = %s", (productId))
        resProName = cursor.fetchall()
        productName = resProName[0][0]
        productPrice = resProName[0][1]
        z = cursor.execute("Select * from cart where productId = %s",(productId))
        if z > 0:
            cursor.execute("Select productQuantity from cart where productId = %s", (productId))
            q = cursor.fetchall()
            quanFromCart = q[0][0]
            x = quanFromCart + productQuantity
            cursor.execute("select product_Quantity from products where product_id = %s", (productId))
            res6 = cursor.fetchall()
            if res6[0][0] >= x:
                cursor.execute("Update cart set productQuantity = %s, totalPrice = %s", (x, (x * int(productPrice))))
                connect.commit()
            else:
                return print("Enter quantity as per the products available quantity ")    
        else:
            cursor.execute("Insert into cart(userId, productId, productName, productQuantity, totalPrice) values(%s,%s,%s,%s,%s)", (userId, productId, productName, productQuantity, (int(productPrice) * productQuantity)))
            connect.commit()

    def showCart(self, username):
        cursor.execute("select id from users where username = %s", (username))
        resid = cursor.fetchall()
        userId = resid[0][0]
        cursor.execute("select * from cart where userId = %s", (userId))
        result = cursor.fetchall()
        if len(result) < 1:
            return print("There are no products in cart")    
        head = ["user_Id ", "product_Id", "product_Name ", "product_Quantity ", "Toatal price"]
        mydata = []
        for i in result:
            mydata.append([i[1], i[2], i[3], i[4], i[5]])
        print(tabulate(mydata, headers=head, tablefmt="grid"))

    def addToOrder(self, username):
        cursor.execute("select id from users where username = %s", (username))
        resid = cursor.fetchall()
        userId = resid[0][0]
        cursor.execute("select * from cart where userId = %s", (userId))
        result = cursor.fetchall()
        for i in result:
            user_id = i[1]
            productId = i[2]
            product_Name = i[3]
            product_Quantity = i[4]
            product_price = i[5]
            cursor.execute("Insert into orders (user_id, product_id, product_name, quantity, price) values (%s,%s,%s,%s,%s)", (user_id, productId, product_Name, product_Quantity, product_price))
            connect.commit
        cursor.execute("Select product_Quantity from products where product_id = %s", (productId))
        res2 = cursor.fetchall()
        mainProdQuan = res2[0][0]   
        cursor.execute("Update products set product_Quantity = %s where product_id = %s",((mainProdQuan - product_Quantity), productId))      
        cursor.execute("Delete from cart where (userId = %s)",(userId))
        connect.commit()
        cursor.execute("Select product_Quantity from products where product_id = %s", (productId))
        res4 = cursor.fetchall()
        proQua = res4[0][0]
        if proQua < 1:
            cursor.execute("Delete from products where product_id = %s",(productId))
        connect.commit()    
        return "successfully confirmed order"   

    def removeProduct(self, remProductId):
        cursor.execute("Delete from cart where productId = %s", (remProductId))
        connect.commit()
        return "Product Removed"

    def lessenQuantity(self, lessenId, lessenQuant):
        cursor.execute("Select product_price from products where product_id = %s", (lessenId))
        res1 = cursor.fetchall()
        proPrice = res1[0][0]
        cursor.execute("select product_Quantity from products where product_id = %s", (lessenId))
        res6 = cursor.fetchall()
        if res6[0][0] >= lessenQuant:
            cursor.execute("Update cart set productQuantity = %s, totalPrice = %s where productId = %s", (lessenQuant, (int(proPrice) * lessenQuant), lessenId))
            connect.commit()
        else: 
            return print("Enter quantity as per the products available quantity")    

    def showOrdersUser(self, username):
        cursor.execute("Select id from users where username = %s", (username))
        res3 = cursor.fetchall()
        userId = res3[0][0]
        cursor.execute("Select * from orders where user_id = %s", (userId))
        result = cursor.fetchall()
        if len(result) < 1:
            return print("There are no orders")    
        head = ["order_id ", "user_id", "product_id ", "product_name ", "quantity", "price"]
        mydata = []
        for i in result:
            mydata.append([i[0], i[1], i[2], i[3], i[4], i[5]])
        print(tabulate(mydata, headers=head, tablefmt="grid"))    

#Register
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
#admin    
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
                    print("B - Go Back")
                    admin.showProducts()
                    addUpdateDel = ""
                    while addUpdateDel != "B":
                        addUpdateDel = input("Enter what to do: ")
                        if addUpdateDel == "A":
                            newProductName = input("Enter Product Name: ")
                            newProductPrice = input("Enter Product Price: ")
                            newProductQuantity = input("Enter Product Quantity: ")
                            newProductDesc = input("Enter Product Description")
                            print(admin.addProducts(newProductName, newProductPrice, newProductQuantity, newProductDesc))
                        elif addUpdateDel == "U":
                            updateProId = int(input("Enter same product id: "))
                            updateProName = input("Enter Product Name: ")
                            updateProPrice = input("Enter Product Price: ")
                            updateProQuantity = input("Enter Product Quantity: ")
                            updateProDesc = input("Enter Product Description: ")
                            print(admin.updateProduct(updateProId, updateProName, updateProPrice, updateProQuantity, updateProDesc))
                        elif addUpdateDel == "D":
                            DelProductId = int(input("Enter Product id to Delete"))
                            print(admin.deleteProduct(DelProductId)) 
                elif adminInput == "O":
                    admin.showOrders()               
        else:
            print("You have entered wrong credentials")   
# user
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
                customerOrd = ""
                while customerOrd != "B":
                    print("O - Order Products")
                    print("Cart - C")
                    print("S - See Orders")
                    print("B - Go Back")
                    customerOrd = input("Enter From above: ")
                    if customerOrd == "O":
                        user.showProducts()
                        print("Select Products From the List")
                        userProductId = input("Enter Product Id from the List: ")
                        userProductQuantity = int(input("Enter Product Quantity: "))
                        cursor.execute("select product_Quantity from products where product_id = %s", (userProductId))
                        productQuantity = cursor.fetchall()
                        if userProductQuantity > productQuantity[0][0]:
                            print("Entered higher quantity than available Quantity")
                        else:
                            user.addToCart(oldUserName, userProductId, userProductQuantity)
                    # cart
                    elif customerOrd == "C":
                        cartInput = ""
                        while cartInput != "B":
                            cartInput = input("Enter from above: ")
                            print("CO - Confirm Order")
                            print("R - Remove Product")
                            print("CH - Change the Quantity")
                            print("B - Go Back")
                            user.showCart(oldUserName)
                            if cartInput == "CO":
                                print(user.addToOrder(oldUserName))
                            elif cartInput == "R":
                                remProductId = int(input("Enter product ID: "))
                                print(user.removeProduct(remProductId))
                            elif cartInput == "CH":
                                lessenId = int(input("Enter Product Id: "))
                                lessenQuant = int(input("Enter new Quantity: "))
                                user.lessenQuantity(lessenId, lessenQuant)  
                    elif customerOrd == "S":
                        user.showOrdersUser(oldUserName)                  

            else:
                print("You have entered wrong credentials")


    elif firstInput == "Q":
        break                     

