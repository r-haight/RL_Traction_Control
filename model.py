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

        self.J = 0.001 #inertial load, Nm
        self.b = 0.00000397 #viscosity in system
        self.r_w = 0.032 # tire radius, m
        self.m = 1.136 #mass of wheel, kg
        self.L = 0.003 # inductace f DC motor, H
        self.R = 0.141 # armature resistor, ohms
        self.km = 0.00574 #motor constant
        self.kb =  0.00574

        #for the purpose of simulation, a road condition flag will be used to calculate the type of friction factor
        #we need to use. this gets changed during simulation to test how the controller responds
        # 1 = dry
        # 2 = wet
        # 3 = snow
        # 4 = ice
        self.road_condition_status = 1 # initialize to dry conditions
        self.td = 0 #disturbance

        # the following are arrays that store information to get printed out later, just need them to be created in the constructor
        self.current = []
        self.slip = []
        self.forward_velocity = []
        self.angular_velocity_of_tire = []
        self.friction_coefficient = []
        self.voltage_input = []

        pass

    # here is a function for calculating slip
    def calculate_slip(self):
        tol = 0.0000000001
        self.S = (self.w * self.r_w - self.v)/abs(self.v + tol)
        #a tolerance is added so that there is no division by 0
        #now if the calculate slip is huge we should just set to 10
        if(self.S>10):
            self.S = 10
        elif(self.S<-10):
            self.S = -10

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
        dt = 0.001
        didt = (-self.i * self.R - self.kb * self.w + self.Voltage)/self.L
        dwdt = (1/self.J)*(self.km*self.i - self.td - self.b * self.w - self.r_w * self.m * 9.81 * self.mu)
        dvdt = 9.81 * self.mu

        self.i = self.i + didt*dt
        self.w = self.w + dwdt*dt
        self.v = self.v + dvdt*dt

        pass

    def iterate(self, v):
        #step 1: get the voltage from the controller
        self.Voltage = v
        #step 2: calculate the slip
        self.calculate_slip()
        #step 3: calculate the coeffient of friction
        self.calculate_friction_factor()
        #step 4: calculate the new state
        self.calculate_new_state()
        #step 5: save the info into the arrays
        self.save_values()
    #this function is used to save the important values for plotting
    def save_values(self):
        # here are some values that we may want to plot at the end
        self.current.append(self.i)
        self.angular_velocity_of_tire.append(self.w)
        self.forward_velocity.append(self.v)
        self.friction_coefficient.append(self.mu)
        self.slip.append(self.S)
        self.voltage_input.append(self.Voltage)

    def reset_model(self):
        self.current=[]
        self.angular_velocity_of_tire=[]
        self.forward_velocity=[]
        self.friction_coefficient=[]
        self.slip=[]
        self.voltage_input = []




