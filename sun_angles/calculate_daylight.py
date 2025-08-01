# Type hinting for flexible input types
from typing import Union
import numpy as np
from rasters import Raster, SpatialGeometry
from datetime import datetime
from dateutil import parser
import pandas as pd

from solar_apparent_time import solar_day_of_year_for_longitude

from .SHA_deg_from_DOY_lat import SHA_deg_from_DOY_lat
from .daylight_from_SHA import daylight_from_SHA

def calculate_daylight(
    time_UTC: Union[datetime, str, list, np.ndarray] = None,
    geometry: SpatialGeometry = None,
    day_of_year: Union[Raster, np.ndarray, int] = None,
    lat: Union[Raster, np.ndarray, float] = None,
    lon: Union[Raster, np.ndarray, float] = None,
    SHA_deg: Union[Raster, np.ndarray, float] = None
) -> Union[Raster, np.ndarray]:
    """
    Calculate the number of daylight hours for a given day and location.

    This function flexibly computes daylight hours based on the information provided:

    - If `SHA_deg` (sunrise hour angle in degrees) is provided, it is used directly to compute daylight hours.
    - If `SHA_deg` is not provided, it is calculated from `day_of_year` and `lat` (latitude in degrees).
    - If `lat` is not provided but a `geometry` object is given, latitude is extracted from `geometry.lat`.
    - If `day_of_year` is not provided but `time_UTC` is given, the function converts the UTC time(s) to day of year, accounting for longitude if available.

    Parameters
    ----------
    time_UTC : Union[datetime, str, list, np.ndarray], optional
        Datetime(s) in UTC. Used to determine `day_of_year` if not provided. Accepts a single datetime, a string, or an array/list of datetimes or strings.
        Example: `time_UTC=['2025-06-21', '2025-12-21']` or `time_UTC=datetime(2025, 6, 21)`
    geometry : SpatialGeometry, optional
        Geometry object containing latitude (and optionally longitude) information. Used if `lat` or `lon` are not provided.
    day_of_year : Union[Raster, np.ndarray, int], optional
        Day of year (1-366). Can be a Raster, numpy array, or integer. If not provided, will be inferred from `time_UTC` if available.
    lat : Union[Raster, np.ndarray, float], optional
        Latitude in degrees. Can be a Raster, numpy array, or float. If not provided, will be inferred from `geometry` if available.
    lon : Union[Raster, np.ndarray, float], optional
        Longitude in degrees. Can be a Raster, numpy array, or float. If not provided, will be inferred from `geometry` if available.
    SHA_deg : Union[Raster, np.ndarray, float], optional
        Sunrise hour angle in degrees. If provided, it is used directly and other parameters are ignored.

    Returns
    -------
    Union[Raster, np.ndarray]
        Daylight hours for the given inputs. The output type matches the input type (e.g., float, array, or Raster).

    Examples
    --------
    1. Provide SHA directly:
        daylight = calculate_daylight(SHA_deg=100)
    2. Provide day of year and latitude:
        daylight = calculate_daylight(day_of_year=172, lat=34.0)
    3. Provide UTC time and latitude:
        daylight = calculate_daylight(time_UTC='2025-06-21', lat=34.0)
    4. Provide geometry and UTC time:
        daylight = calculate_daylight(time_UTC='2025-06-21', geometry=my_geometry)
    """

    # If SHA_deg is not provided, calculate it from DOY and latitude
    if SHA_deg is None:
        # If latitude is not provided, try to extract from geometry
        if lat is None and geometry is not None:
            lat = geometry.lat

        if lon is None and geometry is not None:
            lon = geometry.lon

        # Handle day_of_year input: convert lists to np.ndarray
        if day_of_year is not None:
            if isinstance(day_of_year, list):
                day_of_year = np.array(day_of_year)

        # Handle lat input: convert lists to np.ndarray
        if lat is not None:
            if isinstance(lat, list):
                lat = np.array(lat)

        # If day_of_year is not provided, try to infer from time_UTC
        if day_of_year is None:
            # Handle string or list of strings for time_UTC
            if isinstance(time_UTC, str):
                time_UTC = parser.parse(time_UTC)
            elif isinstance(time_UTC, list):
                time_UTC = [parser.parse(t) if isinstance(t, str) else t for t in time_UTC]
            elif isinstance(time_UTC, np.ndarray) and time_UTC.dtype.type is np.str_:
                time_UTC = np.array([parser.parse(t) for t in time_UTC])

            # If lon is None, raise a clear error
            if lon is None:
                raise ValueError("Longitude (lon) must be provided when using time_UTC to infer day_of_year.")

            day_of_year = solar_day_of_year_for_longitude(
                time_UTC=time_UTC,
                lon=lon
            )

        SHA_deg = SHA_deg_from_DOY_lat(day_of_year, lat)

    # Compute daylight hours from SHA_deg
    daylight_hours = daylight_from_SHA(SHA_deg)

    return daylight_hours
