import logging
import os

from discord.ext import commands

import cogs

TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix='!')
bot.add_cog(cogs.AvalonBot(bot))

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord!")
    print(f"{bot.user} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f'{guild.name} (id: {guild.id})')

@bot.event
async def on_command_error(ctx, error):
    pass

bot.run(TOKEN)
