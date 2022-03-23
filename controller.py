import numpy as np
from FACL import FACL
import model
class controller(FACL):

    def __init__(self, state, max, min, num_mf, model_object):
        self.state = state.copy()
        self.reward_track =[] # to keep track of the rewards
        self.tire_model = model_object
        FACL.__init__(self, max, min, num_mf) #explicit call to the base class constructor
        self.initial_state = state.copy()

    def get_reward(self):
        # print(self.tire_model.S)
        error = 0.0-(self.tire_model.slip[0])
        if self.tire_model.S>=1 or self.tire_model.S<=-1: #(desired - actual_now) - (desired - actual_last_iteration ?)
            r = 6*np.exp(-(error/0.5)**2)-3
        else:
            r=0
        self.update_reward_graph(r)
        return r

    def update_state(self):
        u = self.u_t # output of the FIS is the voltage to apply to the DC motor
        self.tire_model.iterate(u)
        pass

    def reset(self):
        # Edited for each controller
        self.state = self.initial_state.copy() #
        self.reward_track = []
        self.tire_model.reset_model()

        pass


    def update_reward_graph(self, r):
        self.reward_track.append(r)
