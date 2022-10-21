import sys
from zmqRemoteApi import RemoteAPIClient
import numpy as np
import time
import sim
import math

sim.simxFinish(-1)
ID=sim.simxStart('127.0.0.1',19999,True,True,5000,5)

client = RemoteAPIClient()
sim_ = client.getObject('sim')

if ID ==-1:
    print('Connection Error')  
    exit()

print('Connected to Coppelia')  


#Coletando objetos

time.sleep(1)
error, floor = sim.simxGetObjectHandle(ID, 'Floor', sim.simx_opmode_oneshot_wait)

if(error == -1):
    print(f'Error getting floor object')  
    exit()

error, dummy = sim.simxGetObjectHandle(ID, 'Dummy', sim.simx_opmode_oneshot_wait)
if(error == -1):
    print(f'Error getting Dummy object')  
    exit()


#Estabelecendo troca de dados
error, orientation_dummy = sim.simxGetObjectOrientation(ID, dummy, floor, sim.simx_opmode_streaming)
if(error == -1):
    print(f'Error getting orientation')  
    exit()

error, position_dummy = sim.simxGetObjectPosition(ID, dummy, floor, sim.simx_opmode_streaming)
if(error == -1):
    print(f'Error getting position')
    exit()

print(f"Dummy Position: {position_dummy}")
print(f"Dummy orientation: {orientation_dummy}")

orientation_dummy_degree = [d * (180/math.pi) for d in orientation_dummy]
print(f"Rotating dummy: {position_dummy}")

sim.simxSetObjectPosition(ID, dummy, -1, (0.5,0.5,0.5), sim.simx_opmode_blocking)
if(error == -1):
    print(f'Error setting position')
    exit()

sim.simxSetObjectOrientation(ID, dummy, floor, [45,45,45], sim.simx_opmode_buffer)
if(error == -1):
    print(f'Error setting orientation')
    exit()

error, orientation_dummy = sim.simxGetObjectOrientation(ID, dummy, floor, sim.simx_opmode_streaming)
if(error == -1):
    print(f'Error getting orientation')  
    exit()

error, position_dummy = sim.simxGetObjectPosition(ID, dummy, floor, sim.simx_opmode_streaming)
if(error == -1):
    print(f'Error getting position')
    exit()

print(f"Dummy Position: {position_dummy}")
print(f"Dummy orientation: {orientation_dummy}")

matrix_transformation = sim_.getObjectMatrix(dummy, floor)
matrix_transformation_formatted = np.array(matrix_transformation).reshape((3, 4))

print(f"Matriz de transformação: \n{matrix_transformation_formatted}")

# Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
sim.simxGetPingTime(ID)

# Now close the connection to CoppeliaSim:
sim.simxFinish(ID)
