import random


class Player:
    is_alive = True
    voted_count = 0

    def __init__(self, role):
       self.role = role
    def vote(can_vote_players):
        selected_player = random.choice(can_vote_players)
        selected_player.voted_count += 1

class Wolf:
    def select_voting():
        pass
    def night_act(myself_player):
        return  randomwwes.choice(survivor.remove(myself_player))
        

class Villager:
    def select_voting():
        pass

class FortuneTeller:
    def select_voting():
        pass
    def night_act(can_fotune_telling_players):
        return random.choice(can_fotune_telling_players).role


def vote():
    pass

survivor = [
    Player(Wolf),
    Player(Villager),
    Player(Villager),
    Player(FortuneTeller)
]       