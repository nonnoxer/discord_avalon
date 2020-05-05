from classes.player import Player


class Lobby(object):
    def __init__(self, avalon):
        self.avalon = avalon

    async def join(self, ctx):
        if ctx.author not in self.avalon.players and len(self.avalon.players) <= 10:
            self.avalon.players.append(ctx.author)
            await ctx.send(f"{ctx.author.mention} has joined the game!\nPlayer slots: {len(self.avalon.players)} / 10")
        elif ctx.author in self.avalon.players:
            await ctx.send("You are already in the game.")
        else:
            await ctx.send("The game is full.")

    async def leave(self, ctx):
        if ctx.author in self.avalon.players:
            self.avalon.players.remove(ctx.author)
            del self.avalon.cog.players[ctx.author]
            await ctx.send(f"{ctx.author.mention} has left the game.\nPlayer slots: {len(self.avalon.players)} / 10")
            if ctx.author == self.avalon.host and len(self.avalon.players) >= 1:
                self.avalon.host = self.avalon.players[0]
                await ctx.send(f"{self.avalon.host.mention} is now the host.")
            elif ctx.author == self.avalon.host:
                await ctx.send(f"The game is empty, closing game.")
                del self.avalon.cog.games[self.avalon.game_id]
        else:
            await ctx.send("You are not in the game.")

    async def start(self, ctx):
        if len(self.avalon.players) >= 3: # CHANGE THIS LATER
            good_special_roles, evil_special_roles = 0, 0
            for role in self.avalon.roles:
                if role % 3 == 0:
                    good_special_roles += 1
                    self.avalon.role_config["good"].append(role)
                else:
                    evil_special_roles += 1
                    self.avalon.role_config["evil"].append(role)
            good_roles = len(self.avalon.players) * 2 // 3
            evil_roles = len(self.avalon.players) - good_roles
            if good_special_roles <= good_roles and evil_special_roles <= evil_roles:
                await ctx.send(f"The game begins!\nPlayer count: {len(self.avalon.players)} / 10")
                while good_special_roles < good_roles:
                    self.avalon.role_config["good"].append(-1)
                    good_special_roles += 1
                while evil_special_roles < evil_roles:
                    self.avalon.role_config["evil"].append(-1)
                self.avalon.state = 1
                print(self.avalon.role_config)
            else:
                await ctx.send(f"You have too many roles. You have:\n{good_special_roles} good roles for {good_roles} good slots\n{evil_special_roles} evil roles for {evil_roles} evil slots\nUse `!remove_role <roles>` then try again.")
        else:
            await ctx.send(f"The game is too empty.\nPlayer slots: {len(self.avalon.players)} / 10")

    async def end(self, ctx):
        await ctx.send("The game has been ended by the host.")
        del self.avalon.cog.games[self.avalon.game_id]
        for player, game_id in self.avalon.cog.players.items():
            if game_id == self.avalon.game_id:
                del self.avalon.cog.players[player]

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
                        await ctx.send(f"{role} has already been added to the game.")
                    else:
                        await ctx.send(f"{role} has been added to the game.")
                        self.avalon.roles.append(raw_role)
                else:
                    await ctx.send(f"{role} is an invalid role.")

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
                        await ctx.send(f"{role} has been removed from the game.")
                        self.avalon.roles.remove(raw_role)
                    else:
                        await ctx.send(f"{role} has not been added to the game.")
                else:
                    await ctx.send(f"{role} is an invalid role.")

    async def make_host(self, ctx):
        if len(ctx.message.mentions) == 1:
            await ctx.send(f"{ctx.message.mentions[0]} is now the host.")
            self.avalon.host = ctx.message.mentions[0]
        else:
            await ctx.send("Please give a valid mention.")
