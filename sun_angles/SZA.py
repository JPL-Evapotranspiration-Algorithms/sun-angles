from typing import Union
from datetime import datetime

import numpy as np
from rasters import Raster, CoordinateArray

from solar_apparent_time import solar_day_of_year_for_longitude, solar_hour_of_day_for_area

from .day_angle import day_angle_rad_from_DOY
from .declination import solar_dec_deg_from_day_angle_rad

def SZA_deg_from_lat_dec_hour(
        latitude: Union[Raster, np.ndarray], 
        solar_dec_deg: Union[Raster, np.ndarray], 
        hour: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    This function calculates the solar zenith angle (SZA) given the latitude, solar declination, and solar time. 
    The SZA is the angle between the zenith and the center of the sun's disc. The zenith is the point on the celestial 
    sphere directly above a specific location on the earth's surface.

    The calculation is based on the formula:
    cos(SZA) = sin(latitude) * sin(solar declination) + cos(latitude) * cos(solar declination) * cos(hour angle)

    The function has been validated against the MOD07 product, with the SZA calculated by this function matching 
    the SZA provided by MOD07 to within 0.4 degrees.

    Parameters:
    :param latitude: Latitude of the location in degrees. Ranges from -90 (South Pole) to 90 (North Pole).
    :param solar_dec_deg: Solar declination in degrees. It is the tilt of the Earth's axis relative to the sun and varies throughout the year.
    :param hour: Solar time in hours. It is the time based on the position of the sun in the sky, and varies throughout the day from 0 to 24.

    Returns:
    :return: Solar zenith angle in degrees. Ranges from 0 (sun directly overhead) to 90 (sun on the horizon).

    References:
    Muneer, T., & Fairooz, F. (2005). Solar radiation model. Applied energy, 81(4), 419-437.
    """
    # Convert latitude from degrees to radians for computation
    latitude_rad = np.radians(latitude)

    # Convert solar declination from degrees to radians for computation
    solar_dec_rad = np.radians(solar_dec_deg)

    # Calculate the hour angle in degrees. The hour angle is the angular distance between the sun and the meridian plane.
    # It is positive before noon and negative after noon. The formula used here converts solar time to hour angle.
    hour_angle_deg = hour * 15.0 - 180.0

    # Convert the hour angle from degrees to radians for computation
    hour_angle_rad = np.radians(hour_angle_deg)

    # Calculate the solar zenith angle in radians using the formula:
    SZA_rad = np.arccos(np.sin(latitude_rad) * np.sin(solar_dec_rad) + np.cos(latitude_rad) * np.cos(solar_dec_rad) * np.cos(hour_angle_rad))

    # Convert the solar zenith angle from radians to degrees for the final output
    SZA_deg = np.degrees(SZA_rad)

    # Return the solar zenith angle in degrees
    return SZA_deg

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

def calculate_SZA_from_datetime(time_UTC: datetime, lat: float, lon: float):
    """
    Calculates the solar zenith angle (SZA) in degrees based on the given UTC time, latitude, and longitude.

    Args:
        time_UTC (datetime.datetime): The UTC time to calculate the SZA for.
        lat (float): The latitude in degrees.
        lon (float): The longitude in degrees.

    Returns:
        float: The calculated solar zenith angle in degrees.
    """
    # Calculate the day of year based on the UTC time and longitude
    doy = solar_day_of_year_for_longitude(time_UTC, lon)
    # Calculate the hour of the day based on the UTC time and longitude
    hour = solar_hour_of_day_for_area(time_UTC=time_UTC, geometry=CoordinateArray(x=lon, y=lat))
    # Calculate the solar zenith angle in degrees based on the latitude, solar declination angle, and hour of the day
    SZA = calculate_SZA_from_DOY_and_hour(lat, lon, doy, hour)

    # Return the calculated solar zenith angle
    return SZA
