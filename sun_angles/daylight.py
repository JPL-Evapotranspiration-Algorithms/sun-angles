from typing import Union
import numpy as np
from rasters import Raster

def daylight_from_SHA(SHA_deg: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    This function calculates daylight hours from the sunrise hour angle (SHA) in degrees.
    
    The calculation is based on the formula:
    
    $$ daylight = \frac{2}{15} * SHA $$
    
    where:
    - daylight is the length of the day in hours
    - SHA is the sunrise hour angle in degrees
    
    The factor of 2/15 converts the hour angle from degrees to hours (since 360 degrees is equivalent to 24 hours, hence 1 hour is 15 degrees).
    
    Parameters
    ----------
    SHA_deg : np.ndarray
        Sunrise hour angle in degrees. Must be a numpy array.
        
    Returns
    -------
    np.ndarray
        Daylight hours. Returns a numpy array of the same shape as `SHA_deg`.
        
    References
    ----------
    - Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56. FAO, Rome, 300(9).
    - Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.
    """
    return (2.0 / 15.0) * SHA_deg
