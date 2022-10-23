import sys
from zmqRemoteApi import RemoteAPIClient
import numpy as np
import time
import sim
import math


def theta_1(O2, x, y):
  k_1 = 0.4*math.cos(O2) + 0.475
  k_2 = 0.4*math.sin(O2)

  return np.arctan2(y, x) - np.arctan2(k_2, k_1)


def theta_2(x,y):
  cos_2 = (x**2 + y**2 - 0.475**2 - 0.4**2)/(2*0.475*0.4)

  if(cos_2 < -1 or cos_2 > 1):
    print("Posição inválida!")
    return 0

  sin_2 = math.sqrt(1 - cos_2**2)

  return np.arctan2(sin_2, cos_2)

def theta_3(O1, O2, phi):
  return np.pi - O1 - O2

def iKine(x, y, z, phi):
  O2 = theta_2(x, y)
  O1 = theta_1(O2, x, y)
  O3 = theta_3(O1, O2, phi)
  d4 = -z + 0.1
  return O1, O2, O3, d4

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

error, scara = sim.simxGetObjectHandle(ID, 'MTB', sim.simx_opmode_oneshot_wait)
if(error == -1):
    print(f'Error getting Dummy object')  
    exit()

error, scara_axis1 = sim.simxGetObjectHandle(ID, 'axis1',sim.simx_opmode_oneshot_wait)
if(error == -1):
    print(f'Error getting Dummy object')  
    exit()

error, scara_axis2 = sim.simxGetObjectHandle(ID, 'axis2',sim.simx_opmode_oneshot_wait)
if(error == -1):
    print(f'Error getting Dummy object')  
    exit()

error, scara_axis3 = sim.simxGetObjectHandle(ID, 'axis3',sim.simx_opmode_oneshot_wait)
if(error == -1):
    print(f'Error getting Dummy object')  
    exit()

error, scara_axis4 = sim.simxGetObjectHandle(ID, 'axis4',sim.simx_opmode_oneshot_wait)
if(error == -1):
    print(f'Error getting Dummy object')  
    exit()

#Estabelecendo troca de dados

sim.simxSetObjectPosition(ID, dummy, scara, (0.5,0.5,0.5), sim.simx_opmode_blocking)
if(error == -1):
    print(f'Error setting position')
    exit()

sim.simxSetObjectOrientation(ID, dummy, scara, [45,45,45], sim.simx_opmode_buffer)
if(error == -1):
    print(f'Error setting orientation')
    exit()


error, orientation_dummy = sim.simxGetObjectOrientation(ID, dummy, scara, sim.simx_opmode_streaming)
if(error == -1):
    print(f'Error getting orientation')  
    exit()

error, position_dummy = sim.simxGetObjectPosition(ID, dummy, scara, sim.simx_opmode_streaming)
if(error == -1):
    print(f'Error getting position')
    exit()

print(f"Dummy Position: {position_dummy}")
print(f"Dummy orientation: {orientation_dummy}")

O1, O2, O3, d4 = iKine(0.5,0.5,0.5, 0)

sim.simxSetJointPosition(ID,scara_axis1, O1, sim.simx_opmode_oneshot_wait)
sim.simxSetJointPosition(ID,scara_axis2, O2, sim.simx_opmode_oneshot_wait)
sim.simxSetJointPosition(ID,scara_axis3, O3, sim.simx_opmode_oneshot_wait)
sim.simxSetJointPosition(ID,scara_axis4, d4, sim.simx_opmode_oneshot_wait)


print(f"Dummy Position: {position_dummy}")
print(f"Dummy orientation: {orientation_dummy}")



# Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
sim.simxGetPingTime(ID)

# Now close the connection to CoppeliaSim:
sim.simxFinish(ID)