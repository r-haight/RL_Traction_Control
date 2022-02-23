import numpy as np
import FACL as FACL
import model
class FACLController(FACL):

    def __init__(self, state, max, min, num_mf, model_object):
        self.state = state
        self.reward_track =[] # to keep track of the rewards
        FACL.__init__(self, max, min, num_mf) #explicit call to the base class constructor
        self.initial_state = state
        self.tire_model = model_object
    def get_reward(self):
        r = 0 #(desired - actual_now) - (desired - actual_last_iteration ?)
        self.update_reward_graph(r)
        return r

    def update_state(self):
        v = self.u_t # output of the FIS is the voltage to apply to the DC motor
        self.tire_model.iterate(v)
        pass

    def reset(self):
        # Edited for each controller
        self.state = self.initial_state # set to self.initial_state, debug later??? [1,1,0]
        self.reward_track = []

        pass


    def update_reward_graph(self, r):
        self.reward_track.append(r)
