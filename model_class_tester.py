# This file is used to test the model class and make sure that we're getting the outputs expected
import model
import matplotlib.pyplot as plt
#step 1: create a model object
state = [0,1,1] #start with 1m/s and 1rad/s
max_iterations = 500
tire = model.traction_model(state)
#step 2: call iterate for a max # iterations
for i in range(max_iterations):
    tire.iterate(12)
    if(i == 150):
        tire.road_condition_status = 3
    elif(i == 200):
        tire.road_condition_status = 2

fig, ax = plt.subplots()
ax.plot(tire.slip)
plt.show()