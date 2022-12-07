#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h> // for checking file exists

// a data structure for Product holding name and price variables
struct Product {
	char* name;
	double price;
};
// a data structure for ProductStock holding quantity and Product variables
struct ProductStock {
	struct Product product;
	int quantity;
};
// a data structure for Shop holding cash, and ProductStock.
struct Shop {
	double cash;
	struct ProductStock stock[20];
	int index;
};
// a data structure for Customer
struct Customer {
	char* name;
	double budget;
	struct ProductStock shoppingList[10];
	int index;
};

// a procedure to print the product 
void printProduct(struct Product p)
{
	printf("PRODUCT NAME: %s \nPRODUCT PRICE: %.2f\n", p.name, p.price);	
}

/// check if file name exists  see  https://www.zentut.com/c-tutorial/c-file-exists/
// instead of reading data from the file, read files attributes using stat() function
int cfileexists(const char* filename){
    //
    struct stat buffer;
    int exist = stat(filename,&buffer);
    // stat() returns 0 if operation was successful,
    if(exist == 0)
        return 1;
    else // -1
        return 0;
}

//struct to create and stock the shop from the stock csv file
struct Shop createAndStockShop()
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("../stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

	read = getline(&line, &len, fp);
	float cash = atof(line);
	//printf("cash in shop is %.2f\n", cash);
	
	struct Shop shop = { cash };

    while ((read = getline(&line, &len, fp)) != -1) {
        //string tokenise to get the name, price and quantity from each line of the csv 
        //printf("%s IS A LINE", line);
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");
        // convert to integer (atoi) and float (atof)
		int quantity = atoi(q);
		double price = atof(p);
        // allocate enough memory for name of product
		char *name = malloc(sizeof(char) * 50);
        // copy the name from n into name
		strcpy(name, n);
        //create a Product struct using name and price
		struct Product product = { name, price };
        //create a ProductStock struct  using product struct and quantity
		struct ProductStock stockItem = { product, quantity };
        // increment index for next item
		shop.stock[shop.index++] = stockItem;
		// printf("NAME OF PRODUCT %s PRICE %.2f QUANTITY %d\n", name, price, quantity);
    }
	// return a shop struct containing the cash and stock items and quantities
	return shop;
}

// void printShop(struct Shop s) updated this to get updated cash and stock using pointers
void printShop(struct Shop *s)
{
	printf("Shop has €%.2f in cash\n", s->cash);
	for (int i = 0; i < s->index; i++)
	{   //call the print product method for each item in the shop using pointers to get the current states
		printProduct(s->stock[i].product);
		printf("The shop has %d in stock.\n", s->stock[i].quantity);
        printf("-------------\n");
	}
}

// DISPLAY MENU
void displayMenu()
{
	fflush(stdin); 
    printf("\n\n");   
    printf("\n\t\tWelcome to our humble little shop\n\n");
    printf("\t\t----------------------------------\n");
    printf("\t\tSelect 1 for Shop Overview\n");
    printf("\t\tSelect 2 for Batch order\n");
    printf("\t\tSelect 3 for Live orders\n");
    printf("\t\tSelect 0 to Exit Shop Application\n\n\n");	
}

// a procedure to give the option to see the display menu again, keeping screen clutter free
void returnToMenu(){
    fflush(stdin); 
    char menu;   
    printf("\n Hit any key to return to main menu ");
    scanf("%c", &menu);
    if (menu){
        displayMenu();
    }
}

// clearing the screen, using empty lines
void clearScreen ( void )
    {
      for ( int i = 0; i < 25; i++ ) 
        printf("\n");
    }

/// read in customer from csv file
struct Customer readCustomer()
{   
    FILE * fp;
    //allocate enough memory for filename
    char *filename = malloc(sizeof(char) * 20);  
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    printf("Please enter the name of your customer file: ");
    scanf("%s", filename);
    
    // https://www.linuxquestions.org/questions/programming-9/prepending-to-a-string-in-c-619093/
    strcat(filename, ".csv");
    char filepath[40] = "../";
    // adding the path ../ before the filename
    strcat(filepath, filename);
    //printf("Attempting to cat path to fielname %s",filepath);

    // instead of checking if the filename exists, check if the filename with file path exists
    int exist = cfileexists(filepath);
    if(exist)
    {
    //printf("File %s exist\n",filepath);
    FILE * fp;
    fp=fopen(filepath, "r"); 

// the first line has the customer name and budget
    read = getline(&line, &len, fp);
    // read the first line, break into 2 pieces using the tokeniser, customer name, customer budget
    char *n = strtok(line, ","); 
    char *b = strtok(NULL, ","); 
    char *name = malloc(sizeof(char) * 100);
    // avoid overwriting name each time by strtok
    strcpy(name, n);
    double budget = atof(b); // make it a double
    //create a customer struct 
    struct Customer customer = {name, budget}; 

    // add while loop to read rest of csv file
    while ((read = getline(&line, &len, fp)) != -1) {
        // need to strcpy for product name to stop it being overwritten when using strtok
        // product name n, quantity q on each line after line 1
        char *n = strtok(line, ","); 
        char *q = strtok(NULL, ","); 
        int quantity = atoi(q); // convert to integer
        // dynamically allocate new memory for storing the product name
        char *pname = malloc(sizeof(char) * 20); 
        // strcpy from pname to p to pname to avoid it being overwritten during the while loop
		strcpy(pname, n);
        // create a Product Struct and ProductStock struct for each item on shopping list
        struct Product product = { pname }; 
        struct ProductStock custItem = { product, quantity };
        //increment index
        customer.shoppingList[customer.index++] = custItem;
    }
    // return customer struct
    return customer;
    }
    // in case the file doesn't exist, create a customer struct with budget of zero as need to return a customer
    else{
        printf("That file %s is not valid\n",filename); 
        char *name = "";
        int budget=0;
        struct Customer customer = {name, budget};
        return customer;
        returnToMenu();
    }
    // this would exit the program completely but need to be the same as other versions
    //exit(EXIT_FAILURE);        
}

//// print customer details and their shopping list
    void printCustomer(struct Customer *cust, struct Shop *shop){
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f\n", cust->name, cust->budget);
	printf("-------------\n");
    // loop through items on customer shopping list
    for(int i = 0; i < cust->index; i++){
        printProduct(cust->shoppingList[i].product);
		printf("%s ORDERS %d OF ABOVE PRODUCT\n\n", cust->name, cust->shoppingList[i].quantity);
        printf("*************************\n");
    }

    printf("Please wait while we check our stock...\n\n");
    printf("-----------------------------------------\n");
    printf("We have the following items in stock:\n\n");
    for(int i = 0; i < cust->index; i++){
    // get customer product from the shopping list
        char *custProduct = cust->shoppingList[i].product.name;
        // product price on customer shopping list is initially zero
        double custProductPrice = cust->shoppingList[i].product.price;
        // loop through shop stock items
        for (int j=0; j< shop->index; j++){
            // get the shop product name and product price 
            char *shopProduct = shop->stock[j].product.name;
            double shopProductPrice = shop->stock[j].product.price;
            // compare customer products to shop products, if there is a product match update the price on customer shopping list
            if (strcmp (custProduct, shopProduct)==0){
                custProductPrice = shopProductPrice;
                // print the cost, customer quantity times shop price
                printf("%d units of %s at €%.2f per unit  for cost of €%.2f \n\n",cust->shoppingList[i].quantity,custProduct,  shopProductPrice, cust->shoppingList[i].quantity* shopProductPrice );
                } 
            } 
        } 
}
// a struct for a live customer
struct Customer liveCustomer()

{
	printf("Welcome to live shop mode \n");
    // for product name
    char *productName = (char*) malloc(10 * sizeof(char));
    // for product quantity
    char *pq = (char*) malloc(3 * sizeof(char)); 
    // memory for customer name
    char *custName = malloc(sizeof(char)*30);
    char *b = (char*) malloc(10 * sizeof(char)); 
    // read in customer name, budget
    printf("Please enter your name:\t");
    scanf("%s", custName);
    printf("Welcome to the shop %s\n",custName);
    printf("Please enter your budget:\t");
    scanf("%s",b);
    // make budget a double      
    double budget = atof(b);
    printf("Your budget is %lf\n",budget);
    // create customer struct with customer name and budget
    struct Customer customer = {custName, budget};
    // if budget not entered or entered incorrectly
    if (budget ==0)
            {
            printf("Please enter your budget as a number.\n");
            returnToMenu();
            }
    else {
            printf("Please enter the name of the product you are looking for. Please note product name is case sensitive.\t\t");
            scanf("%s", productName);
            printf("Please enter the quantity of %s that you are looking for \n ",productName);
            struct Product product = { productName };
            scanf("%s",pq);
            int productQuantity = atoi(pq); 
            printf("You are looking for %d of %s\n",productQuantity, productName);
            struct ProductStock custItem = { product, productQuantity };
            // create customer shopping list
            customer.shoppingList[customer.index++] = custItem;
            // if quantity not entered or not entered as an integer            
            if (productQuantity ==0)
            {
            printf("Please enter a quantity as an integer\n");
            returnToMenu();
            }
        }
    return customer;
}

// A struct for processing the order by the shop
    struct Shop processingOrder(struct Shop *shop, struct Customer *cust){
    printf("PROCESSING ORDER...\n");
    printf("-------------------\n");
    // using pointer to get the current shop cash
    double openingcash = 0;
    openingcash = shop->cash;
    // using pointer to get customer budget
    double openingWallet = cust->budget;
    //total cost to customer
    double totalCost = 0;
    // loop through the customer shopping list
    for (int i=0; i<cust->index; i++){
        // true false flag
        //int check = 0;
        // assign memory for customer item
        char *custItem = malloc(sizeof(char)*30);
        // copy the customer product on shopping list into custItem
        strcpy(custItem, cust->shoppingList[i].product.name); 
        // loop through the shop stock list
        for (int j=0; j< shop->index; j++){
            char *shopItem = malloc(sizeof(char)*30);
            // copy the products from the stock into shopItem to compare with customers item
            strcpy(shopItem, shop->stock[j].product.name); 
           // compare customer shopping list items to stock items
            if(strcmp(custItem, shopItem)==0){
                // set the stock flag to 1
                //check = 1;
                // get product quantity from customer shopping list using pointer
                int custQty = cust->shoppingList[i].quantity;
                // get current quantity of item in shop using pointer
                int shopQty = shop->stock[j].quantity;
                // get stock price
                double price = shop->stock[j].product.price;
                // to store the total product cost
                double totalProductCost = 0;
                // if enough stock of item in shop
                if (shopQty>= custQty){
                    // calculate total product cost
                    totalProductCost = price * custQty;
                    // adding  a customer cash  balance check here 
                    if (cust->budget >= totalProductCost){
                        // update shop cash if customer has enough to pay
                        shop->cash += totalProductCost;
                        // update customer cash
                        cust->budget -= totalProductCost;
                        // update shop stock to reflect sale of goods
                        printf("€%.2f deducted from the customer funds for %d unit(s) of %s.\n\n", totalProductCost, custQty, custItem);
                        shop->stock[j].quantity = shop->stock[j].quantity - custQty;
                    } 
                    // if customer does not have enough to pay, print message
                    else if((cust->budget < totalProductCost)){
                        //print(f"You have insufficient funds, you only have €{c.budget} but you need €{totalProductCost} to pay for this item")
                        printf("Insufficient funds, Customer has €%.2f but €%.2f required for %s.\n",cust->budget, totalProductCost, custItem);
                    }
                }
                // if shop has not enough stock to fill the total customer order of this product, sell the customer what we have
                if (shopQty < custQty){
                    printf("We only have %d of %s at the moment. You will be charged only for the products sold.\n",shopQty, shopItem);
                    totalProductCost = price * shopQty;
                    // check if customer has enough cash to pay
                    if (cust->budget >= totalProductCost){
                        printf("€%.2f  deducted from the customer funds for %d unit(s) of %s\n",totalProductCost, shopQty, custItem);
                        // update shop cash
                        shop->cash += totalProductCost;
                        // update customer cash
                        cust->budget -= totalProductCost;
                        // if customer buys all of the product, there is none remaining
                        shop->stock[j].quantity = 0;
                    }

                    else if((cust->budget < totalProductCost)){
                        //print(f"You have insufficient funds, you only have €{c.budget} but you need €{totalProductCost} to pay for this item")
                        printf("You have insufficient funds, you only have €%.2f but you need €%.2f to pay for %s.\n",cust->budget, totalProductCost, custItem);
                    }
                }
                // if item on customer shopping list does not match any item in the shop stock list
                else if (strcmp(custItem, shopItem)!=0){
                    // flag set to zero,
                        //check =0;
                        printf("");
                    }
            }
        };    
    }
    return *shop;
}

// main program is defined here
int main(void) 
{   // clear clutter from the screen
    clearScreen();
    // create and stock the shop
    printf("Setting up the shop for today ...\n\n\n\n");
	struct Shop shop = createAndStockShop();
    // call the function to display the user menu
    displayMenu();
    // a while loop that does not finish until the user chooses to  exit the program
    int choice  = -1;
    while (choice != 0){
		// clear the standard input
		fflush(stdin); 
        printf("Please select option from the main menu: \t");
        scanf("%d", &choice);

        if (choice ==1){
            printf("1: SHOP OVERVIEW\n");
            //print the current shop stock and cash status
            printShop(&shop);
            returnToMenu();


        } else if (choice ==2){ 
            // for customer csv files
            printf("2: BATCH ORDERS");
            printf("-------------\n");
            struct Customer customer = readCustomer();
            //making sure there is a valid cash balance in the file to proceed
            if (customer.budget ==0){
                returnToMenu();
            }
            else {
            //call functions to print customer shopping list and process the order if possible 
            printCustomer(&customer, &shop);
            processingOrder(&shop,&customer);
            printf("UPDATING CASH.\n-------------------\nCustomer %s has €%.2f left.\n",customer.name, customer.budget);
            returnToMenu();
            }    

        } else if (choice == 3){
            printf("3: *** LIVE MODE ***");
            printf("Please choose from our products listed below\n");
            printShop(&shop);
            // call functions to create customer, print their order and process if possible
            struct Customer c = liveCustomer();
            printCustomer(&c, &shop);
            processingOrder(&shop,&c);
            printf("Customer %s has €%.2f left.",c.name, c.budget);
            returnToMenu();

        // this was for testing
        } else if(choice==4){
            printf("Testing mode");
            returnToMenu();
        }
    }
printf("Thank you for shopping here. Goodbye\n");
return 0;

}
    