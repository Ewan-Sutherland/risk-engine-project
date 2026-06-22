# This script will compute the inverse normal using (initially) Acklam approximation
# followed by one step of Halley's method.

# Importing libraries
import math
import scipy

# Global variables
p_low = 0.02425
p_high = 0.97575

# The normal density function
def phi(x: float):
    density = (1/math.sqrt((2*math.pi)))*(math.exp(-(x**2)/2))
    return density

# The normal CDF function
def Phi(x:float):
    cdf = (1/2)*(1+math.erf(x/(math.sqrt(2))))
    return cdf

# Acklam values
a = [-3.969683028665376e+01,  2.209460984245205e+02,
     -2.759285104469687e+02,  1.383577518672690e+02,
     -3.066479806614716e+01,  2.506628277459239e+00]

b = [-5.447609879822406e+01,  1.615858368580409e+02,
     -1.556989798598866e+02,  6.680131188771972e+01,
     -1.328068155288572e+01]

c = [-7.784894002430293e-03, -3.223964580411365e-01,
     -2.400758277161838e+00, -2.549732539343734e+00,
      4.374664141464968e+00,  2.938163982698783e+00]

d = [ 7.784695709041462e-03,  3.224671290700398e-01,
      2.445134137142996e+00,  3.754408661907416e+00]

# Central region
def centralRegion(p:float):
    q = p - 0.5
    r = q * q
    x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    return x

# Lower tail region
def lowerRegion(p:float):
    q = math.sqrt(-2 * math.log(p))
    x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    return x

# Upper tail region
def upperRegion(p:float):
    q = math.sqrt(-2 * math.log(1-p))
    x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    return x

# Acklam approximation
def acklam(p: float):
    if 0 < p and p < p_low:
        return lowerRegion(p)
    elif p_low <= p and p <= p_high:
        return centralRegion(p)
    elif p_high < p and p < 1:
        return upperRegion(p)
    else:
        raise ValueError("p must be between 0 and 1")

# Halley's method step
def inverseNormal (p):
    x0 = acklam(p)
    err = Phi(x0)-p
    newtonRatio = err/phi(x0)
    x = x0-newtonRatio/(1+(x0*newtonRatio)/2)
    return x