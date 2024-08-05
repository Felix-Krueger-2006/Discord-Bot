import asyncio

async def privat_message(message: str, interaction: object):
    await interaction.response.send_message(message, ephemeral=True)
    await asyncio.sleep(5)
    await interaction.delete_original_response()
    
async def send_log_message(message: str, bot: object, channel: int):
    try:
        channel = bot.get_channel(channel)
        await channel.send(message)
    except:
        print("Es gibt einen Fehler bei der 'send_log_message()' funktion")