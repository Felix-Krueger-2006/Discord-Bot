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

table_check()

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

@tasks.loop(seconds=300.0)
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
            message = "Es gibt einen Fehler bei der 'check_minecraft_player_amount' Abfrage!"
            await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
        
        # Server online check
        try:
            status = await check_minecraft_server(get_setting('server-adress')['value'])
            channel = await bot.fetch_channel(str(get_setting('status-channel')['value']))
            
            if status is not None and status:
                await channel.edit(name="Status: 🟢Online")
            else:
                await channel.edit(name="Status: ⚫Offline")
            
        except Exception as e:
            message = "Es gibt einen Fehler bei der 'check_minecraft_player_amount' Abfrage!"
            await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
            
        # Whitelist sort out
        try:
            channel = await bot.fetch_channel(str(get_setting('whitelist-channel')['value']))
            async for message in channel.history(limit=None):
                if message.embeds:
                    for embed in message.embeds:
                        if embed.fields:
                            for field in embed.fields:
                                if field.name == "Ingamename":
                                    new_embed = discord.Embed.from_dict(embed.to_dict())
                                    if not await name_check(await get_uuid_from_username(field.value)) and new_embed.color == discord.Color.green():
                                        new_embed.description = "Von der Whitelist entfernt."
                                        new_embed.color = discord.Colour(0x1c1c1c)
                                        new_embed.set_footer(text="Status: Entwhitelistet")
                                        
                                        await message.edit(embed=new_embed)        
        except Exception as e:
            message = "Es gibt einen Fehler bei der 'whitelist_sort_out' Funktion!"
            await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
            
        try:
            giveaway = await check_if_giveaway_starts()
            if giveaway != None and giveaway[9] <= 0:
                
                    try:
                        channel = bot.get_channel(int(get_setting("giveaway-channel")["value"]))
                        embed = await giveaway_embed(giveaway)
                        message = await channel.send(embed=embed)
                        await message.add_reaction("🎉")
                        await set_giveaway_on_active(giveaway, message.id)
                    except Exception as e:
                        message = "Es gibt einen Fehler bei der 'Giveaway Embed Send' Funktion!"
                        await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
        except Exception as e:
            message = "Es gibt einen Fehler bei der 'check_if_giveaway_starts' Funktion!"
            await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
            
        try:
            giveaway = await check_if_giveaway_ends()
            if giveaway != None and giveaway[10] <= 0:
                await set_giveaway_on_ends(giveaway)
                
                try:
                    channel = bot.get_channel(int(get_setting("giveaway-channel")["value"]))
                    message = channel.fetch_message(int(giveaway[11]))
                    user = await giveaway_solve(message, await winner_embed())
                    
                    await set_giveaway_winner(giveaway, user)
                    
                except Exception as e:
                    message = "Es gibt einen Fehler bei der 'Giveaway Ends' Funktion!"
                    await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
                    
        except Exception as e:
            message = "Es gibt einen Fehler bei der 'check_if_giveaway_starts' Funktion!"
            await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
            
        print("Loop Durchlauf")

@bot.tree.command()
async def whitelist(interaction: discord.Interaction, ingamename: str):
    try:
        if int(interaction.channel.id) == int(get_setting('whitelist-channel')["value"]):
            if not await user_already_in(interaction.user.id):
                if not await name_check(await get_uuid_from_username(ingamename)):
                    if await is_valid_minecraft_username(ingamename):
                        
                        try:
                            await add_user_to_whitelist(ingamename, await get_uuid_from_username(ingamename))
                        except Exception as e:
                            message = "Es gibt einen Fehler bei der 'add_user_to_whitelist' Funktion!"
                            return await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
                        
                        try:
                            if not await user_exist(interaction.user.id):
                                await add_user_to_table(interaction.user.id, await get_uuid_from_username(ingamename))
                            else:
                                await replace_user_in_table(await get_uuid_from_username(ingamename), interaction.user.id)
                        except Exception as e:
                            message = "Es gibt einen Fehler bei der 'add_user_to_table' Funktion!"
                            return await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
                        
                        embed = await whitelist_embed(interaction, ingamename)
                        await interaction.response.send_message(embed=embed)
                        
                    else:
                        await privat_message("Dieser Name ist kein existierender Minecraft Name!", interaction)
                else:
                    await privat_message("Dieser Spieler ist bereits in der Whitelist!", interaction)
            else:
                await privat_message("Du hast dich bereits in die Whitelist eingetragen!", interaction)
        else:
            await privat_message("Dies ist der falsche Channel für sowas!", interaction)
    except Exception as e:
        await privat_message("Es ist ein Fehler aufgetreten, versuche es nochmal!", interaction)
        print(f"Fehler in whitelist-Funktion: {e}")

@bot.event
async def on_message(ctx):
    
    try:
        if not ctx.author.bot and str(ctx.content[:10]).lower() == '!whitelist' and (ctx.author.guild_permissions.administrator or discord.utils.get(ctx.guild.roles, name="🔧 - Support") in ctx.author.roles):
            
            try:
                if str(ctx.content[11:15]).lower() == 'kick':
                    user = str(ctx.content[16:]).lower()
                    uuid = await get_uuid_from_username(user)
                    
                    if await name_check(uuid):
                        try:
                            await delete_user_from_whitelist(uuid)
                        except Exception as e:
                            message = "Es gibt einen Fehler bei der 'delete_user_from_whitelist' Funktion!"
                            return await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
                        
                        message = "Spieler: **" + str(ctx.content[16:]) + "** aka <@" + str(get_discord_id(uuid)) + "> \n\n<@" + str(ctx.author.id) + "> hat diesen Spieler manuel von der whitelist entfernt!"
                        await ctx.delete()
                        return await send_log_message(await log_embed(message, None), bot, int(get_setting('logs-channel')["value"]))
                    else:
                        message = "Dieser Spieler ist nicht auf der Whitelist!"
                        return await ctx_message(await ctx_message_embed(message), ctx)
        
            except Exception as e:
                message = "Es gibt einen Fehler bei der '!whitelist kick' Funktion!"
                await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
            
            try:
                if str(ctx.content[11:15]).lower() == 'show':
                    count = await count_whitelist()
                    embed = await limit_embed(count)
                    
                    message = await ctx.reply(embed=embed)
                    await ctx.delete()
                    await asyncio.sleep(10)
                    return await message.delete()
        
            except Exception as e:
                message = "Es gibt einen Fehler bei der '!whitelist show' Funktion!"
                await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
                
    except Exception as e:
        message = "Es gibt einen Fehler bei der '!whitelist' Funktion!"
        await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
    
    try:
        if not ctx.author.bot and str(ctx.content[:6]).lower() == '!clear' and (ctx.author.guild_permissions.administrator or discord.utils.get(ctx.guild.roles, name="🔧 - Support") in ctx.author.roles):
            if ctx.content[7:].isdigit():
                await ctx.channel.purge(limit=int(ctx.content[7:]) + 1)
                
                channel = discord.utils.get(ctx.guild.channels, name=str(ctx.channel.name))
                channel_mention = channel.mention if channel else "Kanal nicht gefunden"
                message = "Es wurden **" + ctx.content[7:] + " Nachrichten** in " + channel_mention + " von <@" + str(ctx.author.id) + "> gelöscht!"
                return await send_log_message(await log_embed(message, None), bot, int(get_setting('logs-channel')["value"]))
            
    except Exception as e:
        message = "Es gibt einen Fehler bei der '!clear' Funktion!"
        return await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))
    
    try:
        if not ctx.author.bot and int(ctx.channel.id) == int(get_setting('whitelist-channel')["value"]):
            return await ctx.delete()
        
    except Exception as e:
        message = f"Es gibt einen Fehler beim löschen der Nachrichten in <#{int(get_setting('logs-channel')["value"])}>!"
        return await send_log_message(await log_embed(message, e), bot, int(get_setting('logs-channel')["value"]))

    if int(ctx.channel.id) == int(get_setting("commands-channel")["value"]) and not ctx.author.bot:
        return await ctx.delete()

bot.run(get_setting('bot-code')["value"])
