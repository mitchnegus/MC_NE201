"""Quick script to change X, Y, and R coordinates of MCNP cylinders"""
import numpy as np

XYR = np.genfromtxt('coordinates.txt',delimiter=' ')
XYR[:,0] = XYR[:,0]-1.995
XYR[:,1] = XYR[:,1]-4.160
print(XYR)
np.savetxt('coordinates-transformed.txt',XYR,fmt='%0.2f')
