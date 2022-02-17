import numpy as np
import FACL as FACL
import model
class TestController(FACL):

    def __init__(self, state, max, min, num_mf):
        self.state = state
        self.r = 1 #radius of the territory
        self.reward_track =[] # to keep track of the rewards
        FACL.__init__(self, max, min, num_mf) #explicit call to the base class constructor
        model.traction_model.__init__(state)

    def get_reward(self):
        r = 0
        self.update_reward_graph(r)
        return r

    def update_state(self):
        self.state[0] = self.state[0] + self.v * np.cos(self.u_t)
        self.state[1] = self.state[1] + self.v * np.sin(self.u_t)
        self.update_path(self.state)
        pass

    def reset(self):
        # Edited for each controller
        self.state = [5,5] # set to self.initial_state, debug later???
        self.reward_track = []
        self.distance_away_from_target_t = self.distance_from_target()
        pass

    def update_path(self, state):
        self.path = np.vstack([self.path, state])
        pass

    def update_reward_graph(self, r):
        self.reward_track.append(r)
