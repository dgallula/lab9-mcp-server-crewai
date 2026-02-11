// Math operations module

// Addition
function KIVUN_add(a, b) {
    return a + b;
}

// Subtraction
function KIVUN_subtract(a, b) {
    return a - b;
}

// Multiplication
function KIVUN_multiply(a, b) {
    return a * b;
}

// Division
function KIVUN_divide(a, b) {
    if (b === 0) {
        throw new Error("Division by zero is not allowed.");
    }
    return a / b;
}

// Exporting the functions
module.exports = {
    KIVUN_add,
    KIVUN_subtract,
    KIVUN_multiply,
    KIVUN_divide
};