import atexit
import os
import sqlite3


from dbtools import Dao, orm


class Employee(object):
    def __init__(self, id, name,salary, coffee_stand):
        self.id=id
        self.name=name
        self.salary=salary
        self.coffee_stand=coffee_stand
    def __str__(self):
        return  "("+str(self.id) + ", '"+ self.name +"', "+ str(self.salary) + ", " +str(self.coffee_stand) +")"



class Supplier(object):
    def __init__(self,id,name,contact_information):
        self.id=id
        self.name=name
        self.contact_information=contact_information

    def __str__(self):
        return "("+str(self.id)+ ", '"+ self.name + "', '"+ self.contact_information[0:len(self.contact_information)-1] + "')"




class Product(object):
    def __init__(self,id,description,price,quantity):
        self.id=id
        self.description=description
        self.price=price
        self.quantity=quantity
    def __str__(self):
        return "("+str(self.id)+ ", '"+ self.description + "', "+ str(self.price) + ", " +str(self.quantity) + ")"



class Coffee_stand(object):
    def __init__(self,id,location,number_of_employees):
        self.id=id
        self.location=location
        self.number_of_employees=number_of_employees

    def __str__(self):
        return  "("+str(self.id) + ", '" + self.location + "', " + str(self.number_of_employees) + ")"


class Activitie(object):
    def __init__(self,product_id,quantity,activator_id,date):
        self.product_id=product_id
        self.quantity=quantity
        self.activator_id=activator_id
        self.date=date
    def __str__(self):
        return  "(" + str(self.product_id) + ", " + str(self.quantity) + ", " + str(self.activator_id) + ", "+ str(self.date) + ")"



class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('moncafe.db')
        self.cursor = self._conn.cursor()
        self.Employees = Dao(Employee, self._conn)
        self.Suppliers = Dao(Supplier, self._conn)
        self.Products = Dao(Product, self._conn)
        self.Coffee_stands = Dao(Coffee_stand, self._conn)
        self.Activities = Dao(Activitie, self._conn)



    def _close(self):
        self._conn.commit()
#        self._conn.close()

    def create_tables(self):
        cursor = self._conn.cursor()
        cursor.execute(
            """CREATE TABLE Products(id INTEGER, description TEXT NOT NULL, price REAL NOT NULL, 
            quantity INTEGER NOT NULL, PRIMARY KEY(id))""")
        cursor.execute(
            """ CREATE TABLE Suppliers(id INTEGER UNIQUE , name TEXT NOT NULL, contact_information TEXT, PRIMARY KEY(id))
            """)
        cursor.execute(
            """CREATE TABLE Activities(product_id INTEGER, quantity INTEGER NOT NULL, 
            activator_id INTEGER NOT NULL, 
            date DATE NOT NULL, FOREIGN KEY(product_id) REFERENCES Product(id), FOREIGN KEY(activator_id) REFERENCES Employees(id))""")

        cursor.execute(
            """CREATE TABLE Employees(id INTEGER UNIQUE , name TEXT NOT NULL, salary REAL NOT NULL, coffee_stand 
            INTEGER, 
            PRIMARY KEY(id),
            FOREIGN KEY(coffee_stand) REFERENCES Coffee_stand(id))""")

        cursor.execute(
            """ CREATE TABLE Coffee_stands(id INTEGER , location TEXT NOT NULL, number_of_employees INTEGER, PRIMARY KEY(id))""")

    def actReport(self):
        c = self._conn.cursor()
        c.execute('SELECT act.date, prod.description, act.quantity, emp.name, supp.name'
                  ' FROM Activities as act '
                  'JOIN Products as prod on prod.id=act.product_id '
                  'LEFT JOIN Suppliers as supp on supp.id=act.activator_id '
                  'LEFT JOIN Employees as emp on emp.id=act.activator_id '
                  'ORDER BY act.date')
        return c.fetchall()


repo = Repository()
atexit.register(repo._close)