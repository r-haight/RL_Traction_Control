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
    if(i == 300): # at 300 we hit an icy patch of road
         tire.road_condition_status = 4
    # elif(i==500):
    #      tire.road_condition_status = 3
    # elif(i>1800):
    #     #hit the brakes
    #     tire.w = 0

fig, ax = plt.subplots()
ax.plot(tire.forward_velocity)
plt.title('Forward Velocity')
plt.xlabel('time - ms')
plt.ylabel('forward velocity - m/s')
plt.show()

fig, ax = plt.subplots()
ax.plot(tire.angular_velocity_of_tire)
plt.title('Angular Velocity')
plt.xlabel('time - ms')
plt.ylabel('angular velocity  - rad/s')
plt.show()

fig, ax = plt.subplots()
ax.plot(tire.slip)
plt.title('Slip')
plt.xlabel('time - ms')
plt.ylabel('slip ratio')
plt.show()

fig, ax = plt.subplots()
ax.plot(tire.current)
plt.title('Current')
plt.xlabel('time - ms')
plt.ylabel('current - A')
plt.show()