
from pelita.player import AbstractPlayer
from pelita.datamodel import stop

# use relative imports for things inside your module
from .utils import utility_function


class ReporterPlayer(AbstractPlayer):
    """Like KangarooPlayer, but reports data read from game server etc."""

    memory = 0

    def __init__(self):
        self.sleep_rounds = 0

    def set_initial(self):
        print("Universe:")
        print(self.current_uni.pretty)

    def check_pause(self):
        # make a pause every fourth step because it is too hot to jump
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            texts = ["40°C", "Too hot", "Too tired", "Too lazy"]
            self.say(self.rnd.choice(texts))
            return stop

    def report(self):
        print("***Report***")
        print("**Universe")
        print(self.current_uni.pretty)
        print("**Legal moves")
        print(self.legal_moves)
        print("**Current position")
        print(self.current_pos)
        print("**Enemy food")
        print(self.enemy_food)
        print("**Previous position")
        print(self.previous_pos)
        print("**Team")
        print(self.team)
        print("**Team border")
        print(self.team_border)
        print("**Enemy bots")
        print(self.enemy_bots)
        print("***End report***")

    def get_move(self):
        self.report()
        self.check_pause()

        # legal_moves returns a dict {move: position}
        # we always need to return a move
        possible_moves = list(self.legal_moves.keys())
        # selecting one of the moves
        return self.rnd.choice(possible_moves)

class KangarooPlayer(AbstractPlayer):
    """ Jumps in random directions. """

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0

    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        print(self.current_uni.pretty)

    def check_pause(self):
        # make a pause every fourth step because it is too hot to jump
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            texts = ["40°C", "Too hot", "Too tired", "Too lazy"]
            self.say(self.rnd.choice(texts))
            return stop

    def get_move(self):
        utility_function()

        self.check_pause()

        # legal_moves returns a dict {move: position}
        # we always need to return a move
        possible_moves = list(self.legal_moves.keys())
        # selecting one of the moves
        return self.rnd.choice(possible_moves)
