# Module Importieren
import sys
import os

aktueller_pfad = os.path.dirname(os.path.abspath(__file__))
module_verzeichnis = os.path.join(aktueller_pfad, 'module')
sys.path.append(module_verzeichnis)

from module.discord_module import *
from module.minecraft_module import *
from module.embed_module import *
from module.sql_module import *

# Regulärer Code
import discord
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
connected = False

@bot.event
async def on_ready():
    print("Bot ist online")
    check.start()
    await bot.tree.sync()

@bot.event
async def on_connect():
    global connected
    connected = True

@bot.event
async def on_disconnect():
    global connected
    connected = False

@tasks.loop(seconds=10.0)
async def check():
    if connected:
        # Player amount check
        try:
            amount = await check_minecraft_player_amount(get_setting('server-adress')['value'])
            channel = await bot.fetch_channel(str(get_setting('player-channel')['value']))
        
            if amount is not None:
                await channel.edit(name="Spieler: " + str(amount))
            else:
                await channel.edit(name="Spieler: 0")
            
        except Exception as e:
            message = "Es gibt einen Fehler bei der 'check_minecraft_player_amount' Abfrage! \nError: " + str(e)
            await send_log_message(message, bot, int(get_setting('logs-channel')["value"]))
        
        # Server online check
        try:
            status = await check_minecraft_server(get_setting('server-adress')['value'])
            channel = await bot.fetch_channel(str(get_setting('status-channel')['value']))
        
            if status is not None and status:
                await channel.edit(name="Status: 🟢Online")
            else:
                await channel.edit(name="Status: ⚫Offline")
            
        except Exception as e:
            message = "Es gibt einen Fehler bei der 'check_minecraft_player_amount' Abfrage! \nError: " + str(e)
            await send_log_message(message, bot, int(get_setting('logs-channel')["value"]))

bot.run(get_setting('bot-code')["value"])
