import random

from classes.lobby import Lobby
from classes.player import Player
from classes.quest import Quest


class Avalon(object):
    """instance of Avalon game"""
    def __init__(self, cog, ctx, user, game_id):
        self.cog = cog
        self.ctx = ctx
        self.users = [user]
        self.host = user
        self.game_id = game_id
        self.state = 0 # Lobby phase
        self.lobby = Lobby(self)

        self.roles = [0, 1] # Merlin, Assassin
        self.ROLE_DICT = {"merlin": 0, "assassin": 1, "mordred": 2, "percival": 3, "morgana": 4, "oberon": 5} # loyal servant: -3, mordred minion: -1
        self.role_config = {}
        self.players = []

        self.quests = []

    def restrict_state(target_states):
        def restrict_state_decorator(func):
            async def restrict(self, *args, **kwargs):
                if self.state in target_states:
                    value = await func(self, *args)
                else:
                    value = await args[0].send("Invalid command for current game state.")
                return value
            return restrict
        return restrict_state_decorator

    @restrict_state(target_states=[0])
    async def join(self, ctx):
        await self.lobby.join(ctx)

    @restrict_state(target_states=[0])
    async def leave(self, ctx):
        await self.lobby.leave(ctx)

    @restrict_state(target_states=[0])
    async def start(self, ctx):
        await self.lobby.start(ctx)

    @restrict_state(target_states=[0])
    async def end(self, ctx):
        await self.lobby.end(ctx)

    @restrict_state(target_states=[0])
    async def add_role(self, ctx, roles):
        await self.lobby.add_role(ctx, roles)

    @restrict_state(target_states=[0])
    async def remove_role(self, ctx, roles):
        await self.lobby.remove_role(ctx, roles)
    
    @restrict_state(target_states=[0])
    async def make_host(self, ctx):
        await self.lobby.make_host(ctx)

    def start_game(self):
        random.shuffle(self.users)
        random.shuffle(self.roles)
        for i in range(len(self.users)):
            self.players.append(Player(self, self.users[i], self.roles[i]))
        self.state = 1

        self.role_config["evil"] = []
        for player in self.players:
            if player.loyalty == 0 and player.role != 5:
                self.role_config["evil"].append(player)
        if 0 in self.roles: # Merlin
            self.role_config["evil_visible"] = []
            for player in self.players:
                if player.loyalty == 0 and player.role != 2:
                    self.role_config["evil_visible"].append(player)
        if 3 in self.roles: # Percival
            self.role_config["percival_visible"] = []
            for player in self.players:
                if player.role % 4 == 0: # Morgana
                    self.role_config["percival_visible"].append(player)
        print(self.role_config)