from colorama import Fore, Style

class Bank():
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

def get_error(err_id, amount):
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
# class Bank():
#     self._users = {}
#     self._accountIDs = {}

class Log_File():
    def __init__(self, filename):
        self._name = filename
        try:
            with open(f"logFiles/{self._name}", "x") as log:
                pass
        except FileExistsError:
            print(f'{Fore.RED}\nfile with name "{self._name}" already exists')
            print('\nPlease delete files from previous session before continuing')
            print(Style.RESET_ALL)

    def append(self, content):
        with open(f"logFiles/{self._name}", "a") as log:
            log.write(f'{content}\n')
    
    def read(self):
        with open(f"logFiles/{self._name}", "r") as log:
            print(log.read())
    
    def get_lines(self):
        with open(f"logFiles/{self._name}", "r") as log:
            return log.readlines()
        

# file = Log_File('pybank_test1')
# file.append('made in pybank')
# file.read()
# print(file.get_lines())

class Account():
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

    def deposit(self, amount):
        try:
            amount = float(amount)
            format(amount, ".2f")
        except Exception as err:
            # print(err)
            return (1, 'nan')
        else:
            if float(amount) < 0:
                return (1, 'neg')
            elif len(str(amount).split('.')[-1]) > 2:
                # print(amount.split('.')[-1])
                return (1, 'dec')
            self._balance += float(amount)
            self._transactions.append(("deposit", amount, self._balance))
            return (0, format(self._balance, ".2f"))                
    
    def withdraw(self, amount):
        try:
            amount = float(amount)
            format(amount, ".2f")
        except:
            return (1, 'nan')
        else:
            if float(amount) < 0:
                return (1, 'neg')
            elif len(str(amount).split('.')[-1]) > 2:
                return (1, 'dec')
            elif float(amount) > self._balance:
                return (1, 'ins')
            self._transactions.append(("withdraw", amount, self._balance))
            self._balance -= float(amount)
            return (0, format(self._balance, ".2f"))
    


# testAccount = Account('AAA-001', '000-000-001')
# while True:
#     test_num = input("deposit money: ")
#     if test_num == 'w':
#         test_num = input("withdraw money: ")
#         print(testAccount.withdraw(test_num))
#         print(testAccount.get_balance())
#         continue
#     print(testAccount.deposit(test_num))
#     print(testAccount.get_balance())
#     continue


print('working?')
def app():
    while True:
        account = None
        while True:
            option = input(f'\nWelcome to PyBank, please enter one of the following commands:\n\n\t{Fore.CYAN}A{Style.RESET_ALL} - Create New Account\n\t{Fore.CYAN}S{Style.RESET_ALL} - Select Account\n\t{Fore.CYAN}Q{Style.RESET_ALL} - Quit"\n\nInput: ').lower().strip()
            if option == 'q':
                print(f'{Fore.RED}Goodbye')
                print(Style.RESET_ALL)
                return
            elif option == 'a':
                account_name = input(f'Please enter a name for your account, or {Fore.CYAN}"Q"{Style.RESET_ALL} to cancel: ').strip()
                if account_name == 'q' or account_name == 'Q':
                    continue
                pybank.iterate_id()
                id_str = f'{pybank.get_id():06d}'
                account_ID = f'{id_str[:3]}-{id_str[3:]}'
                new_account = Account(account_name, account_ID)
                pybank.add_account(new_account)
                # ACCOUNTS[new_account.get_number()] = new_account
                print (f'{Fore.GREEN}\nNew Account Created! Details:\n\t{Style.RESET_ALL}Account Name: {Fore.YELLOW}{new_account.get_name()}\n\t{Style.RESET_ALL}Account ID: {Fore.YELLOW}{new_account.get_number()}')
                print (Style.RESET_ALL)
                continue
            elif option == 's':
                if len(pybank.get_accounts()) == 0:
                    print(f'{Fore.RED}\nYou have created no accounts yet, please create an account first')
                    print(Style.RESET_ALL)
                    continue
                account_lst = []
                counter = 1
                display = f'Please Choose an Account {Fore.YELLOW}(Account Name, Account ID, Balance){Style.RESET_ALL}:\n\n'
                for id_num, acc in pybank.get_accounts().items():
                    display += f'\t{Fore.CYAN}{counter}{Style.RESET_ALL} - {Fore.YELLOW}{acc.get_name()}{Style.RESET_ALL}, {Fore.YELLOW}{id_num}{Style.RESET_ALL}, {Fore.YELLOW}${acc.get_balance()}\n{Style.RESET_ALL}'
                    counter += 1
                    account_lst.append(acc)
                display += f'\t{Fore.CYAN}Q{Style.RESET_ALL} - Cancel\n'
                display += '\nEnter Number: '
                while True:
                    choice = input(display).strip()
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
                    else:
                        account = account_lst[int(choice) - 1]
                        break
                break
            else:
                print(f'{Fore.RED}\n{option} is not a valid option, please try again')
                print(Style.RESET_ALL)
                continue
        while True:
            print(f'\n{Fore.GREEN}Current Account\n\t{Style.RESET_ALL}Name: {Fore.YELLOW}{account.get_name()}\n\t{Style.RESET_ALL}ID: {Fore.YELLOW}{account.get_number()}\n\t{Style.RESET_ALL}Balance: {Fore.YELLOW}${account.get_balance()}')
            option = input(f'\nPlease enter one of the following commands:\n\n\t{Fore.CYAN}W{Style.RESET_ALL} - withdraw\n\t{Fore.CYAN}D{Style.RESET_ALL} - deposit\n\t{Fore.CYAN}V{Style.RESET_ALL} - View Previous Transactions\n\t{Fore.CYAN}Q{Style.RESET_ALL} - Back to Account Selection"\n\nInput: ').lower().strip()
            if option == 'q':
                break
            elif option == 'v':
                if len(account.get_transactions()) == 0:
                    print(f'\n{Fore.RED}This account has made no transactions yet\n')
                    print (Style.RESET_ALL)
                    continue
                display = f'{Fore.GREEN}Transaction History (Type: Amount, New Balance){Style.RESET_ALL}\n\n'
                for transaction in account.get_transactions():
                    display += f'\t{transaction[0].capitalize()}: {Fore.CYAN}${transaction[1]}{Style.RESET_ALL}, {Fore.YELLOW}${transaction[2]}{Style.RESET_ALL}\n'
                display += f'\n{Fore.RED}End of Transaction Record{Style.RESET_ALL}'
                print(display)
                continue
            elif option == 'd':  
                while True:
                    amount = input(f'\n{Fore.CYAN}Deposit\n\n{Style.RESET_ALL}Enter deposit amount or {Fore.CYAN}"Q"{Style.RESET_ALL} to cancel: ')
                    if amount == 'q':
                        break
                    confirm = input(f'Deposit "${amount}"? (Y / N): ').lower().strip()
                    if confirm == 'n':
                        continue
                    elif confirm == 'y':
                        code = account.deposit(amount)
                        # print (code)
                        if code[0]:
                            get_error(code[1], amount)
                            continue
                        else:
                            account._log.append(f'deposit: {amount}, {account.get_balance()}')
                            print (f'{Fore.GREEN}You have deposited {Fore.YELLOW}"${format(float(amount), ".2f")}"{Fore.GREEN}, your new balance is {Fore.YELLOW}"${account.get_balance()}"{Style.RESET_ALL}')  
                        break
                    else: 
                        continue
            elif option == 'w':
                while True:
                    amount = input(f'\n{Fore.CYAN}Withdraw\n\n\t{Style.RESET_ALL}Current Balance = {Fore.YELLOW}"${account.get_balance()}"{Style.RESET_ALL}\n\nEnter withdraw amount or {Fore.CYAN}"Q"{Style.RESET_ALL} to cancel: ')
                    if amount == 'q':
                        break
                    confirm = input(f'Withdaw "${amount}"? {Fore.CYAN}(Y / N){Style.RESET_ALL}: ').lower().strip()
                    if confirm == 'n':
                        continue
                    elif confirm == 'y':
                        code = account.withdraw(amount)
                        # print (code)
                        if code[0]:
                            get_error(code[1], amount)
                            continue
                        else:
                            account._log.append(f'("withdraw", {amount}, {account.get_balance()})')
                            print (f'{Fore.GREEN}You have withdrawn {Fore.YELLOW}"${format(float(amount), ".2f")}"{Fore.GREEN}, your new balance is {Fore.YELLOW}"${account.get_balance()}"{Style.RESET_ALL}')
                        break
                    else: 
                        continue
            else:
                print(f'{Fore.RED}\n{option} is not a valid option, please try again')
                print(Style.RESET_ALL)
                continue
            more = input(f'\nWould you like to make another transaction? {Fore.CYAN}(Y / N){Style.RESET_ALL}: ').lower().strip()
            if more == 'n':
                break
            else:
                continue

pybank = Bank()
app()
print(Style.RESET_ALL)
