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
    await ctx.send("Start a game of Avalon? [Y]es/[N]o")
    def check(message):
        return message.author == ctx.author
    reply = await bot.wait_for("message", check=check)
    reply_content = reply.content.lower()
    if reply_content == "y" or reply_content == "yes":
        await ctx.send("The quest begins!")
    elif reply_content == "n" or reply_content == "no":
        await ctx.send("Another day then.")
    else:
        await ctx.send("You speak in riddles.")

@bot.event
async def on_command_error(ctx, error):
   pass

bot.run(TOKEN)
