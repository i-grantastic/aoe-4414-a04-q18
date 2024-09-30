# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
#   converts ECI coordinates to ECEF coordinates

# Parameters:
#   year: int
#   month: int
#   day: int
#   hour: int
#   minute: int
#   second: float
#   eci_x_km: x-component of ECI vector in km
#   eci_y_km: y-component of ECI vector in km
#   eci_z_km: z-component of ECI vector in km

# Output:
#   ECEF coordinates
#
# Written by Grant Chapman
# Other contributors: None

# import Python modules
import sys
import math
import numpy as np

# initialize script arguments
year   = float('nan')
month  = float('nan')
day    = float('nan')
hour   = float('nan')
minute = float('nan')
second = float('nan')
eci_x_km = float('nan')
eci_y_km = float('nan')
eci_z_km = float('nan')

# parse script arguments
if len(sys.argv) == 10:
  year   = int(sys.argv[1])
  month  = int(sys.argv[2])
  day    = int(sys.argv[3])
  hour   = int(sys.argv[4])
  minute = int(sys.argv[5])
  second = float(sys.argv[6])
  eci_x_km = float(sys.argv[7])
  eci_y_km = float(sys.argv[8])
  eci_z_km = float(sys.argv[9])
else:
  print(\
    'Usage: '\
    'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
  )
  exit()

## script below this line

# julian date
jd = day - 32075 + 1461*(year + 4800 + (month - 14)/12)/4\
+ 367*(month - 2 - (month - 14)/12*12)/12\
- 3*((year + 4900 + (month - 14)/12)/100)/4

# fractional julian date
jd_midnight = int(jd) - 0.5
d_frac = (second + 60*(minute + 60*hour))/86400
jd_frac = jd_midnight + d_frac

# ECI vector
eci_vector = [eci_x_km, eci_y_km, eci_z_km]

# getting angle
jd_ut1 = jd_frac
t_ut1 = (jd_ut1 - 2451545.0) / 36525
theta = 67310.54841+(876600*60*60 + 8640184.812866)*t_ut1 + 0.093104*t_ut1**2 - 6.2e-6*t_ut1**3
theta_rad = (theta % 86400)*7.292115e-5

# eci to ecef
r_z = [[math.cos(-theta_rad), -math.sin(-theta_rad), 0],
       [math.sin(-theta_rad), math.cos(-theta_rad), 0],
       [0, 0, 1]]

# calculate ecef
ecef_vector = np.matmul(r_z, eci_vector)
ecef_x_km = ecef_vector[0]
ecef_y_km = ecef_vector[1]
ecef_z_km = ecef_vector[2]

# print
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)