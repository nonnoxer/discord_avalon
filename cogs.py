from discord.ext import commands

class Avalon(commands.Cog):
    def __init__(self, bot, ctx, user):
        self.bot = bot
        self.ctx = ctx
        self.players = [user]
        self.host = user

    @commands.command()
    async def join(self, ctx):
        if ctx.author not in self.players and len(self.players) <= 10:
            self.players.append(ctx.author)
            await ctx.send(f"{ctx.author} has joined the game!\nPlayer slots: {len(self.players)} / 10")
        elif ctx.author in self.players:
            await ctx.send("You are already in the game.")
        else:
            await ctx.send("The game is full.")

    @commands.command()
    async def start(self, ctx):
        if ctx.author == self.host:
            if len(self.players) >= 5:
                await ctx.send(f"The game begins!\nPlayer count: {len(self.players)} / 10")
            else:
                await ctx.send(f"The game is too empty.\nPlayer slots: {len(self.players)} / 10")
        else:
            await ctx.send("You are not the host.")

class Round(commands.Cog):
    pass