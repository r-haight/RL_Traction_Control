# This file is used to test the model class and make sure that we're getting the outputs expected
import model
import matplotlib.pyplot as plt
#step 1: create a model object
# state = current, angular velocity of wheel, forward velocity of body
state = [0,0,0] #start with 1rad/s and 1m/s
max_iterations = 1000
tire = model.traction_model(state)
v=5
#step 2: call iterate for a max # iterations
for i in range(max_iterations):
    tire.iterate(v) #input the voltage as a parameter
    if(i == 150):
        v = 10
        pass
    elif(i == 300): # at 300 we hit an icy patch of road
         tire.road_condition_status = 4
    elif(i>800):
        #hit the brakes
        tire.w = 0

fig, ax = plt.subplots()
ax.plot(tire.forward_velocity)
plt.show()

fig, ax = plt.subplots()
ax.plot(tire.slip)
plt.show()

fig, ax = plt.subplots()
ax.plot(tire.current)
plt.show()