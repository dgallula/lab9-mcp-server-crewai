// Create a function that sorts an array of numbers 
function sortNumbers(arr) {
    return arr.sort((a, b) => a - b);
}

// Create a complicated function that calculates the factorial of a number

function factorial(n) {
    if (n < 0) return -1
    if (n === 0) return 1;
    return n * factorial(n - 1);
}