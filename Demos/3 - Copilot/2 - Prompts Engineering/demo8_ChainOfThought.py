#Write a Python function that checks if a given string is a palindrome
#First, define a function called "is_palindrome" that takes a string as input.
#Next, convert the string to lowercase to avoid case sensitivity.
#Then, iterate through the string and compare the characters at the beginning and end.
#If they match, move inwards one character at a time and repeat the comparison.
#If all characters match their counterparts, return True (the string is a palindrome). Otherwise, return False.

def is_palindrome(s):
    # Convert the string to lowercase
    s = s.lower()
    
    # Initialize pointers
    left, right = 0, len(s) - 1
    
    # Iterate through the string
    while left < right:
        # Compare characters
        if s[left] != s[right]:
            return False
        # Move inwards
        left += 1
        right -= 1
    
    return True
