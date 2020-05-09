from discord.ext import commands

class InGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(InGame(bot))