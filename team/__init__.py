
from pelita.player import SimpleTeam
from .demo_player import KangarooPlayer
# (please use relative imports inside your module)

# The default factory method, which this module must export.
# It must return an instance of `SimpleTeam`  containing
# the name of the team and the respective instances for
# the first and second player.

def team():
    return SimpleTeam("Drunk Team", KangarooPlayer(), KangarooPlayer())

# For testing purposes, one may use alternate factory methods::
#
#     def alternate_factory():
#          return SimpleTeam("Our alternate Team", AlternatePlayer(), AlternatePlayer())
#
# To be used as follows::
#
#     $ pelita path_to/groupN/:alternate_factory
