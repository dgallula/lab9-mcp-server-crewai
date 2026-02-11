// Write a struct the represents a Product
// Price is a must.
// Dont include color
// Add more attributes if needed
#include <string>

struct Product {
    double price;
    std::string name;
    int quantity;

    Product(double p, std::string n, int q) : price(p), name(n), quantity(q) {}
};