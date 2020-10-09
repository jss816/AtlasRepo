import discord
from discord.ext import commands
from discord import message
import re
import numpy
import csv



finishedDict = { "Author" : " ",
    "ticker" : " ",
    "strike" : " ",
    "type" : " ",
    "exp" : " ",
    "entry_price" : " ",
    "entry_date" : " ",
    "exit_date" : " ",
    "exit_price" : " ",
    "WL" : " "
    }
fieldnames = finishedDict.keys()
storeHere = []

token = 'NzYyOTYzNzk4MzQ0NTk3NTA0.X3wzaA.Ezat8NQaOBRiQU2GxBLrLoiGAAg'

bot = commands.Bot(command_prefix='!')

client = discord.Client()

@bot.event
async def on_ready():
    print('Logged in as: ' + bot.user.name)
    print('Bot ID: ' + str(bot.user.id))
    print('--------------------------')



@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.event
async def on_message(message):
    testMe2 = re.search('(?<=BTO) (.*)', message.content)
    authorOfMessage = message.author

    finishedDict.update(Author = str(authorOfMessage))
    words = testMe2.group(0).split()
    await message.channel.send("Found: " + str(testMe2) + "Signaled By: " + str(authorOfMessage))
    print(words)
    for i in range(len(words)):
        if i == 0:
            finishedDict.update(ticker = words[i])
        elif i == 1:
            finishedDict.update(strike = words[i])
        elif i == 2:
            finishedDict.update(type = words[i])
        elif i == 3:
            finishedDict.update(exp = words[i])
        elif i == 4:
            finishedDict.update(entry_price = words[i])
    t = message.timestamp
    finishedDict.update(entry_date = str(t))
    print(fieldnames)
    storeHere.append(finishedDict)

    output = open('test.csv', 'w', newline='')
    with output:
        dict_writer = csv.DictWriter(output, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(storeHere)

    await message.channel.send("Found: " + str(testMe2) + "Signaled By: " + str(authorOfMessage))
    return



client.run(token)

bot.run('')
