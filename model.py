# this is a file for the tire and dc motor traction model.
# This class updates the states at each iteration. It is used in the update state control side
import numpy as np

class traction_model :
    def __init__(self, state):
        #initialization of the states
        # the states are i for current, w for angular velocity of wheel, v for forward velocity of body

        self.i = state[0]
        self.w = state[1]
        self.v = state[2]

        # these are some of the constants
        # they are static and do not change
        # if needed, we can change them from the main
        # essentially, these values chosen are representative of a toy car

        self.J = 0.0001 #inertial load, Nm
        self.b = 0.00000397 #viscosity in system
        self.r_w = 0.032 # tire radius, m
        self.m = 0.5 #mass of wheel, kg
        self.L = 0.003 # inductace f DC motor, H
        self.R = 0.141 # armature resistor, ohms
        self.km = 0.00574 #motor constant
        self.kb = 0.00574

        #for the purpose of simulation, a road condition flag will be used to calculate the type of friction factor
        #we need to use. this gets changed during simulation to test how the controller responds
        # 1 = dry
        # 2 = wet
        # 3 = snow
        # 4 = ice
        self.road_condition_status = 1 # initialize to dry conditions
        self.td = 0 #disturbance

        pass

    # here is a function for calculating slip
    def calculate_slip(self):
        self.S = (self.w * self.r_w - self.v)/abs(self.v)


    def calculate_friction_factor(self):
        if(self.road_condition_status == 1): #dry
            B = 10
            C = 1.9
            D = 1
            E = 0.97
        elif(self.road_condition_status == 2): #wet
            B = 12
            C = 2.3
            D = 0.82
            E = 1
        elif (self.road_condition_status == 3): #snow
            B = 5
            C = 2
            D = 0.3
            E = 1
        else: #ice
            B = 4
            C = 2
            D = 0.1
            E = 1

        self.mu = D * np.sin(C * np.arctan(B*self.S - E*(B * self.S - np.arctan(B*self.S))))
        pass

    def input_voltage(self, volt):
        self.Voltage = volt
        pass

    def calculate_new_state(self):
        didt = (-self.i * self.R - self.kb * self.w + self.Voltage)/self.L
        dwdt = (1/self.J)*(self.km*self.i - self.td - self.b * self.w - self.r_w * self.m * 9.81 * self.mu)
        dvdt = 9.81 * self.mu

        self.i = self.i + didt
        self.w = self.w + dwdt
        self.v = self.v + dvdt

        pass

    #this function is used to save the important values for plotting
    def save_state_values(self):
        current

