class Player(object):
    def __init__(self, avalon, user, role):
        self.avalon = avalon
        self.user = user
        self.role = role
        if self.role % 3 == 0:
            self.loyalty = 1
        else:
            self.loyalty = 0
    
    async def night(self):
        await self.user.send(f"You are {self.avalon.REVERSE_ROLE_DICT[self.role]}.")
        if self.loyalty == 0 and self.role != 5:
            if len(self.avalon.role_config["evil"]) > 1:
                evil = ""
                for player in self.avalon.role_config["evil"]:
                    if player != self:
                        evil += f"\n{player.user.mention}"
                await self.user.send(f"Your fellow Minions of Mordred are:{evil}")
            else:
                await self.user.send(f"You are the only Minion of Mordred.")
        if self.role == 0:
            evil_visible = ""
            for player in self.avalon.role_config["evil_visible"]:
                evil_visible += f"\n{player.user.mention}"
            await self.user.send(f"The Minions of Mordred are:{evil_visible}")
        if self.role == 3:
            if len(self.avalon.role_config["percival"] == 0):
                await self.user.send("There is no Merlin.")
            elif len(self.avalon.role_config["percival"] == 1):
                await self.user.send(f"Merlin is {self.avalon.role_config[0].user.mention}")
            elif len(self.avalon.role_config["percival"] == 2):
                await self.user.send(f"Merlin is either {self.avalon.role_config[0].user.mention} or {self.avalon.role_config[1].user.mention}.")
            else:
                await self.user.send("why are there more than 2 merlins this is not supposed to happen raise an issue on github asap")
