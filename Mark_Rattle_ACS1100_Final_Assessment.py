import re

'''
Online banking app for final assessment in ACS1100
Data.txt has a list of users and information that will be parsed by the program
The user will be prompted to input their username/password combo and if either are not found or the combination is not correct they will be denied access without exposing which element was incorrect.
If a correct username and password combination is entered, the user will be shown their account information and granted access to extra functions.
'''
# define the data file as a variable for file read-in
user_file = "./data.txt"

account_info = {}

def get_accounts(user_file):
    '''
    A funciton that opens data.txt and creates a dictionary of with usernames as keys and password, full_name, and balance as associated values
    Input - user_info (string): location of the data.txt file as a string
    Return - account_info (dict): compiled dict of usernames as keys + associated info as values
    '''
    infile = open(user_file, "r")
    file_lines = infile.readlines()
    infile.close()
    for line in file_lines:
        split_line_list = line.rstrip().split(",")
        username = split_line_list[0]
        password = split_line_list[1]
        full_name = split_line_list[2]
        balance = float(split_line_list[3])
        account_info[username] = password, full_name, balance


def authenticate():
    '''
    A function to get user input of username and password, which validates matching key/value pairs for username/password.  Allows access when given a correct un/pw pair
    Input - nothing
    Return - input_username (string): authenticated username
    '''
    input_username = input("Please input your username > ")
    input_password = input("Please enter your password > ")

    # nested conditionals to eliminate key errors on bogus username input

    if input_username in account_info:
        if input_password == account_info[input_username][0]:
            print("Access granted!")
            authenticated_user = input_username
            return authenticated_user    
        else:
            print("User name and password not found.")
    else:
        print("User name and password not found.")

def display_information(authenticated_user):
    '''
    A function to display full name and balance information for a successfully authenticated user
    Input - authenticated_user (string): validated username received as return from autheticate() function
    Return - none
    '''
    print(f'Full name: {account_info[authenticated_user][1]}')
    print(f'Current balance: {account_info[authenticated_user][2]}')

def get_option():
    '''
    A function to get option input for extra functions from the user.  Loops until the user is done.
    Input - none
    Return - none
    '''
    option_loop = True
    while option_loop == True:
        print("""
Account options:
1 - Deposit
2 - Withdraw
3 - Transfer to another user's account
4 - Display current balance
0 - Exit

""")
        option_input = input("Please enter an option > ")
        match option_input:
            case '1':
                deposit(authenticated_user, account_info)
            case '2':
                withdraw(authenticated_user, account_info)
            case '3':
                transfer(authenticated_user, account_info)
            case '4':
                print(f"Your account balance is: ${account_info[authenticated_user][2]}")
            case '0':
                print("Thank you for using the bank!")
                option_loop = False

def untuple(authenticated_user, account_info):
    '''
    A function that unpacks a tuple so that balance can be modified and packed back into the dict
    This is super ugly but I'm not sure how to quickly break a tuple into something mutable
    Input - authenticated_user (string): currently authenticated username
        account_info (dict): user info dict
    Return - Info_package (list): Returns a list of current user info that is mutable because I found out that I accidentally built myself into a corner with tuples.
    '''
    password = account_info[authenticated_user][0]
    full_name = account_info[authenticated_user][1]
    balance = account_info[authenticated_user][2]
    info_package = [password, full_name, balance]
    return info_package

def deposit(authenticated_user, account_info):
    '''
    A function to add a deposit amount to a user's current balance. Takes a number greater than 0, up to $9000 (even trims the '$' if entered) and adds to balance. 
    Input - authenticated_user (string): currently authenticated username
            account_info (dict): user info dict
    Return - none
    '''
    info_package = untuple(authenticated_user, account_info)
    deposit_amount = input("Please enter a deposit amount. This terminal can only accept up to $9000 at a time > ")
    while re.match("[^0-9\.\$]*$", deposit_amount) or float(deposit_amount.strip('$')) <= 0 or float(deposit_amount.strip('$')) > 9000:
        deposit_amount = input("Not a valid deposit amount.  Please enter a number greater than 0, with a $9000 limit > ")

    deposit_amount = float(deposit_amount)
    account_info[authenticated_user] = info_package[0], info_package[1], (info_package[2] + deposit_amount)
    print(f"Your account balance is: ${account_info[authenticated_user][2]}")

def withdraw(authenticated_user, account_info):
    '''
    A function to subtract a withdrawal amount from a user's current balance. Takes a number greater than 0, up to the user's current balance (even trims the '$' if entered) and subtracts from the balance. 
    Input - authenticated_user (string): currently authenticated username
            account_info (dict): user info dict
    Return - none
    '''
    info_package = untuple(authenticated_user, account_info)
    if info_package[2] > 0:
        withdraw_amount = input(f"Your current balance is: ${account_info[authenticated_user][2]}. Please enter an amount to withdraw, up to your current balance > ")
        while re.match("[^0-9\.\$]*$", withdraw_amount) or float(withdraw_amount.strip('$')) <= 0 or float(withdraw_amount.strip('$')) > account_info[authenticated_user][2]:
            withdraw_amount = input(f"Not a valid amount to withdraw.  Please enter a number greater than 0, up to ${account_info[authenticated_user][2]} > ")
        withdraw_amount = float(withdraw_amount)
        account_info[authenticated_user] = info_package[0], info_package[1], (info_package[2] - withdraw_amount)
    else:
        print("You have no money in your account!")
    print(f"Your remaining balance is: ${account_info[authenticated_user][2]}")

def transfer(authenticated_user, account_info):
    '''
    A function to transfer balances between accounts.  Takes a username for the account to be transferred to and transfers user input amount.
    Input - authenticated_user (string): currently authenticated username
            account_info (dict): user info dict
    Return - none
    '''
    transfer_to_user = ''
    info_package_send = untuple(authenticated_user, account_info)
    if info_package_send[2] > 0:
        while transfer_to_user not in account_info:
            transfer_to_user = input("Please enter the username of the account you would like to transfer to > ") 
        transfer_amount = input(f"Your current balance is: ${account_info[authenticated_user][2]}. Please enter an amount to transfer to {[account_info[transfer_to_user][1]]}, up to your current balance > ")
        while re.match("[^0-9\.\$]*$", transfer_amount) or float(transfer_amount.strip('$')) <= 0 or float(transfer_amount.strip('$')) > account_info[authenticated_user][2]:
            transfer_amount = input(f"Not a valid amount to transfer. Please enter a number greater than 0, up to ${account_info[authenticated_user][2]} > ")
        transfer_amount = float(transfer_amount)
        account_info[authenticated_user] = info_package_send[0], info_package_send[1], (info_package_send[2] - transfer_amount)
        info_package_rcv = untuple(transfer_to_user, account_info)
        account_info[transfer_to_user] = info_package_rcv[0], info_package_rcv[1], (info_package_rcv[2] + transfer_amount)

# Program are calls here, loops until the user wants to quit

get_accounts(user_file)
keep_repeating = True
another_user = ''
while keep_repeating == True:
    authenticated_user = authenticate()
    if authenticated_user in account_info:
        display_information(authenticated_user)
        get_option()
        while another_user.lower() != 'y' and another_user.lower() != 'n':
            another_user = input("Would you like to access another account? Please enter y / n > ")
            if another_user.lower() == 'n':
                keep_repeating = False
        another_user = ''
print("Goodbye!")

