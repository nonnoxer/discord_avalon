class Player(object):
    def __init__(self, avalon, player, role):
        self.avalon = avalon
        self.player = player
        self.role = role
        if self.role % 3 == 0:
            self.loyalty = 1
        else:
            self.loyalty = 0