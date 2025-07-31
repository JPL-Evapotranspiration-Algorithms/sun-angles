

# Type hinting for flexible input types
from typing import Union
# Numerical operations
import numpy as np
# Custom Raster type for geospatial data
from rasters import Raster
# For handling date and time
from datetime import datetime
# For parsing date strings
from dateutil import parser
# For date operations
import pandas as pd
# Function to compute sunrise hour angle from day of year and latitude
from .SHA import SHA_deg_from_DOY_lat
# Geometry class for spatial data
from .sun_angles import SpatialGeometry


def daylight_from_SHA(SHA_deg: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculates daylight hours from the sunrise hour angle (SHA) in degrees.

    The calculation is based on the formula:
        daylight = (2/15) * SHA
    where:
        - daylight is the length of the day in hours
        - SHA is the sunrise hour angle in degrees

    The factor 2/15 converts the hour angle from degrees to hours (since 360 degrees = 24 hours, so 1 hour = 15 degrees).

    Parameters
    ----------
    SHA_deg : Union[Raster, np.ndarray]
        Sunrise hour angle in degrees. Can be a `Raster` object or a numpy array.

    Returns
    -------
    Union[Raster, np.ndarray]
        Daylight hours. Returns a `Raster` object or a numpy array of the same shape as `SHA_deg`.

    References
    ----------
    - Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56. FAO, Rome, 300(9).
    - Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.
    """
    # Convert SHA (degrees) to daylight hours using the standard formula
    return (2.0 / 15.0) * SHA_deg


def calculate_daylight(
    DOY: Union[Raster, np.ndarray, int] = None,
    lat: Union[Raster, np.ndarray, float] = None,
    SHA_deg: Union[Raster, np.ndarray, float] = None,
    datetime_UTC: datetime = None,
    geometry: SpatialGeometry = None
) -> Union[Raster, np.ndarray]:
    """
    Calculate the number of daylight hours for a given day and location.

    This function is flexible in its inputs:
    - If SHA_deg (sunrise hour angle in degrees) is provided, it is used directly.
    - Otherwise, SHA_deg is computed from the day of year (DOY) and latitude (lat).
    - If lat is not provided but a geometry object is, latitude is extracted from geometry.
    - If DOY is not provided but a datetime_UTC is, DOY is computed from the datetime.

    Parameters
    ----------
    DOY : Union[Raster, np.ndarray, int], optional
        Day of year (1-366). Can be a Raster, numpy array, or integer.
    lat : Union[Raster, np.ndarray, float], optional
        Latitude in degrees. Can be a Raster, numpy array, or float.
    SHA_deg : Union[Raster, np.ndarray, float], optional
        Sunrise hour angle in degrees. If not provided, it will be calculated.
    datetime_UTC : datetime, optional
        Datetime in UTC. Used to determine DOY if DOY is not provided.
    geometry : SpatialGeometry, optional
        Geometry object containing latitude information.

    Returns
    -------
    Union[Raster, np.ndarray]
        Daylight hours for the given inputs.
    """
    # If SHA_deg is not provided, calculate it from DOY and latitude
    if SHA_deg is None:
        # If latitude is not provided, try to extract from geometry
        if lat is None and geometry is not None:
            lat = geometry.lat

        # If DOY is not provided, try to extract from datetime_UTC
        if DOY is None and datetime_UTC is not None:
            # If datetime_UTC is a string, parse it to a datetime object
            if isinstance(datetime_UTC, str):
                datetime_UTC = parser.parse(datetime_UTC)

            # Convert datetime to day of year
            DOY = int(pd.Timestamp(datetime_UTC).dayofyear)

        # Compute SHA_deg using DOY and latitude
        SHA_deg = SHA_deg_from_DOY_lat(DOY, lat)

    # Compute daylight hours from SHA_deg
    daylight_hours = daylight_from_SHA(SHA_deg)

    return daylight_hours