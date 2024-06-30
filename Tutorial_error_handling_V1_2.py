# Program: checks for a valid number
# Author: Michael Wu
# Date: 27 June 2024
# Version 1.2

# TODO: Create a function to call every time I ask a user for a number
#

'''
# checking for a valid number. if it is not a valid number, then try again.
done = False
while not done: 
    print:("Please enter your value as an integer")
    try:
        num = int(input())
        done = True
    except ValueError:
        print("That is not an integer.")
        continue
        
print(f"The integer you entered is {num}")


# Create a function to call every time I ask a user for a number.
# It tries for a correct number until a valid one gets entered.

def test_float_num (question): # The parameter 'question' is a placeholder where my question will insert when i call the function.
    done = False
    error = "That is not a valid number."
    while not done:
        print(question)
        try:
            num = float(input())
            done = True # Or use the word 'break'.
        except ValueError: # If an incorrect value is enters, the program t doen't crash, but instead runs the section of code under the 'except'.
            print(error)
    return(num) 

#----------- Main program -----------#
# Call the function and use it in more than one question

num_1 = test_float_num("Please enter your 1st number:")
num_2 = test_float_num("Please enter your 2nd number:")

print(f"The 1st number you entered is {num_1} and the 2nd number you entered is {num_2}")
'''
# Create a function to call every time I ask a user for a number.
# It tries for a correct number until a valid one gets entered.

def test_float_num (question): # The parameter 'question' is a placeholder where my question will insert when i call the function.
    error = "That is not a valid number."
    while True:
        print(question)
        try:
            num = float(input())
            break
        except ValueError: # If an incorrect value is enters, the program t doen't crash, but instead runs the section of code under the 'except'.
            print(error)
    return(num) 

#------------ Main program ----------------#
print("welcome, you will be asked to enter 3 numbers. the program will then add them together.")
total = 0 
for i in range(3): # i is name of loop, 3 is no. of times this code will be repeated
    num = test_float_num("Please enter your value:")
    print("The number",i+1,"you entered is", num)
    total += num #Adds the inputted number into the total
print(f"The total of the numbers added is {total}")