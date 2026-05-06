import sqlite3

databasefile = r"C:\Users\karab\Downloads\ITAPA2\LondonRoots.DB"

connection = sqlite3.connect(databasefile)

cursorDb = connection.cursor() 

def addEmployee():
    name = input("Enter employee name: ")
    surname = input("Enter employee surname: ")
    cell = input("Enter employee cell: ")
    email = input("Enter employee email: ")
    
    cursorDb.execute("INSERT INTO Employee(name, surname, cell, email) VALUES(?,?,?,?)",
                     (name, surname, cell, email))
    connection.commit()
    print("Employee added successfully.")
    
def showAllEmployees():
    cursorDb.execute("SELECT * FROM Employee")
    employees = cursorDb.fetchall()
    for emp in employees:
        print(f"ID: {emp[0]} | Name: {emp[1]} {emp[2]} / Cell: {emp[3]} / Email: {emp[4]}")

def addCustomer():
    name = input("Enter customer name: ")
    surname = input("Enter customer surname: ")
    cell = input("Enter customer cell: ")
    email = input("Enter customer email: ")
    billing = input("Enter customer billing address: ")
    
    cursorDb.execute("INSERT INTO Customer(name, surname, cell, email, billing_address) VALUES(?,?,?,?,?)",
                    (name, surname, cell, email, billing))
    connection.commit()
    print("Customer added successfully.")
    
def addProduct():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    qty = int(input("Enter product quantity: "))
    
    cursorDb.execute("INSERT INTO Product(name, price, quantity) VALUES(?,?,?)",
                    (name, price, qty))
    connection.commit()
    print("Product added successfully.")
    
def sellProduct():
    salesID = int(input("Enter product ID to sell: "))
    qty = int(input("Enter quantity: "))
    date = input("Enter sale date (YYYY-MM-DD): ")
    
    cursorDb.execute("SELECT name, price, quantity FROM Product WHERE salesID=?", (salesID,))
    product = cursorDb.fetchone()
    
    if product and product[2] >= qty: 
        total = product[1] * qty
        cursorDb.execute("UPDATE Product SET quantity=? WHERE productID=?", (product[2] - qty, salesID))
        cursorDb.execute("INSERT INTO Sales(date, product_name, total) VALUES(?,?,?)",
                        (date, product[0], total))
        connection.commit()
        print("Sale recorded successfully.")
    else:
        print("Not enough stock.")
        
def mainMenu():
    while True:
        print("\nWelcome to the Store Management System!")
        print("1. Manage Employees")
        print("2. Manage Customers")
        print("3. Manage Products")
        print("4. Manage Sales")
        print("0. Exit")
        
        
        choice = input("Select option: ")
        
        
        if choice == "1":
            EmployeeMenu() #calls EmployeeMenu
        elif choice == "2":
            customerMenu()
        elif choice == "3":
            productMenu()
        elif choice == "4":
            salesMenu()
        elif choice == "0":
            break
        
     
def EmployeeMenu():
    while True:
        print("\nHello. Welcome to Employee Management")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Display Employees")
        print("0. Return to Main Menu")
        
        choice = input("Select an option: ")
        if choice == "1":
            name = input("Name: ")
            surname = input("Surname: ")
            cell = input("Cell: ")
            email = input("Email: ") 
            emp = EmployeeManager(name, surname, cell, email)
            emp.insert_person()
        elif choice == "2":
            empID = int(input("Enter employee ID to remove: "))
            EmployeeManager("", "", "","").remove_person(empID)
            print("Employee removed")
        elif choice == "3":
            EmployeeManager("","","","").display_all()
        elif choice == "0":
            break
       
        

def customerMenu():
    while True:
        print("Customer Management\n")
        print("1. Add Customer")
        print("2. Remove Customer")
        print("0. Return")
        
        choice = input("Select an option: ")
        if choice == "1":
            name = input("Name: ")
            surname = input("Surname: ")
            cell = input("Cell: ")
            email = input("Email: ")
            billing = input("Billing Address: ")
            cust = CustomerManager(name, surname, cell, email, billing)
            cust.insert_person()
        elif choice == "2":
            custID = int(input("Enter customer ID to remove: "))
            CustomerManager("","","","","").remove_person(custID)
            print("Customer removed.") 
        elif choice == "3":
            CustomerManager("","","","","").display_all()
        elif choice == "0":
            break
       
       
        

def productMenu():
    store = Store()
    while True:
        print("\nProduct Management")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Product")
        print("4. Display Product")
        print("5. Sell Product")
        print("0. Return to Main Menu")
        
        choice = input("Select an option: ")
        if choice == "1":
            name = input("Product Name: ")
            price = float(input("Price: "))
            qty = int(input("Quantity: "))
            store.add_product(name, price, qty)
        elif choice == "2":
            prodID = int(input("Enter product ID to remove: "))
            store.remove_product(prodID)
            print("Product removed.")
        elif choice == "3":
            prodID = int(input("Enter product ID to update: "))
            name = input("Enter new name: ")
            price = float(input("Enter new price: "))
            qty = int(input("Enter new quantity: "))
            store.update_product(prodID, name, price, qty)
            print("Product updated.")
        elif choice == "4":
            store.display_products()
        elif choice == "5":
            prodID = int(input("Enter product ID to sell: "))
            qty = int(input("Quantity: "))
            date = input("Sale date: YYYY-MM-DD): ")
            store.sell_product(prodID, qty, date)
        elif choice == "0":
            break
       
       
def salesMenu():
    store = Store()
    while True:
        print("\nSales Management")
        print("1. Sell Display")
        print("2. Display Sales")
        print("0. Return to Main Menu")
        
        choice = input("Select an option: ")
        if choice == "1":
            salesID = int(input("Enter product ID to sell: "))
            qty = int(input("Quantity: "))
            date = input("Sale Date (YYYY-MM-DD): ")
            store.sell_product(salesID, qty, date)
        elif choice == "2":
            store.display_sales()
        elif choice == "0":
            break
        

    
        
from abc import ABC, abstractmethod
import sqlite3

#Connect to LondonRoots.db

connection = sqlite3.connect(databasefile)
cursorDb = connection.cursor()

class PersonManager(ABC):
 def __init__(self, name, surname, cell, email):
    self.name = name
    self.surname = surname
    self.cell = cell
    self.email = email 
@abstractmethod
def insert_person(self):
    pass 
@abstractmethod
def remove_person(self, person_id):
        pass
@abstractmethod           
def display_all(self):
    pass 
    
class EmployeeManager(PersonManager):
 def insert_person(self):
        cursorDb.execute("INSERT INTO Employee(name, surname, cell, email) VALUES(?,?,?,?)",
                         (self.name, self.surname, self.cell, self.email))
        connection.commit()
        print("Employee added successfully.")
        
def remove_employee(self, employeeID):
        cursorDb.execute("DELETE FROM Employee WHERE employeeID=?", (employeeID,))
        connection.commit()
        print("Employee removed")
        
def display_AllEmplpyee(self):
        cursorDb.execute("SELECT * FROM Employee")
        employees = cursorDb.fetchall()
        for emp in employees:
            print(f"ID: {emp[0]} / Name: {emp[1]} {emp[2]} / Cell: {emp[3]} / Email: {emp[4]}")
            
class CustomerManager(PersonManager):
 def __init__(self, name, surname, cell, email, billing_address):
        super().__init__(name, surname, cell, email)   
        self.billing_address = billing_address
    
def insert_customer(self):
        cursorDb.execute("INSERT INTO Customer(name, surname, cell, email, billing_address) VALUES(?,?,?,?,?)",
                         (self.name, self.surname, self.cell, self.email, self.billing_address))
        connection.comit()
        print("Customer added successfully")
        
def  remove_customer(self, customerID):
        cursorDb.execute("DELETE FROM Customer WHERE customerID=?", (customerID,))
        connection.commit()
        print("Customer removed")
        
def display_allcustomer(self):
        cursorDb.execute("SELECT * FROM Customer")
        customers = cursorDb.fetchall()
        for cust in customers:
            print(f"ID: {cust[0]} / Name: {cust[1]} {cust[2]} / Cell: {cust[3]} / Email: {cust[4]} / Billing: {cust[5]}")
            
class Store:
 def add_product(self, name, price, quantity):
       cursorDb.execute("INSERT INTO Product(name, price, quantity) VALUES(?,?,?)", (name, price, quantity))
       connection.commit()
       print("Product added successfully")
       
def remove_product(self, productID):
         cursorDb.execute("DELETE FROM Product WHERE productID=?", (productID,))
         connection.commit()
         print("Product removed successfully.")
         
def update_product(self, productID, name, price, quantity):
         cursorDb.execute("UPDATE Product SET name=?, price=?, quantity=? WHERE productID=?",
                          (name, price, quantity, productID))
         connection.commit()
         print("Product updated.")
         
def display_product(self):
         cursorDb.execute("SELECT * FROM Product")
         products = cursorDb.fetchall()
         for prod in products:
             print(f"ID: {prod[0]} / Name: {prod[1]} / Price: {prod[2]} / Quantity: {prod[3]}")
    
def sell_product(self, salesID, quantity, date):
         cursorDb.execute("SELECT name, price, quantity FROM Product WHERE productID=?", (salesID,))
         product = cursorDb.fetchone()
         if product and product[2] >= quantity:
             total = product[1] * quantity
             cursorDb.execute("UPDATE Product SET quantity=? WHERE productID=?", (product[2] - quantity, salesID))
             cursorDb.execute("INSERT INTO Sales(date, product_name, total) VALUES(?,?,?)", (date, product[0], total))
             connection.commit()
             print("Sale has been recorded")
         else:
             print("Low stock")
            
def display_sales(self):
          cursorDb.execute("SELECT * FROM Sales")
          sales = cursorDb.fetchall()
          for sales in sellProduct:
              print(f"salesID: {sales[0]} / Date: {sales[1]} / Product: {sales[2]} / Total: R{sales[3]}")
              
if __name__ == "__main__":
   mainMenu()
   

             
         
       
              
              
        
    
    
