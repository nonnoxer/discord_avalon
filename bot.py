import os

from discord.ext import commands

import cogs

TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord!")
    print(f"{bot.user} is connected to the following guilds:")
    for guild in bot.guilds:
        print(f'{guild.name} (id: {guild.id})')

@bot.command(name="avalon", help="Initiates a game of Avalon")
async def avalon(ctx):
    await ctx.send("Start a game of Avalon?")

@bot.event
async def on_command_error(ctx, error):
   pass

bot.run(TOKEN)
