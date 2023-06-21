# Import for command line styling
from colorama import Fore, Style
import os

# delete the files from the session before closing, otherwise hosted demo has conflicts when making files
def log_purge_quit():
    for account in pybank.get_accounts().values():
        file_name = account.get_log().get_name()
        os.remove(f"logFiles/{file_name}")
    quit()

class Bank():
    '''
    Class for the overall Bank, used to hold and modify variables tht would otherwise be global, created account objects belong to the Bank object
    '''
    # current_id is used to give a unique identifier to each account created, it is iterated for each account
    # the accounts dictionary hold all created account objects, with keys being the account ID, 
    def __init__(self):
        self._current_id = 0
        self._accounts = {}
    
    def iterate_id(self):
        self._current_id += 1

    def get_id(self):
        return self._current_id

    def add_account(self, account):
        self._accounts.update({account.get_number(): account})

    def get_accounts(self):
        return self._accounts


class Log_File():
    '''
    class for the log files, to implement methods fro appending transactions, a log file object belongs to an account object
    '''
    # the log file init contains an escape route from the program which might be confusing, would want to move this to the workflow in later iterations
    def __init__(self, filename):
        self._name = filename
        try:
            with open(f"logFiles/{self._name}", "x") as log:
                pass
        except FileExistsError:
            print(f'{Fore.RED}\nfile with name "{self._name}" already exists')
            print('\nFile managment error, please delete all files in "logFiles" dir (except "dummy") from previous session before continuing')
            print(Style.RESET_ALL)
            log_purge_quit()

    def append(self, content):
        with open(f"logFiles/{self._name}", "a") as log:
            log.write(f'{content}\n')
    
    def read(self):
        with open(f"logFiles/{self._name}", "r") as log:
            print(log.read())
    
    def get_lines(self):
        with open(f"logFiles/{self._name}", "r") as log:
            return log.readlines()
    
    def get_name(self):
        return self._name

class Account():
    '''
    this is the main account class that handles each of the account the user creates, the account objects belong to the Bank object, and the log file objects each belong to an account
    '''
    # We create a log file object for the account during account initialization, this creates a bit of coupling between them, other option could be to create it in the workflow and pass it to the account, but this seems cleaner initially
    def __init__(self, name, num, owner=None):
        self._name = name
        self._number = num
        self._owner = owner
        self._balance = 0.00
        self._transactions = []
        self._log = Log_File(f"log{num}")

        self._log.append(f'Account ID: {self._number}\nAccount Name: {self._name}\nCustomer: {self._owner}')

    def get_number(self):
        return self._number
    
    def get_name(self):
        return self._name
    
    def get_owner(self):
        return self._number

    def get_balance(self):
        return format(self._balance, ".2f")

    def get_transactions(self):
        return self._transactions
    
    def get_log(self):
        return self._log

    # both the deposit and withdraw methods return error "codes" if there is an issue with the string passed for amount, the workflow then calls an error function based on these codes
    def deposit(self, amount):
        # check if number is float, and if can be properly formatted with format()
        try:
            amount = float(amount)
            format(amount, ".2f")

        # return error code if number is not a proper number
        except Exception as err:
            return (1, 'nan')
        
        # if number can be a float, ensure it is not negative, and that it is not more than 2 decimals long
        else:
            if float(amount) < 0:
                return (1, 'neg')
            elif len(str(amount).split('.')[-1]) > 2:
                return (1, 'dec')
            
            # if number passes checks, deposit it and add the transactions to the transactions list
            self._balance += float(amount)
            self._transactions.append(("deposit", amount, self._balance))
            return (0, format(self._balance, ".2f"))                
    
    def withdraw(self, amount):
        # check if number is float, and if can be properly formatted with format()
        try:
            amount = float(amount)
            format(amount, ".2f")
        
        # return error code if number is not a proper number
        except:
            return (1, 'nan')
        
        # if number can be a float, ensure it is not negative, and that it is not more than 2 decimals long, and ensure it is not more than the account balance
        else:
            if float(amount) < 0:
                return (1, 'neg')
            elif len(str(amount).split('.')[-1]) > 2:
                return (1, 'dec')
            elif float(amount) > self._balance:
                return (1, 'ins')
            
            # if number passes checks, deposit it and add the transactions to the transactions list
            self._transactions.append(("withdraw", amount, self._balance))
            self._balance -= float(amount)
            return (0, format(self._balance, ".2f"))


# function called by after deposit or withdraw if the corresponding methods returned an error code instead of a success    
def get_error(err_id, amount):
    '''
    returns error responses to the user for various issues with deposit/withdraw amounts given, called by the deposit and withdraw methods of the Account class
    '''
    if err_id == 'nan':
        print(f'{Fore.RED}\nERROR: {amount} is not a valid number')
        print(Style.RESET_ALL)
    elif err_id == 'neg':
        print(f'{Fore.RED}\nERROR: Value can not be negative')
        print(Style.RESET_ALL)
    elif err_id == 'dec':
        print(f'{Fore.RED}\nERROR: Value must have a maximum of two decimal places')
        print(Style.RESET_ALL)
    elif err_id == 'ins':
        print(f'{Fore.RED}\nERROR: {amount} is greater than your current balance')
        print(Style.RESET_ALL)
    else:
        print(f'{Fore.RED}\nERROR: Unknown error occurred, please try again')
        print(Style.RESET_ALL)

# workflow for choosing an account, this was seperated from the main app() function to get rid of nested while loops for readability 
def choose_account(account_lst, display_str):
    '''
    asks the user for the account they wish to open, takes the account list and display_str to display to the user for choosing accounts, and returns the user-chosen account
    '''
    while True:
        # ask for user choice of account
        choice = input(display_str).strip()

        # return None if the user doesnt choose an account
        if choice == 'q':
            return

        # validate choice is indeed an int and one of the options shown
        try:
            int(choice)
            if int(choice) < 1:
                raise Exception
            if not account_lst[int(choice) - 1]:
                raise Exception
        except:
            print(f'{Fore.RED}\nInput must be the list number of one of your accounts')
            print(Style.RESET_ALL)
            continue

        # return the chosen account
        else:
            return account_lst[int(choice) - 1]

# workflow for deposit, this was seperated from the main app() function to get rid of nested while loops for readability 
def deposit_flow(account):
    '''
    takes the account to be acted on, deposits money, and returns nothing
    '''
    while True:
        # ask the user for the deposit amount 
        amount = input(f'\n{Fore.CYAN}Deposit\n\n{Style.RESET_ALL}Enter deposit amount or {Fore.CYAN}"Q"{Style.RESET_ALL} to cancel: ')
        if amount == 'q':
            break

        # confirm the choice, as a bank would
        confirm = input(f'Deposit "${amount}"? (Y / N): ').lower().strip()
        if confirm == 'n':
            continue
        # if yes, attempt to deposit
        elif confirm == 'y':
            code = account.deposit(amount)

            # if the deposit method returns an error code, get the error message from the get_error() function to return to the use, if not, deposit the money and display success message
            if code[0]:
                get_error(code[1], amount)
                continue
            else:
                account._log.append(f'deposit: {amount}, {account.get_balance()}')
                print (f'{Fore.GREEN}You have deposited {Fore.YELLOW}"${format(float(amount), ".2f")}"{Fore.GREEN}, your new balance is {Fore.YELLOW}"${account.get_balance()}"{Style.RESET_ALL}')  
            break
        else: 
            continue

# workflow for withdraw, this was seperated from the main app() function to get rid of nested while loops for readability 
def withdraw_flow(account):
    '''
    takes the account to be acted on, withdraws money, and returns nothing
    '''
    while True:
        # ask the user for the withdraw amount
        amount = input(f'\n{Fore.CYAN}Withdraw\n\n\t{Style.RESET_ALL}Current Balance = {Fore.YELLOW}"${account.get_balance()}"{Style.RESET_ALL}\n\nEnter withdraw amount or {Fore.CYAN}"Q"{Style.RESET_ALL} to cancel: ')
        if amount == 'q':
            break

        # confirm the choice, as a bank would
        confirm = input(f'Withdaw "${amount}"? {Fore.CYAN}(Y / N){Style.RESET_ALL}: ').lower().strip()
        if confirm == 'n':
            continue

        # if yes, attempt to withdraw
        elif confirm == 'y':
            code = account.withdraw(amount)

            # if the deposit method returns an error code, get the error message from the get_error() function to return to the use, if not, deposit the money and display success message
            if code[0]:
                get_error(code[1], amount)
                continue
            else:
                account._log.append(f'("withdraw", {amount}, {account.get_balance()})')
                print (f'{Fore.GREEN}You have withdrawn {Fore.YELLOW}"${format(float(amount), ".2f")}"{Fore.GREEN}, your new balance is {Fore.YELLOW}"${account.get_balance()}"{Style.RESET_ALL}')
            break
        else: 
            continue

# main app() function that starts the banking app
def app():
    while True:
        # The first inner while loop is the account creation and selection work flow, the second is the transactions within an account flow
        while True:

            # ask the user what they would like to do, the user must make an account before any banking can be done
            option = input(f'\nWelcome to PyBank, please enter one of the following commands:\n\n\t{Fore.CYAN}A{Style.RESET_ALL} - Create New Account\n\t{Fore.CYAN}S{Style.RESET_ALL} - Select Account\n\t{Fore.CYAN}Q{Style.RESET_ALL} - Quit"\n\nInput: ').lower().strip()

            # if the user wants to quit, end the program
            if option == 'q':
                print(f'{Fore.RED}Goodbye')
                print(Style.RESET_ALL)
                log_purge_quit()
            
            # account creation flow
            elif option == 'a':
                #the user is prompted to give a name for the new account
                account_name = input(f'Please enter a name for your account, or {Fore.CYAN}"Q"{Style.RESET_ALL} to cancel: ').strip()

                # back to the main screen is 'q' is input
                if account_name == 'q' or account_name == 'Q':
                    continue

                # iterate the account identifier variable in the pybank Bank() object, and give the account a unique id in the formal "000-000"
                pybank.iterate_id()
                id_str = f'{pybank.get_id():06d}'
                account_ID = f'{id_str[:3]}-{id_str[3:]}'

                # initialize the new account object with the account ID just created, and name given by the user, the add the account to the account dictionary in the pybank object
                new_account = Account(account_name, account_ID)
                pybank.add_account(new_account)

                # display a success message with account details to the user
                print (f'{Fore.GREEN}\nNew Account Created! Details:\n\t{Style.RESET_ALL}Account Name: {Fore.YELLOW}{new_account.get_name()}\n\t{Style.RESET_ALL}Account ID: {Fore.YELLOW}{new_account.get_number()}')
                print (Style.RESET_ALL)
                continue

            # account selection flow, calls the choose_account() function
            elif option == 's':

                # if there are no accounts made, then notify the user and go back to main screen
                if len(pybank.get_accounts()) == 0:
                    print(f'{Fore.RED}\nYou have created no accounts yet, please create an account first')
                    print(Style.RESET_ALL)
                    continue

                # if there are accounts, initialize an empty list with all accounts, for ease of reference by list index by the user
                account_lst = []
                
                # begin building a string to display to the user of all their availible accounts, looping through each account in the pybank accounts dictionary and addind their identifiers, names and balances to the string
                display_str = f'Please Choose an Account {Fore.YELLOW}(Account Name, Account ID, Balance){Style.RESET_ALL}:\n\n'
                counter = 1
                # loop through accoutns
                for id_num, acc in pybank.get_accounts().items():
                    # add account info to the display string, and iterate the counter that is used at the start of each entry in the display string as an easy way for the user to choose an account
                    display_str += f'\t{Fore.CYAN}{counter}{Style.RESET_ALL} - {Fore.YELLOW}{acc.get_name()}{Style.RESET_ALL}, {Fore.YELLOW}{id_num}{Style.RESET_ALL}, {Fore.YELLOW}${acc.get_balance()}\n{Style.RESET_ALL}'
                    counter += 1

                    # append the account to the account list, again so the "counter" chosen by the user can be used to easily pick-out the correct account, the reason the counter isnt just used earlier key for the account in the account dictionary, which would avoid the construction of this list, is for the future implementation of multiple users, which where we want every account to have a different unique key 
                    account_lst.append(acc)
                display_str += f'\t{Fore.CYAN}Q{Style.RESET_ALL} - Cancel\n'
                display_str += '\nEnter Number: '
                
                # call the choose_account() function to finally display the built display string to the user and prompt an account choice, this was separated to a different function to avoid another nested while loop for readability
                account = choose_account(account_lst, display_str)

                # if the user did not choose an account, and choose_account() returned None, reset loop
                if not account:
                    continue
                break
            
            # reset the loop if the user doesnt input one of the given options
            else:
                print(f'{Fore.RED}\n{option} is not a valid option, please try again')
                print(Style.RESET_ALL)
                continue

        # The second inner while loop transactions workflow within an account selected in the previous while loop
        while True:
            # print the current accounts basic info, and ask the user what they would like to do
            print(f'\n{Fore.GREEN}Current Account\n\t{Style.RESET_ALL}Name: {Fore.YELLOW}{account.get_name()}\n\t{Style.RESET_ALL}ID: {Fore.YELLOW}{account.get_number()}\n\t{Style.RESET_ALL}Balance: {Fore.YELLOW}${account.get_balance()}')

            option = input(f'\nPlease enter one of the following commands:\n\n\t{Fore.CYAN}W{Style.RESET_ALL} - withdraw\n\t{Fore.CYAN}D{Style.RESET_ALL} - deposit\n\t{Fore.CYAN}V{Style.RESET_ALL} - View Previous Transactions\n\t{Fore.CYAN}Q{Style.RESET_ALL} - Back to Account Selection"\n\nInput: ').lower().strip()

            # go back to the main create/choose account screen if the user wants
            if option == 'q':
                break

            # option to view the past transactions of the account
            elif option == 'v':

                # check if there are any past transactons, and tell the user if not
                if len(account.get_transactions()) == 0:
                    print(f'\n{Fore.RED}This account has made no transactions yet\n')
                    print (Style.RESET_ALL)
                    continue

                # initialize the display string that will include all transactions
                display_str = f'{Fore.GREEN}Transaction History (Type: Amount, New Balance){Style.RESET_ALL}\n\n'
                #loop through each past transaction and add them to the display string with custom formatting
                for transaction in account.get_transactions():
                    display_str += f'\t{transaction[0].capitalize()}: {Fore.CYAN}${transaction[1]}{Style.RESET_ALL}, {Fore.YELLOW}${transaction[2]}{Style.RESET_ALL}\n'
                # add end statement, and print the string to the user
                display_str += f'\n{Fore.RED}End of Transaction Record{Style.RESET_ALL}'
                print(display_str)
                continue

            # opening the deposit flow function, seperated to get rid of another nested while loop
            elif option == 'd':
                deposit_flow(account) 

            # opening the withdraw flow function, seperated to get rid of another nested while loop
            elif option == 'w':
                withdraw_flow(account)

            # if the user gives no valid input, let them know and reset
            else:
                print(f'{Fore.RED}\n{option} is not a valid option, please try again')
                print(Style.RESET_ALL)
                continue
            
            # ak if they want to make another transaction, if not then go back to the account selection screen, if so, reset this loop
            more = input(f'\nWould you like to make another transaction? {Fore.CYAN}(Y / N){Style.RESET_ALL}: ').lower().strip()
            if more == 'n':
                break
            else:
                continue


# create the main Bank object that holds "global" info, and start the banking app
pybank = Bank()
app()

# delete log files created during execution
log_purge_quit()

# reset command ine styling
print(Style.RESET_ALL)
