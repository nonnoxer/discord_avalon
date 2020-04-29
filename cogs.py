import random
import string

import discord
from discord.ext import commands

from avalon import *


class AvalonBot(commands.Cog):
    """Cog for receiving commands"""
    def __init__(self, bot):
        self.bot = bot
        self.games = {} # {game_id: Avalon}
        self.players = {} # {user: game_id}
        
    @commands.command()
    async def avalon(self, ctx):
        """Initiate game of Avalon"""
        if ctx.author not in self.players:
            game_id = "".join([random.choice(string.ascii_lowercase) for n in range(4)])
            while game_id in self.games:
                game_id = "".join([random.choice(string.ascii_lowercase) for n in range(4)])
            self.players[ctx.author] = game_id
            self.games[game_id] = Avalon(ctx, ctx.author, game_id)
            await ctx.send(f"The game initiates! Type `!join {game_id}` to join the game.\nPlayer slots: 1 / 10")
        else:
            await ctx.send("You are already in a game.")

    @commands.command()
    async def join(self, ctx, game_id):
        """Join an initiated game of Avalon"""
        self.players[ctx.author] = game_id
        await self.games[game_id].join(ctx)

    @commands.command()
    async def leave(self, ctx):
        """Leave an initiated game of Avalon"""
        game_id = self.players[ctx.author]
        await self.games[game_id].leave(ctx)

    @commands.command()
    async def start(self, ctx):
        """Start an initiated game of Avalon"""
        game_id = self.players[ctx.author]
        await self.games[game_id].start(ctx)

    @commands.command()
    async def end(self, ctx):
        """End an initiated game of Avalon"""
        game_id = self.players[ctx.author]
        await self.games[game_id].end(ctx)

    @commands.command()
    async def test(self, ctx, test):
        await ctx.send(test)

class Avalon(object):
    """Separate instance of Avalon game"""
    def __init__(self, ctx, user, game_id):
        self.ctx = ctx
        self.players = [user]
        self.host = user
        self.game_id = game_id

    async def join(self, ctx):
        if ctx.author not in self.players and len(self.players) <= 10:
            self.players.append(ctx.author)
            await ctx.send(f"@{ctx.author} has joined the game!\nPlayer slots: {len(self.players)} / 10")
        elif ctx.author in self.players:
            await ctx.send("You are already in the game.")
        else:
            await ctx.send("The game is full.")

    async def leave(self, ctx):
        if ctx.author in self.players:
            self.players.remove(ctx.author)
            await ctx.send(f"@{ctx.author} has left the game.\nPlayer slots: {len(self.players)} / 10")
            if ctx.author == self.host and len(self.players) >= 2:
                self.host = self.players[0]
                await ctx.send(f"@{self.host} is now the host.")
            elif ctx.author == self.host:
                self.bot.remove_cog(self)
                await ctx.send(f"The game is empty, closing game.")
        else:
            await ctx.send("You are not in the game.")

    async def start(self, ctx):
        if ctx.author == self.host:
            if len(self.players) >= 5:
                await ctx.send(f"The game begins!\nPlayer count: {len(self.players)} / 10")
            else:
                await ctx.send(f"The game is too empty.\nPlayer slots: {len(self.players)} / 10")
        else:
            await ctx.send("You are not the host.")
