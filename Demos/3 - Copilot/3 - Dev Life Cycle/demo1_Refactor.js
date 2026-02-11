
function sumArray(numbers) {
    try {
        let sum = 0;
        numbers.forEach(num => {
            sum += num;
        });
        return sum;
    } catch (error) {
        console.error("An error occurred while summing the array:", error);
        return 0;
    }
}