import sqlite3
import discord
from discord.ext import commands
from discord import utils
from discord.ext.commands import Bot
from discord.utils import get
from datetime import date
import re
from discord import emoji
from discord import Message
import send_sms


phDate = date.today()

con = sqlite3.connect("DatabaseName.sql")

cur = con.cursor()

#make positions table
cur.execute('''CREATE TABLE IF NOT EXISTS Positions
                (date text, status text, symbol text, strike real, callp char, expiry text, price real, pandl real)''')




client = discord.Client()

token = 'NzY2MDA4MjkyNjQ0MjI1MDc2.X4dG0A.1J9KRiqVfaky9o_GmUXF9SRGLCU'

bot = commands.Bot(command_prefix='!')



def sanitize(text):
    text.replace('@everyone', '@\u200beveryone') # \u200b is our condom
    return text

@bot.command(name='sms')
async def send_smss(ctx, message):
    send_sms.send(message)
    return await SendHomeMML('Sent!')


@bot.command(name='say')
async def say(ctx, args):
    message = "@everyone"
    message = sanitize(message)
    await SendHomeMML(message)

    taabluedisc = discord.utils.get(bot.emojis, name='taabluedisc')
    message = f"{args}" + "\n" + f"{taabluedisc}"
    MessageE = discord.Embed(title = "", description=message, colour=0x12341)
    Message = await SendHomeEML(MessageE)
    await Message.add_reaction(taabluedisc)
    await SendMattEML(MessageE)
    await SendOZEML(MessageE)
    await Message.add_reaction(taabluedisc)

    return

@bot.command(name='sayP')
async def sayP(ctx, args, argl):
    message = "@everyone"
    message = sanitize(message)
    await SendHomeMML(message)
    message = f"{args}" + "\n"
    MessageE = discord.Embed(title="", description=message, colour = 0x12341)
    MessageE.set_image(url=argl)
    await SendHomeEML(MessageE)
    await SendMattEML(MessageE)
    await SendOZEML(MessageE)
    return

@bot.command(name='open')
async def createSignal(ctx, symbol = "", strike = "", callp = "", expiry = "", price = ""):
    message = "@everyone"
    message = sanitize(message)
    await SendHomeMML(message)
    #await SendDevenMML(message)
    green = discord.utils.get(bot.emojis, name='green')
    red = discord.utils.get(bot.emojis, name='red')
    d = date.today()
    strike = float(strike)
    price = float(price)
    cur.execute("""INSERT INTO Positions (date, status, symbol, strike, callp, expiry, price, pandl) Values (?,?,?,?,?,?,?,?)""",
                (d, 'Open', symbol, strike, callp, expiry, price, 0))
    con.commit()

    Message = symbol + " " + str(strike) + " " + callp + " " + expiry + " @" + str(price) + '\n\n'
    MessageE = discord.Embed(title = "**New Position**", description = Message, colour=1221312)



    #cur.execute("SELECT * FROM Positions")
    #k = cur.fetchall()
    #for row in k:
    #await SendHomeMML(k)

    await SendHomeEML(MessageE)
    await SendOZEML(MessageE)
    await SendMattEML(MessageE)
    return

@bot.command (name='showopen')
async def showopen(ctx):
    green = discord.utils.get(bot.emojis, name='green')
    red = discord.utils.get(bot.emojis, name='red')
    cur.execute("Select * From positions where status = ?",('Open',))
    k = cur.fetchall()
    desC = []
    for row in k:
        if(row[7]>=0.00):
            s = ""
            s += f"{green} " + str(row[1]) + " " + \
                 str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + \
                 " " + str(row[5]) + " " + str(row[6]) + " " + "|" + f" **P/L**: " + str(
                row[7]) + "%"
            desC.append(s)

        else:
            s = ""
            s += f"{red} " + str(row[1]) + " " + \
                 str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + \
                 " " + str(row[5]) + " " + str(row[6]) + " " + "|" + f" **P/L**: " + str(
                row[7]) + "%"
            desC.append(s)

    desP = '\n'.join(desC)
    message = '\n' + desP + '\n\n'
    MessageE = discord.Embed(title="***Current Open Positions***" + "\n" + "================", description = message, colour = 0x3432A1)
    await SendHomeEML(MessageE)
    await SendOZEML(MessageE)
    await SendMattEML(MessageE)
    return


@bot.command(name='todayPL')
async def todayPL(ctx):
    green = discord.utils.get(bot.emojis, name='green')
    red = discord.utils.get(bot.emojis, name='red')
    taabluedisc = discord.utils.get(bot.emojis, name='taabluedisc')
    cur.execute("Select * FROM positions where date = ?",(phDate,))
    temp = cur.fetchall()
    cur.execute("Select pandl FROM positions where date = ?", (phDate,))
    temp2 = cur.fetchall()
    desC = []

    for row in temp:
        if(row[7]>=0.00):
            s = ""
            s += f"{green} " + str(row[1]) + " " + \
                 str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + \
                 " " + str(row[5]) + " " + str(row[6]) + " " + "|" + f" **P/L**: " + str(
                row[7]) + "%"
            desC.append(s)

        else:
            s = ""
            s += f"{red} " + str(row[1]) + " " + \
                 str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + \
                 " " + str(row[5]) + " " + str(row[6]) + " " + "|" + f" **P/L**: " + str(
                row[7]) + "%"
            desC.append(s)

    desP = '\n'.join(desC)

    MessageE = discord.Embed(title=f"**Todays P/L** {green}", description=desP, colour=0xfa9324)
    await SendHomeEML(MessageE)
    await SendOZEML(MessageE)
    await SendMattEML(MessageE)
    return

@bot.command(name='showmonth')
async def showmonth(ctx, args):
    green = discord.utils.get(bot.emojis, name='green')
    red = discord.utils.get(bot.emojis, name='red')

    d = date.month
    cur.execute('''Select * From Positions Where date > ?''',(args, ))
    await ctx.channel.send('Showing positions from')
    k = cur.fetchall()
    desC = []
    for row in k:
        if(row[7]>=0.00):
            s = ""
            s += f"{green} " + str(row[1]) + " " + \
                 str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + \
                 " " + str(row[5]) + " " + str(row[6]) + " " + "|" + f" **P/L**: " + str(
                row[7]) + "%"
            desC.append(s)

        else:
            s = ""
            s += f"{red} " + str(row[1]) + " " + \
                 str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + \
                 " " + str(row[5]) + " " + str(row[6]) + " " + "|" + f" **P/L**: " + str(
                row[7]) + "%"
            desC.append(s)

    desP = '\n'.join(desC)

    MessageE = discord.Embed(title=f"**Monthly P/L** {green}", description=desP, colour=0xfa9324)
    await SendHomeEML(MessageE)
    await SendMattEML(MessageE)
    await SendOZEML(MessageE)

    return

@bot.command(name='close')
async def close(ctx, args, strike, expiry):
    cur.execute('''UPDATE Positions set status = ? where symbol = ? and strike = ? and expiry = ?''',('Closed', args, strike, expiry,))
    con.commit()
    message = "@everyone"
    message = sanitize(message)
    await SendHomeMML(message)
    await SendOZMML(message)
    #await SendDevenMML(message)
    messages = args + " " + strike + " " + expiry + '\n\n'
    MessageE = discord.Embed(title="***Closing position***", description=messages, colour = 0xAA4EB)
    await SendHomeEML(MessageE)
    await SendOZEML(MessageE)
    await SendMattEML(MessageE)
    await ctx.channel.send("Position Closed.")
    return

@bot.command(name='update')
async def update(ctx, symbol, strike, expiry, argv):
    green = discord.utils.get(bot.emojis, name='green')
    red = discord.utils.get(bot.emojis, name='red')
    cur.execute("Select price FROM positions where symbol = ? AND strike = ? AND expiry = ?",(symbol, strike, expiry))
    temp = cur.fetchone()
    temp = temp[0]
    temp = float(temp)
    temp = ((float(argv) / float(temp)) - 1) * 100
    temp = round(int(temp), 2)

    cur.execute("""UPDATE Positions set pandl = ? where symbol = ? and strike = ? AND expiry = ?""",(temp, symbol, strike, expiry))
    await ctx.channel.send("Position Updated.")
    con.commit()
    return



async def SendHomeEML(embedded):
    return await bot.get_channel(755488059537096804).send(embed=embedded)

async def SendOZEML(embedded):
    return await bot.get_channel(699780761745752154).send(embed=embedded)

async def SendOZMML(message):
    return await bot.get_channel(699780761745752154).send(message)

async def SendAtlasEML(embedded):
    return await bot.get_channel(736062290721374267).send(embed=embedded)

async def SendHomeMML(message):
    return await bot.get_channel(755488059537096804).send(message)

async def SendAtlasMML(message):
    return await bot.get_channel(736062290721374267).send(message)

async def SendDevenEML(message):
    return await bot.get_channel(782841568557793310).send(embed=message)

async def SendDevenMML(message):
    return await bot.get_channel(782841568557793310).send(message)

async def SendMattEML(message):
    return await bot.get_channel(783563415061921834).send(embed=message)

bot.run(token)