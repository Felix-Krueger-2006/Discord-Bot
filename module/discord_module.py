import asyncio, discord, random

async def privat_message(message: str, interaction):
    await interaction.response.send_message(message, ephemeral=True)
    await asyncio.sleep(5)
    await interaction.delete_original_response()
    
async def ctx_message(embed, ctx):
    reponse = await ctx.channel.send(embed=embed)
    await ctx.delete()
    await asyncio.sleep(5)
    await reponse.delete()
    
async def send_log_message(embed, bot, channel: int):
    try:
        channel = bot.get_channel(channel)
        await channel.send(embed=embed)
    except:
        print("Es gibt einen Fehler bei der 'send_log_message()' funktion")
        
async def giveaway_solve(message, embed):
    users= []
    
    updated_embed = discord.Embed.from_dict(message.embeds[0].to_dict())
    updated_embed.color = discord.Colour.red()
    await message.edit(embed=updated_embed)
                        
    reactions = message.reactions
    for reaction in reactions:
        async for user in reaction.users():
            users.append(user)
    
    max_number = len(users) - 1
    number = random.randint(1, max_number)
            
    if max_number > 1:
        await users[number].send(embed=embed)
    else:
        await users[1].send(embed=embed)
        
    return users[number]
    