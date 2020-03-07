import matplotlib.pyplot as plt
import numpy as np
import math

class Ant():
    def __init__(self, ant_num, position, a=6, sigma_ant=0,  sigma_x=0, sigma_y=0):
        self.ant_num = ant_num
        self.position = position
        self.aperature = a
        self.sigma_ant = sigma_ant #noise
        self.sigma_x = sigma_x 
        self.sigma_y = sigma_y
        self.ax = np.random.normal(a,sigma_ant)
        self.ay = np.random.normal(a,sigma_ant)
        self.xs = np.random.normal(0,sigma_x)
        self.ys = np.random.normal(0,sigma_y)
        
    def airy_beam(self, x, y, nu): #x,y are for sources
        c=3.0*10**8 #speed of light in m/s
        k=2*np.pi*nu/c #wavenumber
        airy_arg=np.einsum("i,k->ik",k,(self.ax**2*(x-self.xs)**2+self.ay**2*(y-self.ys)**2))
        airy_funct = (2*sci.jv(1,airy_arg)**0.5/(airy_arg)**0.5)**2 #Sci.jv are the bessel functions of the 1st kind
        return airy_funct
    
    def gaussian_Beam(self,x,y,nu):
        pass
    
    def bessel_beam(self,x,y,nu):
        pass