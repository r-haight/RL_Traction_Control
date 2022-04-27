# Main driver for testing the adaptive control and reinforcement learning

import model #the tire traction & DC motor model
import FACL as FACL #class that implements fuzzy actor critic learning
from controller import controller  #the FACL controller class that interacts with the agent
from fql_controller import fql_controller
from Agent import Agent
import matplotlib.pyplot as plt
import numpy as np


# Initialization and Setup
#state = current in amps, angular velocity, forward velocity
i_initial = 0
w_initial = 0
v_initial = 0
## This is used to make the membership functions. The maximum velocity is 20m/s etc
initial_state = [i_initial,w_initial,v_initial]
state_max = [100,500,20]
state_min = [-10,-10,-10]
num_of_membership_functions = [9, 19, 9]
action_list = [0,3.3,5]

number_of_epochs = 20

#Create the model object
motor_and_tyre = model.traction_model(initial_state)

# Select which type of RL we use
#1 = FACL and 2 = FQL
selection = 1

if selection ==1:
    # Pass the model object into a new controller object
    Traction_Controller = controller(initial_state, state_max, state_min, num_of_membership_functions, motor_and_tyre)
elif selection == 2:
    Traction_Controller = fql_controller(initial_state, state_max, state_min, num_of_membership_functions,
                                         motor_and_tyre, action_list)

#Agent object we interact with
learning_agent = Agent(Traction_Controller)


## Training Loop

for i in range(number_of_epochs):
    print("epoch: ", i)
    learning_agent.controller.reset()
    for j in range(learning_agent.training_iterations_max):
        #### At this point we make a simulation scenario
      
        if(j==300):
            learning_agent.controller.tire_model.road_condition_status = 2
        elif j ==500:
            learning_agent.controller.tire_model.road_condition_status = 4
        learning_agent.controller.iterate()

        # End the epoch condition?
    learning_agent.end_of_epoch()
# Print the path that our agent took in her last epoch
fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.slip)
plt.title("Slip")
plt.xlabel('time - ms')
plt.ylabel('slip ratio')
plt.show()

fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.forward_velocity)
plt.title("Forward Velocity")
plt.xlabel('time - ms')
plt.ylabel('forward velocity - m/s')
plt.show()


fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.angular_velocity_of_tire)
plt.title("Angular Velocity")
plt.xlabel('time - ms')
plt.ylabel('angular velocity  - rad/s')
plt.show()

fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.voltage_input)
plt.title("Voltage Input")
plt.xlabel('time - ms')
plt.ylabel('voltage - V')
plt.show()
print('Average Voltage Input', np.mean(learning_agent.controller.tire_model.voltage_input))
learning_agent.print_reward_graph()

