from typing import Union
import numpy as np
from rasters import Raster

def solar_dec_deg_from_day_angle_rad(day_angle_rad: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate solar declination in degrees from the day angle in radians.

    Parameters:
    day_angle_rad (Union[Raster, np.ndarray]): A Raster or numpy array containing day angles in radians.

    Returns:
    Union[Raster, np.ndarray]: A Raster or numpy array containing the corresponding solar declination angles in degrees.

    The solar declination is calculated using the following formula:
    solar_declination = 0.006918 - 0.399912 * cos(day_angle_rad) + 0.070257 * sin(day_angle_rad)
                      - 0.006758 * cos(2 * day_angle_rad) + 0.000907 * sin(2 * day_angle_rad)
                      - 0.002697 * cos(3 * day_angle_rad) + 0.00148 * sin(3 * day_angle_rad)
    
    This formula converts the day angle in radians to the solar declination in degrees, 
    which represents the angle between the rays of the sun and the plane of the Earth's equator.

    Reference:
    Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.
    """
    return (0.006918 - 0.399912 * np.cos(day_angle_rad) + 0.070257 * np.sin(day_angle_rad) 
            - 0.006758 * np.cos(2 * day_angle_rad) + 0.000907 * np.sin(2 * day_angle_rad) 
            - 0.002697 * np.cos(3 * day_angle_rad) + 0.00148 * np.sin(3 * day_angle_rad)) * (180 / np.pi)