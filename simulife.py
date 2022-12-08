import bank
import random

def work(user):
    amount = random.randint(457, 2304)
    bank.sendMoneyToUser(user, amount)
    return amount

def show_balance(user):
    balance = bank.get_client_balance(user)
    wallet = bank.get_client_wallet(user)
    total = balance + wallet

    return (wallet, balance, total)

