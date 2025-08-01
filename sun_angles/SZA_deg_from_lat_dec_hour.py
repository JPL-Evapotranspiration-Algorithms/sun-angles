from typing import Union
from rasters import Raster, CoordinateArray
import numpy as np

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
