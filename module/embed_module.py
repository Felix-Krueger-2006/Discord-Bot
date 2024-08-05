import discord

async def winner_embed(image: str, author: str):
    embed = discord.Embed(
        title= "Gewinnspiel",
        description= "Herzlichen Glückwunsch! \n\nDu hast beim Gewinnspiel gewonnen! Um deinen fantastischen Gewinn zu erhalten, schick uns einfach deine Daten. Öffne dazu ein Ticket auf unserem Discord-Server und lass uns von dir hören. Wir können es kaum erwarten, dir deinen Preis zu überreichen! \n\nMit Abenteuerlichen Grüßen \nDas PixelSeasons Team",
        color=discord.Color.green()
    )
            
    embed.set_image(url=image)
    embed.set_footer(text="Gesponsort by " + author)
    
    return embed
        
async def whitelist_embed(user: object, ingamename: str, ):
    embed = discord.Embed(
        title="Whitelist Antrag für den Server",
        description="Du wurdest Gewhitelistet, \nviel Spaß auf dem Server.",
        color=discord.Color.green()
    )
    
    embed.set_footer(text="Status: Gewhitelistet")
    embed.add_field(name="Discord Name", value=user.mention)
    embed.add_field(name="Ingamename", value=ingamename)
    embed.set_thumbnail(url=user.display_avatar.url)
    
    return embed