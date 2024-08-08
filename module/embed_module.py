import discord

async def winner_embed(liste):
    embed = discord.Embed(
        title= "Gewinnspiel",
        description= "Herzlichen Glückwunsch! \n\nDu hast beim Gewinnspiel gewonnen! Um deinen fantastischen Gewinn zu erhalten, schick uns einfach deine Daten. Öffne dazu ein Ticket auf unserem Discord-Server und lass uns von dir hören. Wir können es kaum erwarten, dir deinen Preis zu überreichen! \n\nMit Abenteuerlichen Grüßen \nDas PixelSeasons Team",
        color=discord.Color.green()
    )
            
    embed.set_image(url=liste[4])
    embed.set_footer(text="Gesponsort by " + str(liste[1]))
    
    return embed
        
async def whitelist_embed(interaction, ingamename: str):
    embed = discord.Embed(
        title="Whitelist Antrag für den Server",
        description="Du wurdest gewhitelistet, \nviel Spaß auf dem Server.",
        color=discord.Color.green()
    )
    
    embed.set_footer(text="Status: Gewhitelistet")
    embed.add_field(name="Discord Name", value=interaction.user.mention)
    embed.add_field(name="Ingamename", value=ingamename)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    
    return embed

async def log_embed(message, error):
    embed = None
    
    if error != "" and error != None:
        embed = discord.Embed(
            title= "Fehler Benachrichtigung",
            description= f"**{message}\n\nError:**\n > " + str(error),
            color=discord.Color(0xf54254)
        )
    else:
        embed = discord.Embed(
            title= "System Benachrichtigung",
            description= message,
            color=discord.Color(0x237feb)
        )
    
    return embed

async def ctx_message_embed(message):
    embed = discord.Embed(
        description= message,
        color=discord.Color.yellow()
    )
    
    return embed

async def giveaway_embed(liste):
    embed = discord.Embed(
        title=str(liste[2]),
        description=str(liste[3]),
        color=discord.Color.green()
    )
    embed.set_footer(text="Gesponsort by " + str(liste[1]))
    embed.set_image(url=str(liste[4]))
    
    return embed

async def limit_embed(count):
    message = "Auf der Whitelist sind momentan  **" + str(count) + "**  Spieler gelistet."
    embed = discord.Embed(
        title= "Whitelist ist bei...",
        description= message,
        color=discord.Color(0x237feb)
    )
    
    return embed