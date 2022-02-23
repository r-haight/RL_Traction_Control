# Main driver for testing the adaptive control and reinforcement learning
######## NOT COMPLETED AT ALL ###########
import model #the tire traction & DC motor model
import FACL #class that implements fuzzy actor critic learning
import controller #the official controller class that interacts with the agent
import Agent

#state = current in amps, angular velocity, forward velocity
initial_state = [0,0,0]
state_max = [50,10,10]
state_min = [0,-10,-10 ]
num_of_membership_functions = [10, 10, 10]

#Create the model object
motor_and_tyre = model.traction_model.__init__(initial_state)

#Pass the model object into a new controller object
controller.FACLController.__init__(initial_state, )