import random
import string

from discord.ext import commands

from classes import Avalon

class AvalonBot(commands.Cog):
    """Cog for receiving commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avalon(self, ctx):
        """!avalon | Initiate a game of Avalon: """
        if ctx.author not in self.bot.players:
            game_id = "".join([random.choice(string.ascii_lowercase) for n in range(4)])
            while game_id in self.bot.games:
                game_id = "".join([random.choice(string.ascii_lowercase) for n in range(4)])
            self.bot.players[ctx.author] = game_id
            self.bot.games[game_id] = Avalon(self, ctx, ctx.author, game_id)
            await ctx.send(f"The game initiates! Type `!join {game_id}` to join the game.\nPlayer slots: 1 / 10")
        else:
            await ctx.send("You are already in a game.")

def setup(bot):
    bot.add_cog(AvalonBot(bot))