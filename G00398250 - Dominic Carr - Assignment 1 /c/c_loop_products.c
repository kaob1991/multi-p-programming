#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Product {
	char* name;
	double price;
};

struct ProductStock {
	struct Product product;
	int quantity;
};

struct Shop {
	double cash;
	struct ProductStock stock[20];
	int index;
};

struct Shop createAndStockShop()
{
	struct Shop shop = { 200 };
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    while ((read = getline(&line, &len, fp)) != -1) {		
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");
		int quantity = atoi(q);
		double price = atof(p);
		char *name = malloc(sizeof(char) * 50);
		strcpy(name, n);
		struct Product product = { name, price };
		struct ProductStock stockItem = { product, quantity };
		shop.stock[shop.index++] = stockItem;
    }
	
	return shop;
}

double find(struct Shop s, char* name)
{
	for (int i = 0; i < s.index; i++)
	{
		if (strcmp(name, s.stock[i].product.name) == 0){
			return s.stock[i].product.price;
		}
	}
	return -1;
}

int main(void) 
{
	struct Product productA = { "Coke Can", 0.0 };
	struct Product productB = { "Big Bags", 0.0 };
	struct Product productC = { "Spaghetti", 0.0 };
	struct ProductStock StockA = { productA, 12 };
	struct ProductStock StockB = { productB, 5 };
	struct ProductStock StockC = { productC, 2 };
	
	struct ProductStock array[] = { StockA, StockB, StockC }; 
	
	struct Shop shop = createAndStockShop();
	
	double totalCostForCustomer = 0;
	for(int i=0; i < 3; i++){
		struct Product p = array[i].product;
		double price = find(shop, p.name);
		printf("The price of %s in the shop is %.2f\n", p.name, price);
		double totalCostOfItem = array[i].quantity * price;
		printf("You want %d of %s, that will cost you %.2f\n", array[i].quantity, p.name, totalCostOfItem);
		totalCostForCustomer += totalCostOfItem;
	}
	printf("The total cost for the customer will be %.2f\n", totalCostForCustomer);
	
    return 0;
}