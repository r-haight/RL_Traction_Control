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
        self.voltage_input = [] # to keep track of what voltage is used at what time

        # The goal is to ensure traction but also to keep wheel going within the following speed limits
        # lower = 100 rpm -> 10.5 rad/s
        # upper = 150 rpm -> 15.71 rad/s
        self.angular_vel_goal = 300


    def get_reward(self):

        # use the measured slip to get the current slip error
        error_slip = 0.0-(self.tire_model.S)
        # make the speed error based on the range of acceptable speeds
        error_speed = 0.0

        error_speed = self.angular_vel_goal - self.tire_model.w


        # reward calulation for angular vel and slip
        r_w = 6 * np.exp(-(error_speed / 100) ** 2) - 3

        if self.tire_model.S>=1 or self.tire_model.S<=-1: #(desired - actual_now) - (desired - actual_last_iteration ?)
            r_s = 6*np.exp(-(error_slip/0.5)**2)-3
        else:
            r_s=0

        # speed is half as important as slip
        r = 0.2*r_s + 0.8*r_w
        self.update_reward_graph(r)
        return r

    def update_state(self):
        self.u_t = abs(self.u_t * 5)
        if self.u_t<0:
            self.u_t = 0
        elif self.u_t>5:
            self.u_t = 5
        u = self.u_t # output of the FIS is the voltage to apply to the DC motor
        self.voltage_input.append(u)
        self.tire_model.iterate(u)
        pass

    def reset(self):
        # Edited for each controller
        self.state = self.initial_state.copy() #
        self.reward_track = []
        self.tire_model.reset_model()
        self.voltage_input = []
        pass


    def update_reward_graph(self, r):
        self.reward_track.append(r)
