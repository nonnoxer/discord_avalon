from discord.ext import commands

from classes import Avalon

class Lobby(commands.Cog):
    """Cog for receiving commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, game_id):
        """!join <game_id> | Join initiated game"""
        await self.bot.games[game_id].join(ctx)

    @commands.command()
    async def leave(self, ctx):
        """!leave | Leave initiated game"""
        game_id = self.bot.players[ctx.author]
        await self.bot.games[game_id].leave(ctx)

    @commands.command()
    async def start(self, ctx):
        """!start | Start initiated game (host only)"""
        game_id = self.bot.players[ctx.author]
        await self.bot.games[game_id].start(ctx)

    @commands.command()
    async def end(self, ctx):
        """!end | End initiated game (host only)"""
        game_id = self.bot.players[ctx.author]
        await self.bot.games[game_id].end(ctx)

    @commands.command()
    async def add_role(self, ctx, *args):
        """!add_role <roles> | Add specified roles to initiated game (host only)"""
        game_id = self.bot.players[ctx.author]
        await self.bot.games[game_id].add_role(ctx, args)

    @commands.command()
    async def remove_role(self, ctx, *args):
        """!remove_role <roles> | Remove specified roles from initiated game (host only)"""
        game_id = self.bot.players[ctx.author]
        await self.bot.games[game_id].remove_role(ctx, args)

    @commands.command()
    async def make_host(self, ctx):
        """!make_host <mention> | Makes mentioned player the host of an initiated game (host only)"""
        game_id = self.bot.players[ctx.author]
        await self.bot.games[game_id].end(ctx)

def setup(bot):
    bot.add_cog(Lobby(bot))