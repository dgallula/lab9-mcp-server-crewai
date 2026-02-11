# Create a function that returns a number

# Create a function that receevies 2 numbers and return their sum only if both numbers are positive
def sum_if_positive(num1, num2):
    if num1 > 0 and num2 > 0:
        return num1 + num2
    else:
        return "Both numbers must be positive."