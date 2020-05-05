import random
import string

import discord
from discord.ext import commands

from classes import Avalon, Lobby, Quest

class AvalonBot(commands.Cog):
    """Cog for receiving commands"""
    def __init__(self, bot):
        self.bot = bot
        self.games = {} # {game_id: Avalon}
        self.players = {} # {user: game_id}
        
    @commands.command()
    async def avalon(self, ctx):
        """start | Initiate game of Avalon: """
        if ctx.author not in self.players:
            game_id = "".join([random.choice(string.ascii_lowercase) for n in range(4)])
            while game_id in self.games:
                game_id = "".join([random.choice(string.ascii_lowercase) for n in range(4)])
            self.players[ctx.author] = game_id
            self.games[game_id] = Avalon(self, ctx, ctx.author, game_id)
            await ctx.send(f"The game initiates! Type `!join {game_id}` to join the game.\nPlayer slots: 1 / 10")
        else:
            await ctx.send("You are already in a game.")

    @commands.command()
    async def join(self, ctx, game_id):
        """!join <game_id> | Join initiated game"""
        self.players[ctx.author] = game_id
        await self.games[game_id].join(ctx)

    @commands.command()
    async def leave(self, ctx):
        """!leave | Leave initiated game"""
        game_id = self.players[ctx.author]
        await self.games[game_id].leave(ctx)

    @commands.command()
    async def start(self, ctx):
        """!start | Start initiated game (host only)"""
        game_id = self.players[ctx.author]
        await self.games[game_id].start(ctx)

    @commands.command()
    async def end(self, ctx):
        """!end | End initiated game (host only)"""
        game_id = self.players[ctx.author]
        await self.games[game_id].end(ctx)

    @commands.command()
    async def add_role(self, ctx, *args):
        """!add_role <roles> | Add specified roles to initiated game (host only)"""
        game_id = self.players[ctx.author]
        await self.games[game_id].add_role(ctx, args)

    @commands.command()
    async def remove_role(self, ctx, *args):
        """!remove_role <roles> | Remove specified roles from initiated game (host only)"""
        game_id = self.players[ctx.author]
        await self.games[game_id].remove_role(ctx, args)

    @commands.command()
    async def make_host(self, ctx):
        """!make_host <mention> | Makes mentioned player the host of an initiated game (host only)"""
        game_id = self.players[ctx.author]
        await self.games[game_id].end(ctx)

    @commands.command()
    async def test(self, ctx):
        print(self.games)
        print(self.players)