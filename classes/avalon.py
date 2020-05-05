from classes.lobby import Lobby
from classes.player import Player
from classes.quest import Quest


class Avalon(object):
    """instance of Avalon game"""
    def __init__(self, cog, ctx, user, game_id):
        self.cog = cog
        self.ctx = ctx
        self.players = [user]
        self.host = user
        self.game_id = game_id

        self.state = 0 # Lobby phase
        self.lobby = Lobby(self)
        self.roles = [0, 1] # Merlin, Assassin
        self.ROLE_DICT = {"merlin": 0, "assassin": 1, "mordred": 2, "percival": 3, "morgana": 4, "oberon": 5}
        self.role_config = {"good": [], "evil": []}

    def restrict_state(target_state):
        def restrict_state_decorator(func):
            async def restrict(self, *args, **kwargs):
                if self.state == target_state:
                    value = await func(self, *args)
                else:
                    value = await args[0].send("Invalid command for current game state.")
                return value
            return restrict
        return restrict_state_decorator

    def host_only(func):
        async def restrict(self, *args, **kwargs):
            if self.host == args[0].author:
                value = await func(self, *args)
            else:
                value = await args[0].send("You are not the host.")
            return value
        return restrict

    @restrict_state(target_state=0)
    async def join(self, ctx):
        await self.lobby.join(ctx)

    @restrict_state(target_state=0)
    async def leave(self, ctx):
        await self.lobby.leave(ctx)

    @restrict_state(target_state=0)
    @host_only
    async def start(self, ctx):
        await self.lobby.start(ctx)

    @restrict_state(target_state=0)
    @host_only
    async def end(self, ctx):
        await self.lobby.end(ctx)

    @restrict_state(target_state=0)
    @host_only
    async def add_role(self, ctx, roles):
        await self.lobby.add_role(ctx, roles)

    @restrict_state(target_state=0)
    @host_only
    async def remove_role(self, ctx, roles):
        await self.lobby.remove_role(ctx, roles)
    
    @restrict_state(target_state=0)
    @host_only
    async def make_host(self, ctx):
        await self.lobby.make_host(ctx)
