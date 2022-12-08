import discord
import bank
import re
import simulife

intents=discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('ready!')

@client.event
async def on_message(message):
    user = str(message.author)
    command = message.content

    if command == ".bal" or command == ".balance":
        wallet, balance, total = simulife.show_balance(user)
        await message.channel.send("Wallet: ${}\nBalance: ${}\nTotal: ${}".format(wallet, balance, total))
    elif re.compile(".withdraw \d+").search(command):
        command_split = command.split(" ")
        amount = command_split[1]
        if (bank.withdraw(user, int(amount)) == False):
            await message.channel.send("You don't have the funds for that.")
    elif re.compile(".deposit \d+").search(command):
        command_split = command.split(" ")
        amount = command_split[1]
        if (bank.deposit(user, int(amount)) == False):
            await message.channel.send("You don't have the funds for that.")
    elif command == (".work"):
        amount = simulife.work(user)
        await message.channel.send("You make ${} cleaning barnacles from the lagoon.".format(amount))

