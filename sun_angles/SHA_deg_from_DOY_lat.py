from typing import Union
import warnings
import numpy as np
from rasters import Raster

from .day_angle_rad_from_DOY import day_angle_rad_from_DOY
from .solar_dec_deg_from_day_angle_rad import solar_dec_deg_from_day_angle_rad

def SHA_deg_from_DOY_lat(DOY: Union[Raster, np.ndarray], latitude: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate the sunrise hour angle in degrees from the latitude in degrees and the day of the year.

    Parameters:
    DOY (Union[Raster, np.ndarray]): A Raster or numpy array containing day of the year values (integers between 1 and 365).
    latitude (Union[Raster, np.ndarray]): A Raster or numpy array containing latitude values in degrees.

    Returns:
    Union[Raster, np.ndarray]: A Raster or numpy array containing the corresponding sunrise hour angles in degrees.

    The function performs the following steps:
    1. Calculate the day angle in radians from the day of the year using the function `day_angle_rad_from_DOY`.
    2. Calculate the solar declination in degrees from the day angle in radians using the function `solar_dec_deg_from_day_angle_rad`.
    3. Convert latitude and solar declination from degrees to radians.
    4. Calculate the cosine of the sunrise hour angle using the formula:
       sunrise_cos = -tan(latitude_rad) * tan(solar_dec_rad)
    5. Calculate the sunrise hour angle in radians using the arccosine of the sunrise_cos.
    6. Convert the sunrise hour angle from radians to degrees.
    7. Apply polar correction to handle extreme values of the cosine.

    The sunrise hour angle represents the angle between the local meridian and the hour circle of the sunrise point.

    References:
    Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.
    """
    # Accept lists, scalars, or arrays; convert to np.ndarray if needed
    if isinstance(DOY, list):
        DOY = np.array(DOY)
    if isinstance(latitude, list):
        latitude = np.array(latitude)
    # calculate day angle in radians
    day_angle_rad = day_angle_rad_from_DOY(DOY)

    # calculate solar declination in degrees
    solar_dec_deg = solar_dec_deg_from_day_angle_rad(day_angle_rad)

    # convert latitude to radians
    latitude_rad = np.radians(latitude)

    # convert solar declination to radians
    solar_dec_rad = np.radians(solar_dec_deg)

    # calculate cosine of sunrise angle at latitude and solar declination
    # need to keep the cosine for polar correction
    sunrise_cos = -np.tan(latitude_rad) * np.tan(solar_dec_rad)

    # calculate sunrise angle in radians from cosine
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        sunrise_rad = np.arccos(sunrise_cos)

    # convert to degrees
    sunrise_deg = np.degrees(sunrise_rad)

    # apply polar correction
    sunrise_deg = np.where(sunrise_cos >= 1, 0, sunrise_deg)
    sunrise_deg = np.where(sunrise_cos <= -1, 180, sunrise_deg)

    return sunrise_deg