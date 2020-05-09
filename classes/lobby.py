from classes.player import Player


class Lobby(object):
    def __init__(self, avalon):
        self.avalon = avalon

    def host_only(func):
        async def restrict(self, *args, **kwargs):
            if self.avalon.host == args[0].author:
                value = await func(self, *args)
            else:
                value = await args[0].send("You are not the host.")
            return value
        return restrict

    async def join(self, ctx):
        if ctx.author not in self.avalon.cog.bot.players and ctx.author not in self.avalon.users and len(self.avalon.users) <= 10:
            self.avalon.cog.bot.players[ctx.author] = self.avalon.game_id
            self.avalon.users.append(ctx.author)
            await self.avalon.dm_users(f"{ctx.author.mention} has joined the game!\nPlayer slots: {len(self.avalon.users)} / 10")
        elif ctx.author in self.avalon.cog.bot.players:
            await ctx.send("You are already in a game.")
        elif ctx.author in self.avalon.users:
            await ctx.send("You are already in the game.")
        else:
            await ctx.send("The game is full.")

    async def leave(self, ctx):
        if ctx.author in self.avalon.users:
            self.avalon.users.remove(ctx.author)
            del self.avalon.cog.bot.players[ctx.author]
            await self.avalon.dm_users(f"{ctx.author.mention} has left the game.\nPlayer slots: {len(self.avalon.users)} / 10")
            if ctx.author == self.avalon.host and len(self.avalon.users) >= 1:
                self.avalon.host = self.avalon.users[0]
                await self.avalon.dm_users(f"{self.avalon.host.mention} is now the host.")
            elif ctx.author == self.avalon.host:
                await self.avalon.dm_users(f"The game is empty, closing game.")
                del self.avalon.cog.bot.games[self.avalon.game_id]
        else:
            await ctx.send("You are not in the game.")

    @host_only
    async def start(self, ctx):
        if len(self.avalon.users) >= 3: # CHANGE THIS LATER
            good_special_roles, evil_special_roles = 0, 0
            for role in self.avalon.roles:
                if role % 3 == 0:
                    good_special_roles += 1
                else:
                    evil_special_roles += 1
            good_roles = len(self.avalon.users) * 2 // 3
            evil_roles = len(self.avalon.users) - good_roles
            if good_special_roles <= good_roles and evil_special_roles <= evil_roles:
                await self.avalon.dm_users(f"The game begins!\nPlayer slots: {len(self.avalon.users)} / 10")
                while good_special_roles < good_roles:
                    self.avalon.roles.append(-3)
                    good_special_roles += 1
                while evil_special_roles < evil_roles:
                    self.avalon.roles.append(-1)
                await self.avalon.night()
            else:
                await ctx.send(f"You have too many roles. You have:\n{good_special_roles} good roles for {good_roles} good slots\n{evil_special_roles} evil roles for {evil_roles} evil slots\nUse `!remove_role <roles>` then try again.")
        else:
            await ctx.send(f"The game is too empty.\nPlayer slots: {len(self.avalon.users)} / 10")

    @host_only
    async def end(self, ctx):
        await self.avalon.dm_users("The game has been ended by the host.")
        new_players = {}
        for player, game_id in self.avalon.cog.bot.players.items():
            if game_id != self.avalon.game_id:
                new_players[player] = game_id
        self.avalon.cog.bot.players = new_players
        del self.avalon.cog.bot.games[self.avalon.game_id]

    @host_only
    async def add_role(self, ctx, roles):
        if len(roles) == 0:
            await ctx.send("No role specified.")
        else:
            for role in roles:
                valid = False
                try:
                    raw_role = int(role)
                    if raw_role >= 0 and raw_role <= 5:
                        valid = True
                except:
                    if role.lower() in self.avalon.ROLE_DICT:
                        raw_role = self.avalon.ROLE_DICT[role.lower()]
                        valid = True
                if valid:
                    if raw_role in self.avalon.roles:
                        await ctx.send(f"{role.title()} has already been added to the game.")
                    else:
                        await self.avalon.dm_users(f"{role.title()} has been added to the game.")
                        self.avalon.roles.append(raw_role)
                else:
                    await ctx.send(f"{role} is an invalid role.")

    @host_only
    async def remove_role(self, ctx, roles):
        if len(roles) == 0:
            await ctx.send("No role specified.")
        else:
            for role in roles:
                valid = False
                try:
                    raw_role = int(role)
                    if raw_role >= 0 and raw_role <= 5:
                        valid = True
                except:
                    if role.lower() in self.avalon.ROLE_DICT:
                        raw_role = self.avalon.ROLE_DICT[role.lower()]
                        valid = True
                if valid:
                    if raw_role in self.avalon.roles:
                        await self.avalon.dm_users(f"{role.title()} has been removed from the game.")
                        self.avalon.roles.remove(raw_role)
                    else:
                        await ctx.send(f"{role.title()} has not been added to the game.")
                else:
                    await ctx.send(f"{role} is an invalid role.")

    @host_only
    async def make_host(self, ctx):
        if len(ctx.message.mentions) == 1:
            await self.avalon.dm_users(f"{ctx.message.mentions[0]} is now the host.")
            self.avalon.host = ctx.message.mentions[0]
        else:
            await ctx.send("Please give a valid mention.")
