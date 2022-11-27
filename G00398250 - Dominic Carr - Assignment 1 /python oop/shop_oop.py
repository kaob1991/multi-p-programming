# import packages 
import csv
import os
import sys

#Creating classes for the individual elements in the shop. 

#Product class- name and price of each item
class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    # Define a repr method- this returns a string 
    def __repr__(self):
        return f'Product Name: {self.name}; Product Price: {self.price}; '

# Product Stock class - product from class above and quantity of each item 
# Within this class the variables name, unit price, quantity and cost(unit price x quantity) are also defined

class ProductStock:
    
    def __init__(self, product, quantity):
        #product is a class 
        self.product = product
        #quantity is a floating point number
        self.quantity = quantity
    # get product name
    def name(self):
        return self.product.name
    # get product price
    def unit_price(self):
        return self.product.price
    # calculate cost   
    def cost(self):
        return self.unit_price() * self.quantity
    # get quantity of stock item
    def get_quantity(self):
        return self.quantity

    #{sample}
    # updates the quantity of a product for each quantity of stock sold
    def set_quantity(self, saleQty):
        self.quantity -= saleQty

    def get_product(self):
        return self
        
    def __repr__(self):
        return f"{self.product} has {self.quantity} in stock"



# Customer class- takes in details from a csv file and provides name and budget from row 1 of file
# Then iterates over the csv file to fill a shopping list variable 




class Customer:

    def __init__(self):
        self.shopping_list = []
        self.filename= input("Please enter the name of the customer file: ")
        self.status = True
        
        path = "../" + str(self.filename) + ".csv"

        while self.status:   
            try:
                with open(path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    first_row = next(csv_reader)
                    self.name = first_row[0]
                    self.budget = float(first_row[1])
                    for row in csv_reader:
                        name = row[0]
                        quantity = float(row[1])
                        p = Product(name)
                        ps = ProductStock(p, quantity)
                        self.shopping_list.append(ps)
                    return
                    
            # in case invalid csv file entered
            except Exception as err:
                    print("Invalid customer file name. ") 
                    # should return to the menu here same as pp versions
                    self.status=False

                    return
                    #sys.exit()
      # a method to calculate customer costs   
    def calculate_costs(self, price_list):
            # each shop_item is a productStock
        for shop_item in price_list:
            # iterate through the customer shopping list 
            for list_item in self.shopping_list:
                # check if the item name matches a shop item
                if (list_item.name() == shop_item.name()):
                    # if so pull out the price
                    list_item.product.price = shop_item.unit_price()


      # a method for calculating item cost
    def order_cost(self):
        cost = 0
        # going through the customer shopping list of productStocks  and getting out the cost
        for list_item in self.shopping_list:
            # get the cost using the ProductStock cost method
            cost += list_item.cost()
        return cost

   
  
# A repr method returns a state based representation of the class 
    def __repr__(self):
        print(f'Customer Name: {self.name} \nCustomer Budget: €{self.budget}')

        # just print the actual customer order from the file first
        for item in self.shopping_list:
            print(item.product)
            print(f"{self.name} orders {item.quantity} of above item ")
        # now printing the product with price if we stock the item only
        print("We have the following items in stock:")   
        str = ""
        for item in self.shopping_list:
            price = item.product.price
            # don't print for items we don't stock
            if price !=0:
                str += f"{item.quantity} units of {item.name()} at €{price} per unit which will cost €{item.cost()}\n\n"
            # {DC}
          # print statement saying how much the customer would have left 
          # str += f"\nThe cost would be: {self.order_cost()}, he would have {self.budget - self.order_cost()} left"
             
        return str 

# create a subclass of customer so the live customer can use all the customer functionality
class Live(Customer):
    def __init__(self):
        self.shopping_list=[]
        self.name = input("Please enter your name: ")
        print(f"Welcome to the shop {self.name}")
# loop here to try and add more items to shopping list? 
        while True:
            try:
                self.budget = float(input("Please enter your budget:"))
                break
            except ValueError:
                print("Please enter your budget as a number!")
        product = input("Please enter the product you are looking for: (Please note product name is case sensitive.)")

        # capture inappropiate values
        while True:
            try:
                quantity = int(input(f"Please enter the quantity of {product} you are looking for: "))
                break

            except ValueError:
                print("Please enter the quantity as an integer")
        
        p = Product(product)
        ps = ProductStock(p, quantity)
        self.shopping_list.append(ps)


    

                


# Shop class creates a stock variable and takes in details about the shop from a csv file.
# The first row of the csv file contains the shops available float and the remainder of the file has the shops contents to fill
# The Product Stock and Product instances of the classes






        
class Shop:


    

    #{DC}
    def __init__(self, path):
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
    #{DC}
    def __repr__(self):
        str = ""
        str += f'Shop has €{self.cash} in cash\n'
        # loop over the stock items, each item is class ProductStock
        for item in self.stock:
            str += f"{item}\n"
        return str      

    # {Sample}
    ### def process_order, takes in a customer 
    def process_order(self,c):
        print("PROCESSING ORDER...")
        print("-------------------")
        self.totalProductCost = 0 

        for  list_item in c.shopping_list:
            # call the method to check stock
            self.check_stock(list_item)
            # call the method to update cash or not
            self.update_cash(c)
            # call method to update stock based on quantities in stock as checked by check_stock method
            self.update_stock(self.product)
        print("UPDATING CASH\n-------------------")
        print(f"Customer ({c.name}) has €{c.budget} left")


    # a method to update the cash of the shop and the customer if the customer has the ability to pay         
    def update_cash(self,c):
        # a boolean used by the method to update stock or not. Stock only updated if customer can pay
        self.process = False
        # checking ability of customer to pay, then update the shop cash and customer cash if they can
        if c.budget >= self.totalProductCost:
            self.cash += self.totalProductCost
            c.budget -= self.totalProductCost
            # only print for actual sale quantities
            if self.saleQty>0:
                print(f"€{self.totalProductCost} deducted from the customer's funds for: {self.saleQty} unit(s) of {self.product.name()}.\n")
            # to indicate to the update stock method that the stock should be updated to reflect sale          
            self.process = True
            # if customer cannot pay, then sale does not go ahead. 
        elif c.budget < self.totalProductCost:
            print(f"Insufficient funds, Customer has €{c.budget} but €{self.totalProductCost} required for {self.saleQty} unit(s) of {self.product_name}\n")
           
    # a method to check stock, compare customer items to shop stock items
    def check_stock(self,list_item):
        # checking the stock
        for shop_item in self.stock:
            # if the shop does stock the customer item
            if (list_item.name() == shop_item.name()): 
                # assign the 
                self.product_name = shop_item.name()
                #get the product stock details and return the product for the update stock method to use
                self.product = shop_item.get_product()
                # checking if there is enough stock 
                if list_item.quantity <= shop_item.quantity:
                    # total product cost based on quantity customer wants as we have enough
                    self.totalProductCost = list_item.quantity *shop_item.product.price
                    # store the sale quantity for use later
                    self.saleQty = list_item.quantity
                    return self.totalProductCost, self.product, self.saleQty, self.product_name
                    
                # checking if the customer order quantity is more than we have in stock
                elif (list_item.quantity > shop_item.quantity):
                    print(f"Unfortunately, we only have {shop_item.quantity} of {shop_item.name()} at the moment. You will be charged only for the products sold.\n")
                    # total product cost is based on partial order if thats all that is available
                    self.totalProductCost = shop_item.quantity *shop_item.product.price
                    self.saleQty = shop_item.quantity
                    return self.totalProductCost, self.product, self.saleQty, self.product_name
            # if the customer product is not stocked, sale quantity is zero and no cost to customer. Avoid printing out later
            if (list_item.name() != shop_item.name()):
                self.product = list_item
                self.saleQty =0
                self.totalProductCost =0
                
    # a method to update stock
    def update_stock(self, product):
        # only update stock if the customer can pay, otherwise a sale does not take place
        if self.process == True:
            # call ProductStock methods to update the quantity in stock
            product.set_quantity(self.saleQty)
            

    def display_menu(self):
        while True:
    # clear the screen of previous input
    #clear()
            
            print("Select 1 for Shop Overview")
            print("Select 2 for Batch orders")
            print("Select 3 for Live orders")
            print("Select 0 to Exit Shop Application")

            self.choice = input("Please choose an option from the main menu: ")
            if (self.choice =="1"):
                print("1: Shop Overview")
                
                print(self)
                self.return_to_menu()

            elif (self.choice =="2"):    
                    
                print("2: Bstch Orders")
                # create a customer object 
                c = Customer()
                if c.status == False:
                    self.return_to_menu()

                # call calculate method on the customer with shop stock as input
                c.calculate_costs(self.stock)
                # print the customer
                print(c)
                # process the order using customer object as input
                self.process_order(c)
                self.return_to_menu()

            elif (self.choice=="3"):            
                print("3: Live Orders")
                # create a customer object by calling the live class
                c = Live()
                # call calculate method on the live customer object with shop stock as input
                c.calculate_costs(self.stock)
                print(c)
                # process the order with the customer object as input
                self.process_order(c)
                self.return_to_menu()


            elif(self.choice =="0"):
                print("\nThank you for shopping here. Goodbye")
                # to exit straight out of the program as this is part of the shop class
                # break
                sys.exit()
            
            else:
                print("Please choose an option from the menu above.")
                self.display_menu()
                
    # a method to return to menu
    def return_to_menu(self):
        menu = input("Press any key to return to main menu ")
        if True:
            self.display_menu()

def clear_screen():
    os.system('clear')   

# the main method just creates a shop object 
def main():
    print("Main Menu: ")
    s = Shop("../stock.csv")
    s.display_menu()
        
if __name__ == "__main__":
    # clear the screen
    clear_screen()
    # call the main method
    main()

