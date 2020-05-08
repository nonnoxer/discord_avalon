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
        self.ROLE_DICT = {"merlin": 0, "assassin": 1, "mordred": 2,
            "percival": 3, "morgana": 4, "oberon": 5}
        self.REVERSE_ROLE_DICT = {-3: "a Loyal Servant of Arthur",
            -1: "a Minion of Mordred", 0: "Merlin", 1: "Assassin",
            2: "Mordred", 3: "Percival", 4: "Morgana", 5: "Oberon"}
        self.role_config = {}
        self.players = []

        self.quests = []
        self.QUEST_DICT = {3: [1, 2, 2, 1, 2], 5: [2, 3, 2, 3, 3],
            6: [2, 3, 4, 3, 4], 7: [2, 3, 3, 4, 4], 8: [3, 4, 4, 5, 5],
            9: [3, 4, 4, 5, 5], 10: [3, 4, 4, 5, 5]}

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

    async def dm_users(self, dm):
        for user in self.users:
            await user.send(dm)

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

    async def night(self):
        random.shuffle(self.users)
        random.shuffle(self.roles)
        for i in range(len(self.users)):
            self.players.append(Player(self, self.users[i], self.roles[i]))
        player_order = ""
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
        for player in self.players:
            await player.night()
        for i in range(5): # Generate quests
            self.quests.append(Quest(self, self.QUEST_DICT[len(self.players)][i]))
            if i == 4 and len(self.players) >= 7:
                self.quests[3].fail = 2
        print(self.quests)
        self.state = 2