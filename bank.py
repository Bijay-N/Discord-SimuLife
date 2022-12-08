import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=dotenv_path)
password = os.getenv('password')

cluster = MongoClient(f"mongodb+srv://MongoDBUser:{password}@cluster0.zvcjjsb.mongodb.net/?retryWrites=true&w=majority")
db = cluster["SimuLife"]
collection = db["bankInfo"]

# Adds client to the system.
def add_client(user):
    post = { "name": user, "wallet": 0, "balance": 500, "inventory": [] }
    collection.insert_one(post)

def user_transfer(user, amount, withdraw):
    # if withdraw is true, then move from bank to wallet
    # if withdraw is false, it is a deposit, so move from wallet to bank
    client_wallet = get_client_wallet(user)
    client_balance = get_client_balance(user)
    query = {"name":user}

    if withdraw == True:
        collection.find_one_and_update(query, {"$set": {"wallet":client_wallet + amount} })
        collection.find_one_and_update(query, {"$set": {"balance":client_balance - amount} })
    else:
        collection.find_one_and_update(query, {"$set": {"wallet":client_wallet - amount} })
        collection.find_one_and_update(query, {"$set": {"balance":client_balance + amount} })

def withdraw(user, amount):
    bal = get_client_balance(user)
    if bal < amount or bal <= 0:        # Checking if the user has the funds to withdraw.
        return False

    user_transfer(user, amount, True)
    return True

def deposit(user, amount):
    wallet = get_client_wallet(user)
    if (wallet >= amount):                  # Checking if the user has the funds to deposit.
        user_transfer(user, amount, False)
        return True
    else:
        # error
        return False

# Checks if the client is in the database.
def client_exists(user):
    query = { "name": user }                        # Grabbing name 
    if (collection.count_documents(query) == 0):    # Query by name. If the client does not exist,
        add_client(user)                            # add the client to the database

    return                                          # Return if the client exists.

# Searches the database for the client.
def get_client_data(user):
    client_exists(user)                 # Check if client is in the database.
    query = { "name": user }            # Query database by name.
    return collection.find_one(query)   # Find and return the client's information

# Fetch client's wallet.
def get_client_wallet(user):
    client = get_client_data(user)
    client_wallet = client["wallet"]
    return client_wallet

# Fetch client's balance.
def get_client_balance(user):
    client = get_client_data(user)
    client_balance = client["balance"]
    return int(client_balance)

# Fetch client's inventory.
def get_client_inventory(user):
    client = get_client_data(user)
    client_inventory = client["inventory"]
    return client_inventory

def sendMoneyToUser(user, amount):
    query = {"name":user}
    client_balance = get_client_balance(user)
    collection.find_one_and_update(query, {"$set": {"balance":client_balance + amount} })
