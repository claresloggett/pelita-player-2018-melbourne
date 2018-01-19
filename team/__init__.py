
from pelita.player import SimpleTeam
from .demo_player import KangarooPlayer, ReporterPlayer
from .player import NNPlayer
# (please use relative imports inside your module)

# The default team factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def team():
    return SimpleTeam("Test Team", NNPlayer(), NNPlayer())

# For testing purposes, one may use alternate factory methods::
#
#     def alternate_team():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ pelita path_to/groupN/:alternate_team
