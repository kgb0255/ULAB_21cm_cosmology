import numpy as np
import scipy.special as sci
import math


class Ant():
    def __init__(self, ant_num, position, a=6, sigma_ant=.003,  sigma_x=.005, sigma_y=.005):
        self.ant_num = ant_num
        self.position = position
        self.aperature = a
        self.sigma_ant = sigma_ant
        self.sigma_x = sigma_x
        self.sigma_y = sigma_y
        self.ax = np.random.normal(a,sigma_ant)
        self.ay = np.random.normal(a,sigma_ant)
        self.xs = np.random.normal(0,sigma_x)
        self.ys = np.random.normal(0,sigma_y)
        
    def airy_beam(self, x, y, nu):
        c=3.0e8 #speed of light in m/s
        k=2*np.pi*nu/c #wavenumber
        airy_arg=np.einsum("k,jl->ljk",k,(self.ax**2*(x-self.xs)**2+self.ay**2*(y-self.ys)**2)**.5)
        airy_funct = (2*sci.jv(1,airy_arg)/(airy_arg))**2 #Sci.jv are the bessel functions of the 1st kind
        return airy_funct

    def gaussian_beam(self, x, y, nu, mean = 0):
        self.x = x
        self.y = y
        self.mean = mean
        self.nu = nu
        c = 3.0e8
        a = 6
        sigma = 1.03*c/(4*a*nu*np.sqrt(2*np.log(2)))
        pos = np.tan(x/y)
        exponential = np.einsum("ij,k->jik",-(pos-mean)**2, 1/(2*sigma**2))
        gaussian= 1/(sigma*(2*np.pi)**0.5)*np.e**exponential #x is source position?

        return gaussian

    def airy2_beam(self, x, y, nu):
        c=3.0e8 #speed of light in m/s
        k=2*np.pi*nu/c #wavenumber
        airy2_arg=np.einsum("k,jl->ljk",k,(self.ax**2*(x-self.xs)**2+self.ay**2*(y-self.ys)**2))
        airy2_funct = (2*sci.jve(2,airy2_arg)**0.5/(airy2_arg)**0.5)**2
        return airy2_funct