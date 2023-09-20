import sqlite3
from contextlib import closing

# connect to the database and set the row factory
def connect_db(path):
    
    connection = sqlite3.connect('Sales.db')
    connection.row_factory = sqlite3.Row
    return connection
def view_orders_summary_by_country(connection):
    c = connection.cursor()
    c.execute('''select Country, count(OrderID) as TotalNumberOfOrders, sum(Amount) as TotalOfOrderAmount,
        avg(Amount) as OrderAverage from Orders group by Country''')
    summary = c.fetchall();
    c.close()
    return summary

def view_orders_by_date(connection):
    date = input("Date of orders: " )
    c = connection.cursor()
    c.execute('''select * from Orders where OrderDate = ?''',(date,))
    summary = c.fetchall();
    c.close()
    return summary
        
def view_orders_by_salesperson(connection):
    sp = input("Name of sales person: " )
    c = connection.cursor()
    c.execute('''select * from Orders where Salesperson = ?''',(sp,))
    summary = c.fetchall();
    c.close()
    return summary

def view_orders_by_salesperson_date(connection):
    sp = input("Name of sales person: " )#.split()
    date = input("Date of orders: ")
    c = connection.cursor()
    c.execute('''select * from Orders where Salesperson = ? and OrderDate = ?''',(sp, date,))
    summary = c.fetchall();
    c.close()
    return summary

        
def view_orders_by_amount(connection):
    minNum1 = input("Minimum of order amount: " )#.split()
    maxNum2 = input("Maximum of order amount:" )
    c = connection.cursor()
    c.execute('''select * from Orders where Amount between ? and ?''',(minNum1, maxNum2,))
    summary = c.fetchall();
    c.close()
    return summary



###########################

def update_orders(connection):
    c = connection.cursor()
    print("Update order amount by entering sales person's name AND range of order amount:")
    sp = input("--> Enter sale person's name: ")
    minNum1 = int(input("--> Enter minimum of order amount: "))
    maxNum2 = int(input("--> Enter maximum of order amount: "))
    
   
    c.execute('''select * from Orders where Salesperson = ? and Amount between ? and ?''',(sp, minNum1, maxNum2,))
   
    orders1 = c.fetchall();
    #display_orders(orders1)


    if len(orders1) > 0:
        count = 1
        for order in orders1:
            print(str(count) + " -", order["Country"], "|", order["Salesperson"], "|", \
                  order["OrderID"], "|", order["OrderDate"], "|", "${:,.2f}".format(order["Amount"]))
            #updateNum = int(input("--> How much to update (e.g.,+25,-100,etc.)? "))
            count += 1
            
    
    else:
        print("No orders....")
    print()

    updateNum = int(input("--> How much to update (e.g.,+25,-100,etc.)? "))
    newMin = minNum1 + updateNum
    newMax = maxNum2 + updateNum
    
    c.execute('''update Orders set Amount = Amount + ? where Salesperson = ? and Amount between ? and ?''', (updateNum,sp,minNum1,maxNum2,))
    print("Updated.....")
    connection.commit()
    c.close()
    
    c2 = connection.cursor()
    c2.execute('''select * from Orders where Salesperson = ? and Amount between ? and ?''',(sp, newMin, newMax,))
    orders2 = c2.fetchall();
    if len(orders2) > 0:
        count = 1
        for order in orders2:
            print(str(count) + " -", order["Country"], "|", order["Salesperson"], "|", \
                  order["OrderID"], "|", order["OrderDate"], "|", "${:,.2f}".format(order["Amount"]))
            count += 1
    else:
        print("No orders....")
    print()


    orders2 = c2.fetchall()




    
    c2.close()
    #return orders1

 #########   

def display_menu():
    print("COMMAND MENU")
    print("c - View order summary of a given country")    
    print("d - View order details of a given date")
    print("s - View order details of a given sales person")
    print("sd - View order details of a given sales person and date")
    print("a - View order details of a given range of amounts")
    print("u - Update order amount of a sales person's orders")
    print("m - Display command menu")    
    print("e - Exit program")
    print()    

def display_summary(summary):
    for line in summary:
            print(line["Country"], "|", line["TotalNumberOfOrders"], "orders |", \
                      "${:,.2f}".format(line["TotalOfOrderAmount"]), "in total |", "average is ${:,.2f} per order".format(line["OrderAverage"]))
    print()
    
def display_orders(orders):
    if len(orders) > 0:
        count = 1
        for order in orders:
            print(str(count) + " -", order["Country"], "|", order["Salesperson"], "|", \
                  order["OrderID"], "|", order["OrderDate"], "|", "${:,.2f}".format(order["Amount"]))
            count += 1
    else:
        print("No orders....")
    print()


def main():
    print("Sales Orders Program")
    print()

    conn = connect_db("Sales.db")
   
    display_menu()    
    while True:
        command = input("Command: ")
        if command == "c":
            result = view_orders_summary_by_country(conn)
            display_summary(result)
        elif command == "d":
            result = view_orders_by_date(conn)
            display_orders(result)
        elif command == "s":
            result = view_orders_by_salesperson(conn)
            display_orders(result)
        elif command == "sd":
            result = view_orders_by_salesperson_date(conn)
            display_orders(result)
        elif command == "a":
            result = view_orders_by_amount(conn)
            display_orders(result)
        elif command == "u":
            update_orders(conn)
        elif command == "m":
            display_menu()
        elif command == "e":
            break
        else:
            print("Not a valid command. Please try again.\n")
    print("Bye!")

if __name__ == "__main__":
    main()
