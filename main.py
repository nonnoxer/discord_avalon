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
    await ctx.send("Initiate a game of Avalon? [Y]es/[N]o")
    def check(message):
        return message.author == ctx.author
    reply = await bot.wait_for("message", check=check)
    reply_content = reply.content.lower()
    if reply_content == "y" or reply_content == "yes":
        await ctx.send("The game initiates! Type `!join` to join the game.\nPlayer slots: 1 / 10")
        bot.add_cog(cogs.Avalon(bot, ctx, ctx.author))
    else:
        await ctx.send("Another day then.")

@bot.event
async def on_command_error(ctx, error):
   pass

bot.run(TOKEN)
