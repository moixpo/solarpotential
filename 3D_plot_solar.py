# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:04:09 2020

@author: pierre-olivier.moix
"""


import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#import cmath
#redéfinition: 
def sin(value):
    return np.sin(value)

def cos(value):
    return np.cos(value)

pi=np.pi


plt.close('all')
#___________________________________
#INPUTS SURFACE
#orientation=0  #0=south =direction of x axis
#90=east = dierction of y 
#slope=30       #0 is horizontal 90 is vertical.

#orientation=orientation_selected

#slope=slope_selected
orientation=-30
slope=30

#
##________________
##INPUTS SOLAR
#
#month_number_of_days=[31 29 31 30 31 30 31 31 30 31 30 31]
#if month_selected==1
#    month_number_of_days_total=0
#else
#    month_number_of_days_total=sum(month_number_of_days(1:month_selected-1))
#end
#
#days=day_selected+month_number_of_days_total
#hours=hour_selected
#minutes=minute_selected
#GMT_shift=GMToffset_selected
#latitude=latitude_selected
#longitude=longitude_selected
#altitude=altitude_selected
#albedo=albedo_selected

#_____________FOR MANUAL INPUTS ______________________
latitude=22  #-90 to +90, positiv is north
longitude=-20  #-180 to +180, positiv is west
altitude=1000
albedo=0.1
day=31+28+15
hours=12
minutes=0
GMT_shift=0 #if you want to translate into local time instead of using universal time
#___________________________________


time=day*24*60*60 +(hours+GMT_shift)*60*60 +minutes*60
#___________________________________





#######################################
#for manual inputs in debug mode:
solar_azimut_angle=80
zenith_angle=20
#####################################


#___________________________________
computed_irradiance=20

#r=solar_radiation_on_surface(slope, orientation,time,latitude,longitude, altitude,albedo)
#computed_irradiance=r(1)
#computed_azimut_angle=r(8)*180/pi
#computed_zenith_angle=r(9)*180/pi

#if I_want_solar_computation==1
#    solar_azimut_angle=computed_azimut_angle
#    zenith_angle=computed_zenith_angle
#    #else
#    #computed_irradiance=0
#end



#___________________________________
###########################
# Drawing of the sun ray

sun_vector=np.array([sin(zenith_angle*pi/180)*cos(solar_azimut_angle*pi/180) ,
    sin(zenith_angle*pi/180)*sin(solar_azimut_angle*pi/180),
    cos(zenith_angle*pi/180)])
#We don't want to represent the ray if there is no more sun
if computed_irradiance==0:
    sun_vector=[0, 0, 0]

#k=0:0.1:1
#k=np.array(range(0,10+1))/10
k=np.arange(0, 1+0.01, 0.1)
sun_ray_x=k*sun_vector[0]
sun_ray_y=k*sun_vector[1]
sun_ray_z=k*sun_vector[2]




#############################
#Drawing of the oriented surface
BorderSize=1

x11=0
y11=0
z11=0

x12=BorderSize*sin(orientation*pi/180)
y12=BorderSize*cos(orientation*pi/180)
z12=0

vect=np.array([x12-x11, y12-y11, z12-z11])

x21=-BorderSize*cos(slope*pi/180)*sin(pi/2+orientation*pi/180)
y21=-BorderSize*cos(slope*pi/180)*cos(pi/2+orientation*pi/180)
z21=BorderSize*sin(slope*pi/180)

x22=x21+vect[0]
y22=y21+vect[1]
z22=z21+vect[2]

#vect_centrage=

corners_x=np.array([[x11, x12],[x21, x22]])
corners_y=np.array([[y11, y12],[ y21, y22]])
corners_z=np.array([[z11, z12],[ z21, z22]])



###############################
# Computation of the shadow

if computed_irradiance!=0:
    #From the corner 21:
    #The equation is z21+x*sun_vector(3)=0
    x=-z21/sun_vector[2]
    shadow_corner_x21=x21+x*sun_vector[0]
    shadow_corner_y21=y21+x*sun_vector[1]

    #From the corner 22:
    #x=-z22/sun_vector(3)
    shadow_corner_x22=x22+x*sun_vector[0]
    shadow_corner_y22=y22+x*sun_vector[1]

    # shadow_corner_x22=shadow_corner_x21+vect(1)
    # shadow_corner_y22=shadow_corner_y21+vect(2)

    shadow_corners_x=np.array([[x11, x12],[  shadow_corner_x21, shadow_corner_x22]])
    shadow_corners_y=np.array([[y11, y12],[  shadow_corner_y21, shadow_corner_y22]])
    shadow_corners_z=np.array([[z11, z12],[  0,    0]])


#
########################
## 3D PLOT
#########################
    
    #Axes3D
    
    
fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot the surface.
#surf = ax.plot_surface(X, Y, Z, cmap='jet',
#                       linewidth=0, antialiased=False)

#surf = ax.scatter3D(corners_x, corners_y, corners_z, cmap='jet',
#                       linewidth=0, antialiased=False)
ax.plot_surface(shadow_corners_x, shadow_corners_y, shadow_corners_z, color=[0.4, 0.4, 0.4])


surf = ax.plot_surface(corners_x, corners_y, corners_z,  color= 'r',
                       linewidth=1, antialiased=False)

ax.plot(sun_ray_x, sun_ray_y, sun_ray_z, color='y', linewidth=2)

#Axes3D.plot(corners_x, corners_y, corners_z)

#surf(corners_x, corners_y, corners_z, 'LineWidth', 2, 'FaceColor', 'r')
#surf(corners_x, corners_y, corners_z, 'LineWidth', 2, 'FaceColor', 'r')
#hold on
#plot3(x12, y12, z12, 'g.', 'LineWidth', 3)
#plot3(sun_ray_x, sun_ray_y, sun_ray_z, 'y', 'LineWidth', 3)
#plot3(sun_ray_x, sun_ray_y, sun_ray_z*0, 'y:', 'LineWidth', 1.5)


# Customize the z axis.
ax.set_zlim(0, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_ylabel('North-South axe', fontsize=12)
ax.set_xlabel('East-West axe', fontsize=12)

ax.set_zlabel('elevation Z', fontsize=12)
plt.title('Irradiance on surface', fontsize=12, weight="bold")



circle_angle=np.arange(0, 2*pi+0.1, 0.1)
circle_x=sin(circle_angle)
circle_y=cos(circle_angle)
ax.plot(circle_x,circle_y, color='b')


ax.text(1.1, 0, 0, "South", horizontalalignment='left',verticalalignment='bottom', fontsize=12, weight="bold")
ax.text(0, 1.1, 0, "East", horizontalalignment='left',verticalalignment='bottom', fontsize=12, weight="bold")
ax.text(0, -1.1, 0, "West", horizontalalignment='left',verticalalignment='bottom', fontsize=12, weight="bold")
ax.text(-1.1, 0, 0, "North", horizontalalignment='left',verticalalignment='bottom', fontsize=12, weight="bold")
    
plt.show()


##figure(1)
##get(handles.the_plot_response)
#handles.the_plot_response
#gca
#surf(corners_x, corners_y, corners_z, 'LineWidth', 2, 'FaceColor', 'r')
#hold on
#plot3(x12, y12, z12, 'g.', 'LineWidth', 3)
#plot3(sun_ray_x, sun_ray_y, sun_ray_z, 'y', 'LineWidth', 3)
#plot3(sun_ray_x, sun_ray_y, sun_ray_z*0, 'y:', 'LineWidth', 1.5)
#if computed_irradiance~=0
#    if zenith_angle<90
#        surf(shadow_corners_x, shadow_corners_y, shadow_corners_z, 'LineWidth', 1, 'FaceColor', [0.4, 0.4, 0.4])
#
#    else
#        warning('The shadow cannot be plotted because the zenith is under horizon')
#    end
#end
#
##The directions
#compass(1.5, 0)
#text(1.7, 0, 0, 'South', 'FontWeight', 'Bold')
#compass(0, 1.5)
#text(0, 1.7, 0, 'East', 'FontWeight', 'Bold')
#compass(0, -1.5)
#text(0, -1.7, 0, 'West', 'FontWeight', 'Bold')
#compass(-1.5, 0)
#text(-1.7, 0, 0, 'North', 'FontWeight', 'Bold')
#
##Other indications
#if computed_irradiance==0
#    text(0, 0, 1.5, 'It is night time', 'FontWeight', 'Bold')
#else
#    #text(0, 0, 1.5, ['Irradiance on surface is ' num2str(round(computed_irradiance)) 'W/m^2'], 'FontWeight', 'Bold')
#end
#
#view(21, 8)
#axis([-2 2 -2 2 0 1.5])
#title('View of the surface with sun ray direction and shadow')
##cameratoolbar
#cameratoolbar('SetMode', 'orbit')
#
#
#
#
#
##############################
##Display the values computed
#set(handles.irradiance_text_answer,'string', num2str(computed_irradiance))
#set(handles.azimut_text_answer,'string', num2str(computed_azimut_angle))
#set(handles.zenith_text_answer,'string', num2str(computed_zenith_angle))
#
