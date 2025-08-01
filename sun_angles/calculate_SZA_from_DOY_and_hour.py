from typing import Union
import numpy as np
from rasters import Raster
from .day_angle_rad_from_DOY import day_angle_rad_from_DOY
from .solar_dec_deg_from_day_angle_rad import solar_dec_deg_from_day_angle_rad
from .SZA_deg_from_lat_dec_hour import SZA_deg_from_lat_dec_hour

def calculate_SZA_from_DOY_and_hour(
        lat: Union[float, np.ndarray], 
        lon: Union[float, np.ndarray], 
        DOY: Union[float, np.ndarray, Raster], 
        hour: Union[float, np.ndarray, Raster]) -> Union[float, np.ndarray, Raster]:
    """
    Calculates the solar zenith angle (SZA) in degrees based on the given UTC time, latitude, longitude, day of year, and hour of day.

    Args:
        lat (Union[float, np.ndarray]): The latitude in degrees.
        lon (Union[float, np.ndarray]): The longitude in degrees.
        doy (Union[float, np.ndarray, Raster]): The day of year.
        hour (Union[float, np.ndarray, Raster]): The hour of the day.

    Returns:
        Union[float, np.ndarray, Raster]: The calculated solar zenith angle in degrees.
    """
    day_angle_rad = day_angle_rad_from_DOY(DOY)
    solar_dec_deg = solar_dec_deg_from_day_angle_rad(day_angle_rad)
    SZA = SZA_deg_from_lat_dec_hour(lat, solar_dec_deg, hour)

    return SZA
