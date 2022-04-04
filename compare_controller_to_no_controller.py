# Main driver for testing the adaptive control and reinforcement learning

import model #the tire traction & DC motor model
import FACL as FACL #class that implements fuzzy actor critic learning
from controller import controller  #the FACL controller class that interacts with the agent
from fql_controller import fql_controller
from Agent import Agent
import matplotlib.pyplot as plt


################## RUN THE CONTROLLER PROGRAM FIRST
# Initialization and Setup
#state = current in amps, angular velocity, forward velocity
i_initial = 0
w_initial = 0
v_initial = 0
initial_state = [i_initial,w_initial,v_initial]
state_max = [100,500,20]
state_min = [-10,-10,-10]
num_of_membership_functions = [9, 19, 9]
action_list = [0,3.3,5]

number_of_epochs = 10

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
        ### SCENARIO 1
        if(j==300):
            learning_agent.controller.tire_model.road_condition_status = 2
        elif j ==500:
            learning_agent.controller.tire_model.road_condition_status = 4
        learning_agent.controller.iterate()


        learning_agent.controller.iterate()

        # End the epoch condition?
    learning_agent.end_of_epoch()

######################### RUN THE MODEL SIM WITH STRAIGHT 5V

#step 1: create a model object
# state = current, angular velocity of wheel, forward velocity of body
state_model = [0,0,0] #start with 1rad/s and 1m/s
max_iterations = 500
tire_no_control = model.traction_model(state_model)
v=5
#step 2: call iterate for a max # iterations
learning_agent.controller.tire_model.road_condition_status = 1
for i in range(max_iterations):
    tire_no_control.iterate(v) #input the voltage as a parameter

    ####SCENARIO 1
    if(i == 300): # at 300 we hit an icy patch of road
         tire_no_control.road_condition_status = 2 #Wet
    elif(i==500):
        tire_no_control.road_condition_status = 4 #icy


    # elif(i==500):
    #      tire.road_condition_status = 3
    # elif(i>1800):
    #     #hit the brakes
    #     tire.w = 0

# Print the path that our agent took in her last epoch
fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.slip, label='controlled')
ax.plot(tire_no_control.slip, label = 'not controlled')
plt.legend()
plt.title("Slip - Comparison")
plt.xlabel('time - ms')
plt.ylabel('slip ratio')
plt.show()

fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.forward_velocity, label='controlled')
ax.plot(tire_no_control.forward_velocity, label = 'not controlled')
plt.legend()
plt.title("Forward Velocity - Comparison")
plt.xlabel('time - ms')
plt.ylabel('forward velocity - m/s')
plt.show()


fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.angular_velocity_of_tire, label = 'controlled')
ax.plot(tire_no_control.angular_velocity_of_tire, label = 'not controlled')
plt.legend()
plt.title("Angular Velocity - Comparison")
plt.xlabel('time - ms')
plt.ylabel('angular velocity  - rad/s')
plt.show()

fig, ax = plt.subplots()
ax.plot(learning_agent.controller.tire_model.voltage_input, label = 'controlled')
ax.plot(tire_no_control.voltage_input, label = 'not controlled')
plt.legend()
plt.title("Voltage Input - Comparison")
plt.xlabel('time - ms')
plt.ylabel('Voltage - V')
plt.show()
