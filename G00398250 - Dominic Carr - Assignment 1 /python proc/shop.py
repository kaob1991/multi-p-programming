# import libraries needed

from dataclasses import dataclass, field
from typing import List
import csv
import os

# Create classes required for shop to work correctly

# class for products
##{DC}
@dataclass
class Product:
    name: str
    price: float = 0.0

# class for product stock 
# {DC}
@dataclass 
class ProductStock:
    product: Product
    quantity: int

# Class for shop
# {DC}
@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

# Class for customer
# {DC}
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)


# Clear the screen
def clear_screen():
    os.system('clear')



# Defining a function to create and stock the shop
# {DC}

def create_and_stock_shop():
    s = Shop()
    # Shop is a class that contains cash (the float; as FP no.) and stock (the list from class ProductStock)
    # Reading in a stock csv file; the shop cash is contained in the first row
    with open("../stock.csv", mode = "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        # iterates through the rows of the csv file, creating Product, ProductStock, and Shop stock
        # using the data classes defined above
        for row in csv_reader:
            # Product
            p = Product(row[0], float(row[1]))
            # ProductStock
            ps = ProductStock(p, float(row[2]))
            # Appending product stock to shop stock 
            s.stock.append(ps)
            # Return the shop 
    return s






# Create customer using function 
#{DC}
def read_customer():
    path = input("Please upload your customer file name...")
    # create a file name including the file path
    path = "../" + str(path) + ".csv"
    try:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            # customer name and budget are the first row
            c = Customer(first_row[0], float(first_row[1]))
            # After the first row, the remainder of the file is the customers shopping list
            # Add the data from the file to the Customer class Shopping list
            for row in csv_reader:
                # Product name is first column
                name = row[0]
                # Quantity is the 2nd column
                quantity = float(row[1])
                # Product is a class with 2 variables, of type str(name) and float(price)
                p = Product(name)
                # Product stock adds quantity to the product
                ps = ProductStock(p, quantity)
                c.shopping_list.append(ps)
            return c 



    except Exception as err:
        print("Invalid customer file name. ")
        # return the user to the menu
        return_to_menu()
        


        
# Takes in a product and prints out the price
# {DC}
def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

# This function prints the cash in shop and the number of items and quantity of each item
#{DC}
def print_shop(s):
    print(f'Shop has {s.cash} in cash')
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')
        print ("********************************")



# Define a return to menu 
# {sample}
def return_to_menu():
    menu = input("\n Hit any key to return to main menu")
    if True:
        display_menu()


# a function to display the menu options 
# {sample}      
def display_menu():
    # clear the screen of previous input
    clear_screen()
    print("DISPLAY MENU")
    print("***************************")
    print("Select 1 for an Overview")
    print("Select 2 for Batch orders")
    print("Select 3 for Live orders")
    print("Select 0 to Exit Shop")




# Processing the order
# {sample}
def process_order(c,s):  
    print("Processing order...")
    print("*******************")
    # create variable for total product cost
    totalProductCost = 0 
    # go through each item in customer shopping list
    for item in c.shopping_list:
        # check against each item in shops stock
        for prod in s.stock:
            # if the item is a shop stock item
            if item.product.name == prod.product.name:
                # check if the quantity in stock is enough to fill the order
                if prod.quantity >= item.quantity:
                    # calculate cost
                    totalProductCost = item.quantity * prod.product.price
                    # check if the customer has enough cash to cover the cost of this purchase
                    if c.budget >= totalProductCost:
                        # process sale, update shop cash
                        s.cash += totalProductCost
                        # process sale, update customer cash
                        c.budget -= totalProductCost
                        # process sale, decrease stock quantity of sold items
                        print(f"€{totalProductCost} deducted from the customer funds for {item.quantity} of {item.product.name}.\n")
                        prod.quantity -= item.quantity
                        print ("Shop updated")

                    elif c.budget < totalProductCost:
                        print(f"You have insufficient funds, you only have €{c.budget} but you need €{totalProductCost} to pay for {item.product.name}")
                        # no purchase takes place, pass
                        c.budget -=0
                
                # if quantity in stock is less than what the customer wants
                elif (prod.quantity < item.quantity):
                    print(f"We only have {prod.quantity} of {prod.product.name} at the moment. You will be charged only for the products sold.\n");
                    # calculate cost based on partial order 
                    totalProductCost = prod.quantity * prod.product.price
                    # check if customer has enough cash to pay
                    if c.budget >= totalProductCost:
                        print(f"€{totalProductCost} deducted from the customer funds for {prod.quantity} unit(s) of {item.product.name}.\n")                 
                        # process sale, decrease stock
                        prod.quantity -= prod.quantity
                        # process sale, increase shop cash as a result of sale
                        s.cash += totalProductCost
                        # deduct sale amount for this item from customer wallet
                        c.budget -= totalProductCost  
                    # if customer does not have enough to pay        
                    elif c.budget < totalProductCost:
                        print(f"Insufficient funds, Customer has €{c.budget} but €{totalProductCost} required for {item.product.name}\n")
                        # no purchase takes place, pass
                        c.budget -=0
    print(f"Customer {c.name} now has €{c.budget} left.")



 # takes in a customer which is read in from the csv file 
def print_customer(c,s):
    
    # print customer details
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    print("**************")
    # goes through the customer's shopping list and calls the print_product function to print the product name and price
    print("CUSTOMER ORDER:")
    orderCost =[]
    # loop through items on customer shopping list
    for item in c.shopping_list:
        # loop through items in shop stock
        print_product(item.product)

        print(f"{c.name} ORDERS  {item.quantity} OF ABOVE PRODUCT\n")
        print("***********************************")

    print("Please wait while we check our stock...")
    print("*****************************************")
    print("We have the following items in stock:")
    for item in c.shopping_list:
        for prod in s.stock:
            # comparing items to see if we have the item in stock
            if item.product.name == prod.product.name:
                cost = item.quantity * prod.product.price
                orderCost.append(cost)
                print(f"{item.quantity} units of {item.product.name} at €{prod.product.price} per unit for cost of €{item.quantity *prod.product.price }")



def live_order(s):
    # intialise an array to hold the shopping list
    shopping_list = []
    c=Customer()
    
    c.name = input("Please enter your name: ")
    print(f"Welcome to the shop.{c.name}")
    while True:
        try:
            # asks customer for their budget
            c.budget = float(input("please enter your budget: €"))
            break
        # in case a float is not entered
        except ValueError:
            print("Please enter your budget as a floating number")
    # get product name from customer and store as a Product 
    product  = input("Please enter the name of the product you are looking for. Please note product name is case sensitive\t\t")
    p = Product(product)

    # ask customer for quantity of item, ensure an integer is accepted
    while True:
        try:
            quantity = int(input(f"Please enter the quantity of {product} you are looking for \t\t"))
            break
        # in case an integer is not entered
        except ValueError:
            print("Please enter the quantity as an integer")
    # create a ProductStock using the product and quantity
    ps = ProductStock(p, quantity)    
    print("Please wait while we check")
    # append the items to the customers shopping list
    c.shopping_list.append(ps)
    # return a customer
    return c
'''
# a function to clear the screen for readability
def clear():
    os.system('clear')

'''


def main():
    # clear screen
    clear_screen()
    print("Setting up the shop for today ...")
    # create the shop by calling this function
    s = create_and_stock_shop()
 
    # a forever loop 
    while True:
        # display the user menu
        display_menu()
        # store input as choice
        choice = input("\n Please select option from the main menu:")

        # if option 1 selected, print the current shop state by calling print_shop
        if (choice =="1"):
            print("1: SHOP OVERVIEW")
            print_shop(s)
            return_to_menu()    

        # if option 2 selected, ask user for their customer file
        elif (choice =="2"):    
            
            print("2: BATCH ORDERS")
            # create customer 
            c = read_customer()
            # if a customer has been created, print their order
            if c:
                print_customer(c,s)
                # process the customers order
                process_order(c,s)

            return_to_menu() 

        # if option 3 chosen, create customer by calling the live_order function   
        elif (choice=="3"):            
            print("3:*** LIVE MODE ***")
            print("Please choose from our products listed below")
            print_shop(s)
            c =live_order(s)
            # print customer details
            print_customer(c,s)
            # process the customers order
            process_order(c,s)

            # return to menu
            return_to_menu() 

        # if user selects 0, this signals they wish to exit the program
        elif (choice == "0"):
            # exit clause to break out out of the entire program and back to the command prompt
            print("\nThank you for shopping here. Goodbye.")
            break

    ## for anything else, display the menu
        else: 
            display_menu()

if __name__ == "__main__":
    # only execute if run as a script

    # call the main function above
    main()



        


