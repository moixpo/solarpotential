# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 09:32:46 2020

@author: pierre-olivier.moix

Assessment of solar for my house... and learning to use the PVGIS API
"""
 

###########
#
#All the PVGIS tools can be accessed non-interactively using our web APIs:
#
#https://re.jrc.ec.europa.eu/api/tool_name?param1=value1&param2=value2&... 
#
#with:
#
#    tool_name:   PVcalc, SHScalc, MRcalc, DRcalc, seriescalc, tmy, printhorizon.
#    param1=value1, param2=value2, ...:  input parameters of the tool with their corresponding values concatenated in a query string format.
#
#PVGIS APIs can be called directly using different languages like Python, NodeJS, Perl, Java and many others. Such languages have libraries to ease API calls management. Please, for more information check the documentation of the specific language used.
#
#Please be warned that access to PVGIS APIs via AJAX is not allowed. Please, do not ask for changes in our CORS policy since these requests will be rejected.
#
#APIs calls have a rate limit of 25 calls/second per IP address. This means that if you exceed this threshold, the API call will refuse your call and return an HTTP error code 429 - "Too Many Requests" error.
#
#When you report an error, please always specify the exact URL, the parameters used, the exact error text and the exact version of software/libraries you are using and any other information that may help us find and fix the problem.
#
#Inputs
#
#    If any of the inputs is out of the expected range, a json error message will be returned specifying the range of expected values for that input.
#    The query string must include at least all the mandatory inputs of the app (see minimal usage examples). The default values will be used for undefined optional parameters.
#    Inputs not required by the tool will be deprecated.
#
#Outputs
#
#The outputs obtained with the non-interactive service are exactly the same as those obtained with the PVGIS interface. The output type is controlled with the following two parameters:
#
#    outputformat:
#        outputformat=csv  CSV output.
#        outputformat=json  JSON output.
#        outputformat=basic  Raw CSV output without metadata.
#        outputformat=epw  Energy Plus EPW file (only for the TMY tool).
#    browser:
#        browser=0  Output as a stream.
#        browser=1  Output as a file.
#
#We encourage users to use the JSON output for integrating PVGIS results in other web services and scripts. This will reduce potential impacts of future PVGIS upgrades in their services.
#
##############
#
#Grid-connected & Tracking PV systems
#Show inputs
#
#Example of the minimum usage:
#
#https://re.jrc.ec.europa.eu/api/PVcalc?lat=45&lon=8&peakpower=1&loss=14
#
#    For the fixed PV system, if the parameter "optimalinclination" is selected (set to 1), the value defined for the "angle" parameter is ignored. Similarly, if "optimalangles" is set to 1, values defined for "angle" and "aspect" are ignored and therefore are not necessary. In this case, parameter "optimalinclination" would not be necessary either.
#    For the inclined axis PV system analysis, the parameter "inclined_axis" must be selected, along with either "inclinedaxisangle" or "inclined_optimum". If parameter "inclined_optimum" is selected, the inclination angle defined in "inclinedaxisangle" is ignored, so this parameter would not be necessary.
#    Parameters regarding the vertical axis ("vertical_axis", "vertical_optimum" and "verticalaxisangle") are related in the same way as the parameters used for the inclined axis PV system.
#
#Off-grid PV systems
#Show inputs
#
#Example of the minimum usage:
#
#https://re.jrc.ec.europa.eu/api/SHScalc?lat=45&lon=8&peakpower=10&batterysize=50&consumptionday=200&cutoff=40
#
#Monthly radiation
#Show inputs
#
#Example of the minimum usage:
#
#https://re.jrc.ec.europa.eu/api/MRcalc?lat=45&lon=8&horirrad=1
#
#    At least one output option should be chosen (horirrad, optrad, selectrad, etc). Otherwise the output table will not have any values. 
#
#Daily radiation
#Show inputs
#
#Example of the minimum usage:
#
#https://re.jrc.ec.europa.eu/api/DRcalc?lat=45&lon=8&month=3&global=1
#
#    Unlike the PVGIS web interface, it is also possible here to get values for all 12 months with a single call. See below for more details.
#
#Hourly radiation
#Show inputs
#
#Example of the minimum usage:
#
#https://re.jrc.ec.europa.eu/api/seriescalc?lat=45&lon=8
#
#TMY
#Show inputs
#
#Example of the minium usage:
#
# https://re.jrc.ec.europa.eu/api/tmy?lat=45&lon=8
#
#Horizon profile
#Show inputs
#
#Example of minimum usage:
#
#https://re.jrc.ec.europa.eu/api/printhorizon?lat=45&lon=8
#
#    There is also the option to supply user-defined horizon information. This would not normally be useful since the web service will just send the horizon information back to you. However, it can be a way to check that PVGIS interprets the user-supplied horizon information correctly.
#


#import io
#import json
#from pathlib import Path
import requests
#import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
#import matplotlib.cbook as cbook
#import matplotlib.image as image
#from pvlib.iotools import read_epw, parse_epw


from PIL import Image

plt.close('all')

#figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT)
FIGSIZE_WIDTH=15
FIGSIZE_HEIGHT=6

#jeu de couleur
PINK_COLOR='#FFB2C7'
RED_COLOR='#CC0000'
WHITE_COLOR='#FFFFFF'

#albedo
A_RED_COLOR="#9A031E"
A_YELLOW_COLOR="#F7B53B"
A_BLUE_COLOR="#2E5266"
A_RAISINBLACK_COLOR="#272838"
A_BLUEGREY_COLOR="#7E7F9A"
A_GREY_COLOR_SLATE="#6E8898"
A_GREY_COLOR2_BLUED="#9FB1BC"
A_GREY_COLOR3_LIGHT="#F9F8F8"




URL = 'https://re.jrc.ec.europa.eu/api/'


# API parameters
LATITUDE = 46.155  #PJ
LONGITUDE = 7.451  #PJ

LATITUDE = 46.208  #VEX
LONGITUDE = 7.394  #VEX

#LATITUDE = 46.229  #Vuissoz Conthey
#LONGITUDE = 7.302  ##Vuissoz Conthey


ANGLE = 20 # 	Inclination angle from horizontal plane of the (fixed) PV system.
ANGLE2 = 20
ASPECT = -30 #	F 	No 	0 	Orientation (azimuth) angle of the (fixed) PV system, 0=south, 90=west, -90=east.
ASPECT2 = ASPECT+180
ASPECT = 62
ASPECT2 = ASPECT-180

LOSSES=14   #%
PEAKPOWER= 10 #kWp

WATERMARK_PICTURE='logo.png'
WATERMARK_PICTURE='LogoAlbedo_90x380.png'

START_DATE = datetime(2014, 1, 1, 00, 00, 00)
END_DATE = datetime(2016, 12, 31, 23, 59, 59)
DATABASE = 'PVGIS-SARAH'
OUTPUT_FORMAT='json'

USELOCAL_TIME=1 #True: local time   Else UTC



# Request API
#DOC: https://ec.europa.eu/jrc/en/PVGIS/docs/noninteractive

API_HOURLY_TIME_SERIES = 'http://re.jrc.ec.europa.eu/pvgis5/seriescalc.php'
API_HORIZON_SERIES = 'https://re.jrc.ec.europa.eu/api/printhorizon'
API_TMY_SERIES = ' https://re.jrc.ec.europa.eu/api/tmy'  #A typical meteorological year (TMY) is a set of meteorological data with data values for every hour in a year for a given geographical location. 
API_PVCALC_SERIES= 'https://re.jrc.ec.europa.eu/api/PVcalc'
API_DAILY_RADIATION ='https://re.jrc.ec.europa.eu/api/DRcalc' #we show the average solar irradiation for each hour during the day for a chosen month, with the average taken over all days in that month during the multi-year time period for which we have data. In addition to calculating the average of the solar radiation, the daily radiation application also calculates the daily variation in the clear-sky radiation, both for fixed and for sun-tracking surfaces.


# API parameters
PARAM_LATITUDE = 'lat'
PARAM_LONGITUDE = 'lon'
PARAM_ANGLE='angle'
PARAM_ASPECT='aspect'

PARAM_RAD_DATABASE = 'raddatabase'
PARAM_AUTO_HORIZON = 'useHorizon'
PARAM_USER_HORIZON = 'userHorizon'
PARAM_START_YEAR = 'startyear'
PARAM_END_YEAR = 'endyear'
PARAM_MONTH = 'month'
PARAM_GLOBAL= 'global'
PARAM_COMPONENTS = 'components'
PARAM_OUTPUT_FORMAT = 'outputformat'
PARAM_USELOCAL_TIME= 'localtime'
PARAM_LOSSES = 'loss'
PARAM_PEAKPOWER = 'peakpower'

# Data headers
HEADER_DATE_TIME = 'DateTime'
HEADER_GHI = 'GHI'
HEADER_DNI = 'DNI'
HEADER_DHI = 'DHI'
HEADER_TA = 'TAmb'
HEADER_WS = 'Ws'


# PVGIS json keys
# https://ec.europa.eu/jrc/en/PVGIS/tools/hourly-radiation
KEY_JSON_OUTPUTS = 'outputs'
KEY_JSON_HOURLY = 'hourly'
KEY_JSON_TIME = 'time'
KEY_JSON_GB = 'Gb(i)'
KEY_JSON_GD = 'Gd(i)'
KEY_JSON_GR = 'Gr(i)'
KEY_JSON_TA = 'T2m'
KEY_JSON_WS = 'WS10m'

# Request codes
REQUEST_OK = 200





#--------------------------------
# Solar Potential
#--------------------------------



payload  = {PARAM_LATITUDE:     LATITUDE,
                             PARAM_LONGITUDE:    LONGITUDE,
                             PARAM_OUTPUT_FORMAT:OUTPUT_FORMAT}

print("Request for horizon")

res_horizon = requests.get(API_HORIZON_SERIES, params=payload )

print('Request:', res_horizon.url)
#horizon_json = json.loads(res_horizon.text)
horizon_json = res_horizon.json()
#horizon_json['outputs']['horizon_profile']

angle_A=[]
height_H_hor=[]

for horizdict in horizon_json['outputs']['horizon_profile']:
    angle_A.append(horizdict['A'])
    height_H_hor.append(horizdict['H_hor'])



angle_A_summer=[]
height_H_summer=[]

for horizdict in horizon_json['outputs']['summer_solstice']:
    angle_A_summer.append(horizdict['A_sun(s)'])
    height_H_summer.append(horizdict['H_sun(s)'])

angle_A_winter=[]
height_H_winter=[]

for horizdict in horizon_json['outputs']['winter_solstice']:
    angle_A_winter.append(horizdict['A_sun(w)'])
    height_H_winter.append(horizdict['H_sun(w)'])
    
    


#-----------------------------------
#https://re.jrc.ec.europa.eu/api/PVcalc?lat=45&lon=8&peakpower=1&loss=14
payload  = {PARAM_LATITUDE:     LATITUDE,
                             PARAM_LONGITUDE:    LONGITUDE,
                             PARAM_LOSSES:       LOSSES,
                             PARAM_PEAKPOWER:    PEAKPOWER,
                             PARAM_ANGLE:        ANGLE,
                             PARAM_ASPECT:       ASPECT,
                             PARAM_OUTPUT_FORMAT:OUTPUT_FORMAT}
print("Request for PVCALC fo orientation 1")
res_pvcalc = requests.get(API_PVCALC_SERIES, params=payload )
print('Request:', res_pvcalc.url)
#pvcalc_json = json.loads(res_pvcalc.text)
pvcalc_json = res_pvcalc.json()

month_energy_Em=[]
month_energy_Ed=[]

#pvcalc_json['outputs']['monthly']['fixed']
month_of_year=list(range(1,13))
for monthdict in pvcalc_json['outputs']['monthly']['fixed']:
    month_energy_Em.append(monthdict['E_m'])
    month_energy_Ed.append(monthdict['E_d'])


mean_day_energy_January=month_energy_Ed[0]


#second orientation:
payload[PARAM_ASPECT]=ASPECT2
payload[PARAM_ANGLE]=ANGLE2

print("Request for PVCALC fo orientation 1")
res_pvcalc = requests.get(API_PVCALC_SERIES, params=payload )
print('Request:', res_pvcalc.url)
#pvcalc_json = json.loads(res_pvcalc.text)
pvcalc_json = res_pvcalc.json()

month_energy_Em2=[]
month_energy_Ed=[]
#pvcalc_json['outputs']['monthly']['fixed']
month_of_year=list(range(1,13))
for monthdict in pvcalc_json['outputs']['monthly']['fixed']:
    month_energy_Em2.append(monthdict['E_m'])
    month_energy_Ed.append(monthdict['E_d'])


#--------------------------------
    
fig_solar_potential, axes_solar_potential = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))


width = 0.35  # the width of the bars
b1=axes_solar_potential[0].bar(np.array(month_of_year)- width/2, month_energy_Em, width, color=A_BLUE_COLOR, label='Orientation1')
b2=axes_solar_potential[0].bar(np.array(month_of_year)+ width/2, month_energy_Em2, width, color=A_YELLOW_COLOR, label='Orientation2')


#axes_solar_potential[0].bar(month_of_year, month_energy_Em, month_energy_Em2)
#axes_solar_potential[0].bar(month_of_year, month_energy_Em2, stacked=False)

axes_solar_potential[0].set_ylabel("Energy [kWh/month]", fontsize=12)
axes_solar_potential[0].set_xlabel("month of year", fontsize=12)

axes_solar_potential[0].set_title("PV production potential per month for " +str(PEAKPOWER) + " kWp", fontsize=12, weight="bold")
#TODO: ajouter un encart avec l'orientation et l'angle

axes_solar_potential[0].legend(["Orientation 1", "Orientation 2"])
axes_solar_potential[0].grid(True)

#ax2.fill_between(r.date, pricemin, r.close, facecolor='blue', alpha=0.5)
axes_solar_potential[1].fill_between(angle_A,0,height_H_hor, facecolor='blue', alpha=0.5)
#axes_solar_potential[1].plot(angle_A,height_H_hor)
axes_solar_potential[1].plot(angle_A_summer,height_H_summer, color='k')
axes_solar_potential[1].plot(angle_A_winter,height_H_winter, color='r')
axes_solar_potential[1].set_xlabel("Azimut angle [degrees] E=-90,  S=0, W=90, N=180 or -180", fontsize=12)
axes_solar_potential[1].set_ylabel("Height angle [degrees]", fontsize=12)

axes_solar_potential[1].legend(['summer sunheight', 'winter sunheight' ,"horizon"])

axes_solar_potential[1].set_title("Horizon", fontsize=12, weight="bold")
axes_solar_potential[1].set_xlim(-180,180)
axes_solar_potential[1].set_xticks(np.arange(-180, 180+1, 30.0))
axes_solar_potential[1].grid(True)

#addition of a watermark on the figure
im = Image.open(WATERMARK_PICTURE)   
fig_solar_potential.figimage(im, 10, 10, zorder=3, alpha=.2)


year_energy_orientation1=sum(month_energy_Em)
year_energy_orientation2=sum(month_energy_Em2)

t1 = ("The production  of the year is \n" + str(round(year_energy_orientation1)) + " kWh for orientation 1 \n" + str(round(year_energy_orientation2)) + " kWh for orientation 2")
axes_solar_potential[0].text(0.5, 1000, t1, ha='left', rotation=0, wrap=True)


#--------------------------------
# Typical Day
#--------------------------------



#-----------------------------------
#https://re.jrc.ec.europa.eu/api/DRcalc?lat=45&lon=8&month=3&global=1
payload  = {PARAM_LATITUDE:     LATITUDE,
                             PARAM_LONGITUDE:    LONGITUDE,
                             PARAM_GLOBAL:          1,
                             PARAM_MONTH:           1,
                             PARAM_ANGLE:        ANGLE,
                             PARAM_ASPECT:       ASPECT,
                             PARAM_USELOCAL_TIME: USELOCAL_TIME,
                             PARAM_OUTPUT_FORMAT:OUTPUT_FORMAT}
print("Request for daily radiation january ")
res_dailyrad = requests.get(API_DAILY_RADIATION, params=payload )
print('Request:', res_dailyrad.url)

dailyrad_json = res_dailyrad.json()

dailyirrad_G=[]
dailyirrad_Gb=[]
dailyirrad_Gd=[]

dailyirrad_time=[]

#pvcalc_json['outputs']['monthly']['fixed']
month_of_year=list(range(1,13))
for monthdict in dailyrad_json['outputs']['daily_profile']:
    dailyirrad_time.append(monthdict['time'])
    dailyirrad_G.append(monthdict['G(i)'])
    dailyirrad_Gb.append(monthdict['Gb(i)'])
    dailyirrad_Gd.append(monthdict['Gd(i)'])


  
fig_solar_typical_day, axes_solar_typical_day = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

axes_solar_typical_day[0].plot(dailyirrad_G)
#axes_solar_typical_day[0].plot(dailyirrad_Gd) #diffuse

axes_solar_typical_day[0].set_ylabel("Irradiance [W/m2]", fontsize=12)
axes_solar_typical_day[0].set_xlabel("Time of day [h]", fontsize=12)

axes_solar_typical_day[0].set_title("Irradiance ", fontsize=12, weight="bold")
#TODO: ajouter les infos de l'orientation et l'angle

axes_solar_typical_day[0].legend(["Typical production in January"])
axes_solar_typical_day[0].grid(True)
axes_solar_typical_day[0].set_xticks(np.arange(0, 24+1, 3.0))

axes_solar_typical_day[0].set_xlim(0,24)
fig_solar_typical_day.suptitle('When the sun is shining?', fontweight = 'bold', fontsize = 12) 


###
# DIFFUSE-DIRECT
fig_diffuse_direct, axes_diffuse_direct = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))
fig_diffuse_direct.figimage(im, 10, 10, zorder=3, alpha=.2)


###
# DIFFUSE-DIRECT
x=np.arange(0, 24, 1.0)
y=[dailyirrad_Gd,dailyirrad_Gb]
axes_diffuse_direct[0].stackplot(x,y, labels=['A','B','C'])
#axes_diffuse_direct.plot(dailyirrad_Gd) #diffuse
#axes_diffuse_direct.plot(dailyirrad_Gb) #direct
axes_diffuse_direct[0].set_ylabel("Irradiance [W/m2]", fontsize=12)
axes_diffuse_direct[0].set_xlabel("Time of day [h]", fontsize=12)
axes_diffuse_direct[0].set_title("Components of Irradiance on surface in January ", fontsize=12, weight="bold")
axes_diffuse_direct[0].legend(["Diffuse", "Direct"])
axes_diffuse_direct[0].grid(True)
axes_diffuse_direct[0].set_xlim(0,24)


ratio_to_kWh_prod=mean_day_energy_January/sum(np.array(dailyirrad_G))

#axes_diffuse_direct[1].stackplot(x,y, labels=['A','B','C'])
axes_diffuse_direct[1].bar(x, np.array(dailyirrad_G)*ratio_to_kWh_prod) #
#axes_diffuse_direct.plot(dailyirrad_Gb) #direct
axes_diffuse_direct[1].set_ylabel("Production [kWh per hour]", fontsize=12)
axes_diffuse_direct[1].set_xlabel("Time of day [h]", fontsize=12)
axes_diffuse_direct[1].set_title("Expected production per hour in January ", fontsize=12, weight="bold")
#axes_diffuse_direct[1].legend(["Diffuse orientation 1", "Direct orientation 1"])
axes_diffuse_direct[1].grid(True)
axes_diffuse_direct[1].set_xlim(0,24)



t2 = "The mean production \n of the day is " + str(round(sum(np.array(dailyirrad_G)*ratio_to_kWh_prod),2)) + " kWh \n"
axes_diffuse_direct[1].text(1, 1.5, t2, ha='left', rotation=0, wrap=True)


#second orientation:
payload[PARAM_ASPECT]=ASPECT2
payload[PARAM_ANGLE]=ANGLE2

print("Request for daily radiation july ")
res_dailyrad = requests.get(API_DAILY_RADIATION, params=payload )
print('Request:', res_dailyrad.url)

dailyrad_json = res_dailyrad.json()

dailyirrad_G=[]
dailyirrad_Gb=[]
dailyirrad_Gd=[]

dailyirrad_time=[]

#pvcalc_json['outputs']['monthly']['fixed']
month_of_year=list(range(1,13))
for monthdict in dailyrad_json['outputs']['daily_profile']:
    dailyirrad_time.append(monthdict['time'])
    dailyirrad_G.append(monthdict['G(i)'])
    dailyirrad_Gb.append(monthdict['Gb(i)'])
    dailyirrad_Gd.append(monthdict['Gd(i)'])


axes_solar_typical_day[0].plot(dailyirrad_G)
#axes_solar_typical_day[0].plot(dailyirrad_Gd) #diffuse

axes_solar_typical_day[0].set_ylabel("Irradiance [W/m2]", fontsize=12)
axes_solar_typical_day[0].set_xlabel("Time of day [h]", fontsize=12)

axes_solar_typical_day[0].set_title("Typical Irradiance on surface in January ", fontsize=12, weight="bold")
#TODO: ajouter un encart avec l'orientation et l'angle

axes_solar_typical_day[0].legend(["Orientation 1", "Orientation 2"])
axes_solar_typical_day[0].grid(True)
axes_solar_typical_day[0].set_xlim(0,24)
axes_solar_typical_day[0].set_xticks(np.arange(0, 24+1, 3.0))
fig_solar_typical_day.figimage(im, 10, 10, zorder=3, alpha=.2)


#change the month for july:
payload  = {PARAM_LATITUDE:     LATITUDE,
                             PARAM_LONGITUDE:    LONGITUDE,
                             PARAM_GLOBAL:          1,
                             PARAM_MONTH:           7,
                             PARAM_ANGLE:        ANGLE,
                             PARAM_ASPECT:       ASPECT,
                             PARAM_USELOCAL_TIME: USELOCAL_TIME,
                             PARAM_OUTPUT_FORMAT:OUTPUT_FORMAT}
print("Request for daily radiation january ")
res_dailyrad = requests.get(API_DAILY_RADIATION, params=payload )
print('Request:', res_dailyrad.url)

dailyrad_json = res_dailyrad.json()

dailyirrad_G=[]
dailyirrad_Gb=[]
dailyirrad_Gd=[]

dailyirrad_time=[]

#pvcalc_json['outputs']['monthly']['fixed']
month_of_year=list(range(1,13))
for monthdict in dailyrad_json['outputs']['daily_profile']:
    dailyirrad_time.append(monthdict['time'])
    dailyirrad_G.append(monthdict['G(i)'])
    dailyirrad_Gb.append(monthdict['Gb(i)'])
    dailyirrad_Gd.append(monthdict['Gd(i)'])


  
#fig_solar_typical_day, axes_solar_typical_day = plt.subplots(nrows=1, ncols=2, figsize=(FIGSIZE_WIDTH, FIGSIZE_HEIGHT))

axes_solar_typical_day[1].plot(dailyirrad_G)
#axes_solar_typical_day[1].plot(dailyirrad_Gd) #diffuse

axes_solar_typical_day[1].set_ylabel("Irradiance [W/m2]", fontsize=12)
axes_solar_typical_day[1].set_xlabel("Time of day [h]", fontsize=12)

axes_solar_typical_day[1].set_title("Irradiance ", fontsize=12, weight="bold")
#TODO: ajouter un encart avec l'orientation et l'angle

axes_solar_typical_day[1].legend(["Typical production in July"])
axes_solar_typical_day[1].grid(True)
axes_solar_typical_day[1].set_xticks(np.arange(0, 24+1, 3.0))

axes_solar_typical_day[1].set_xlim(0,24)



#second orientation:
payload[PARAM_ASPECT]=ASPECT2
payload[PARAM_ANGLE]=ANGLE2

print("Request for daily radiation july ")
res_dailyrad = requests.get(API_DAILY_RADIATION, params=payload )
print('Request:', res_dailyrad.url)

dailyrad_json = res_dailyrad.json()

dailyirrad_G=[]
dailyirrad_Gb=[]
dailyirrad_Gd=[]

dailyirrad_time=[]

#pvcalc_json['outputs']['monthly']['fixed']
month_of_year=list(range(1,13))
for monthdict in dailyrad_json['outputs']['daily_profile']:
    dailyirrad_time.append(monthdict['time'])
    dailyirrad_G.append(monthdict['G(i)'])
    dailyirrad_Gb.append(monthdict['Gb(i)'])
    dailyirrad_Gd.append(monthdict['Gd(i)'])


axes_solar_typical_day[1].plot(dailyirrad_G)
#axes_solar_typical_day[1].plot(dailyirrad_Gd) #diffuse
axes_solar_typical_day[1].set_ylabel("Irradiance [W/m2]", fontsize=12)
axes_solar_typical_day[1].set_xlabel("Time of day [h]", fontsize=12)

axes_solar_typical_day[1].set_title("Typical Irradiance on surface in July ", fontsize=12, weight="bold")
#TODO: ajouter un encart avec l'orientation et l'angle

axes_solar_typical_day[1].legend(["Orientation 1", "Orientation 2"])
axes_solar_typical_day[1].grid(True)
axes_solar_typical_day[1].set_xlim(0,24)
axes_solar_typical_day[1].set_xticks(np.arange(0, 24+1, 3.0))
fig_solar_typical_day.figimage(im, 10, 10, zorder=3, alpha=.2)



####
# Save for report
fig_solar_potential.savefig("ReportExport/SolarPotential.png")
fig_solar_typical_day.savefig("ReportExport/TypicalDay.png")
fig_diffuse_direct.savefig("ReportExport/DiffuseDirectProdJanuary.png")

plt.show()