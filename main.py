# Main driver for testing the adaptive control and reinforcement learning

import model #the tire traction & DC motor model
import FACL as FACL #class that implements fuzzy actor critic learning
from controller import controller  #the FACL controller class that interacts with the agent
from fql_controller import fql_controller
from Agent import Agent
import matplotlib.pyplot as plt

# Initialization and Setup
#state = current in amps, angular velocity, forward velocity
i_initial = 0
w_initial = 0
v_initial = 0
initial_state = [i_initial,w_initial,v_initial]
state_max = [50,10,10]
state_min = [-50,-10,-10 ]
num_of_membership_functions = [9, 9, 9]
action_list = [0,1,3.3,5]

number_of_epochs = 10

#Create the model object
motor_and_tyre = model.traction_model(initial_state)

# Select which type of RL we use
#1 = FACL and 2 = FQL
selection = 2

if selection ==1:
    # Pass the model object into a new controller object
    Traction_Controller = controller(initial_state, state_max, state_min, num_of_membership_functions, motor_and_tyre)
elif selection == 2:
    Traction_Controller = fql_controller(initial_state, state_max, state_min, num_of_membership_functions,
                                         motor_and_tyre, action_list)

#Agent object we interact with
learning_agent = Agent(Traction_Controller)


## Training Loop

for i in range(25):
    print("epoch: ", i)
    learning_agent.controller.reset()
    for j in range(learning_agent.training_iterations_max):
        #### At this point we need to make a simulation scenario
        #### We'll do dry road until 400, and then at 400 it needs to learn to enable traction
        if(j==400):
            learning_agent.controller.tire_model.road_condition_status = 4
        learning_agent.controller.iterate()

        # End the epoch condition?
    learning_agent.end_of_epoch()
# Print the path that our agent took in her last epoch
fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.slip)
plt.title("Slip")
plt.show()

fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.forward_velocity)
plt.title("Forward Velocity")
plt.show()


fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.angular_velocity_of_tire)
plt.title("Angular Velocity")
plt.show()

fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.voltage_input)
plt.title("Voltage Input")
plt.show()

learning_agent.print_reward_graph()