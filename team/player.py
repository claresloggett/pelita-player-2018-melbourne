
import numpy as np

from pelita.player import AbstractPlayer
from pelita.datamodel import stop, north, south, east, west

# use relative imports for things inside your module
from .utils import utility_function

def relu(z):
    a = np.zeros_like(z)
    mask = z > 0
    a[mask] = z[mask]
    return a

def sigmoid(z):
    a = 1 / (1 + np.exp(-z))
    return a

class NNPlayer(AbstractPlayer):

    vision_radius = 3

    def __init__(self):
        # For now, set any weights to random values
        # TODO: add legal_outputs as an input to the output layre
        #print("Creating player")
        self.output_moves = [stop, north, south, east, west]

        zone_numinputs = 2  # own zone, west zone
        maze_numinputs = (2*self.vision_radius+1)**2
        food_numinputs = maze_numinputs
        enemy_numinputs = maze_numinputs
        noise_numinputs = maze_numinputs
        team_numinputs = maze_numinputs
        #print("Expected input sizes",[zone_numinputs,
        #                              maze_numinputs,
        #                              food_numinputs,
        #                              enemy_numinputs,
        #                              noise_numinputs,
        #                              team_numinputs])
        num_inputs = zone_numinputs + maze_numinputs + food_numinputs + \
                     enemy_numinputs + noise_numinputs + team_numinputs
        num_outputs = len(self.output_moves)
        self.layer_spec = [num_inputs, 10, 8, num_outputs]
        # Do not apply to first layer, i.e. inputs
        self.layer_funcs = [relu, relu, sigmoid]
        self.weights = []
        self.intercepts = []
        for i in range(1, len(self.layer_spec)):
            # random numbers with variance 1/N, where N is the number of inputs
            # TODO: some inputs are sparse, do we need to adjust first layer variance?
            A, B = self.layer_spec[i-1], self.layer_spec[i]
            self.weights.append(np.random.randn(B,A)/np.sqrt(A))
            self.intercepts.append(np.zeros((B,1)))
        #print("Weights shapes",[m.shape for m in self.weights])
        #print((weights[1] @ weights[0]).shape)
        #fake_input = np.random.randn(num_inputs)
        #print((weights[0] @ fake_input + intercepts[0]).shape)

    def set_initial(self):
        #print("Initialising")
        self.walls_arr = self.maze_to_numpy()
        #print(self.walls_arr)

    # OR: everything done in coordinates relative to self?
    #     then do e.g. 10 closest food pieces
    # Data
    # - which side of map I am on (mine/enemy) - me.in_own_zone.
    #                                       Same as me.is_destroyer
    # - which side of map (west/east) - me.on_west_side
    # - walls vision
    # - enemy food vision
    # - enemy bot vision
    # - enemy bot noise vision
    # - teammate vision
    # - map out of sight quantity, each octant
    # - food out of sight quantity, each octant
    # - coordinates?
    def get_move(self):
        #print("Starting move")
        #return self.output_moves[np.random.randint(5)]
        x,y = self.current_pos
        # view around centre x+vision_radius; so from (x) to (x+2*vision_radius+1)
        xmax = x+2*self.vision_radius+1
        ymax = y+2*self.vision_radius+1

        zone_inputs = np.array([self.me.in_own_zone, self.me.on_west_side], dtype=np.int8)
        #print(zone_inputs)

        see_walls = self.walls_arr[x:xmax, y:ymax]
        #print("Position {}. I see walls:".format((x,y)))
        #print(see_walls)

        #print(see_walls.ravel())

        see_food = self.food_to_numpy(self.enemy_food)[x:xmax, y:ymax]
        #print("I see food")
        #print(see_food)
        #print(see_food.ravel())

        see_enemy, see_noise = self.bots_to_numpy(self.enemy_bots, enemy=True)
        see_enemy = see_enemy[x:xmax, y:ymax]
        see_noise = see_noise[x:xmax, y:ymax]

        #print("I see enemies")
        #print(see_enemy)
        #print(see_enemy.ravel())

        see_team = self.bots_to_numpy(self.other_team_bots, enemy=False)[x:xmax, y:ymax]

        #print("I see friends")
        #print(see_team)
        #print(see_team.ravel())

        #print("Input sizes",[inp.shape for inp in [zone_inputs,
        #                                           see_walls.ravel(),
        #                                           see_food.ravel(),
        #                                           see_enemy.ravel(),
        #                                           see_noise.ravel(),
        #                                           see_team.ravel()]])

        inputs = np.concatenate([zone_inputs,
                                 see_walls.ravel(),
                                 see_food.ravel(),
                                 see_enemy.ravel(),
                                 see_noise.ravel(),
                                 see_team.ravel()])

        #print("Inputs",inputs.shape)

        outputs = self.apply_nn(inputs[:,np.newaxis]).squeeze()
        #print(outputs)
        #print(np.argmax(outputs))
        #print("Time",self.time_spent())

        # Return highest-rated legal move, since illegal moves disqualify us

        # if numpy 1.13.0
        #is_legal = np.isin(self.output_moves, self.legal_moves)
        #return self.output_moves[is_legal][np.argmax(outputs[is_legal])]

        legal_moves = set(self.legal_moves)
        score_move_pairs = [(prob, move) for (prob, move) in zip(outputs,self.output_moves)
                            if (move in legal_moves)]
        scores, moves = zip(*score_move_pairs)
        return moves[np.argmax(scores)]

    def apply_nn(self, inputs):
        #print("Applying NN")
        x = inputs
        #i = 1
        #print(len(self.weights), len(self.intercepts), len(self.layer_funcs))
        for (w, b, activation) in zip(self.weights, self.intercepts, self.layer_funcs):
            #print("Layer",i)
            #i += 1
            z = w @ x + b
            #print(z.shape, w.shape, x.shape, b.shape)
            x = activation(z)
            #print("Size of activations now",x.shape)
        return x


    def maze_to_numpy(self):
        # this assumes we are inside `set_initial` or `get_move`
        maze = self.current_uni.maze
        # create an empty numpy matrix with the same size as the maze
        walls_np = np.zeros(shape=(maze.width, maze.height), dtype=np.int8)
        # maze items iterates over the position and the value at this position
        for (i, j), v in maze.items():
            # v == True means there is a wall, False means free space
            walls_np[i, j] = v
        # pad the maze with the max distance we will ever look. Assume we could
        # stand at the edge (even though we can only stand one from the edge).
        walls_np = np.pad(walls_np, self.vision_radius, 'constant', constant_values=1)
        return walls_np

    # TODO: ignore points outside vision for efficiency?
    def food_to_numpy(self, foodlist):
        # pass in e.g. self.enemy_food
        # assumes self.walls_arr is set, to get maze dimensions
        food_arr = np.zeros_like(self.walls_arr, dtype=np.int8)
        for (x,y) in foodlist:
            food_arr[x+self.vision_radius, y+self.vision_radius] = 1
        return food_arr

    # TODO: ignore points outside vision for efficiency?
    def bots_to_numpy(self, botlist, enemy=False):
        """If enemy, returns tuple of bots, bots_noise.
        Any non-zero values in bots_noise must also be non-zero in bots."""
        # pass in e.g. self.enemy_bots
        # assumes self.walls_arr is set, to get maze dimensions
        bots_arr = np.zeros_like(self.walls_arr, dtype=np.int8)
        if enemy:
            noise_arr = np.zeros_like(self.walls_arr, dtype=np.int8)
        for bot in botlist:
            x, y = bot.current_pos
            bots_arr[x+self.vision_radius, y+self.vision_radius] = 1
            if enemy and bot.noisy:
                noise_arr[x+self.vision_radius, y+self.vision_radius] = 1
        if not enemy:
            return bots_arr
        else:
            return (bots_arr, noise_arr)
