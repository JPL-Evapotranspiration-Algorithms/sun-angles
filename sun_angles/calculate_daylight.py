# Type hinting for flexible input types
from typing import Union
import numpy as np
from rasters import Raster, SpatialGeometry
from datetime import datetime
from dateutil import parser
import pandas as pd
from .SHA_deg_from_DOY_lat import SHA_deg_from_DOY_lat
from .daylight_from_SHA import daylight_from_SHA

def calculate_daylight(
    day_of_year: Union[Raster, np.ndarray, int] = None,
    lat: Union[Raster, np.ndarray, float] = None,
    SHA_deg: Union[Raster, np.ndarray, float] = None,
    time_UTC: Union[datetime, str, list, np.ndarray] = None,
    geometry: SpatialGeometry = None
) -> Union[Raster, np.ndarray]:
    """
    Calculate the number of daylight hours for a given day and location.

    This function is highly flexible and can be used in several ways depending on the information you have:

    - If you already know the sunrise hour angle (`SHA_deg`), provide it directly and the function will return the daylight hours for that value.
    - If you do not provide `SHA_deg`, the function will compute it using the day of year (`day_of_year`) and latitude (`lat`).
    - If you do not provide `lat` but do provide a `geometry` object, the function will extract the latitude from `geometry.lat`.
    - If you do not provide `day_of_year` but do provide `time_UTC`, the function will convert the provided UTC time(s) to day of year. `time_UTC` can be a single datetime, a string, or an array/list of datetimes or strings.

    Parameters
    ----------
    day_of_year : Union[Raster, np.ndarray, int], optional
        Day of year (1-366). Can be a Raster, numpy array, or integer. If not provided, will be inferred from `time_UTC` if available.
    lat : Union[Raster, np.ndarray, float], optional
        Latitude in degrees. Can be a Raster, numpy array, or float. If not provided, will be inferred from `geometry` if available.
    SHA_deg : Union[Raster, np.ndarray, float], optional
        Sunrise hour angle in degrees. If provided, it is used directly and other parameters are ignored.
    time_UTC : datetime, str, list, or np.ndarray, optional
        Datetime(s) in UTC. Used to determine `day_of_year` if `day_of_year` is not provided. Accepts a single datetime, a string, or an array/list of datetimes or strings.
        Example: `time_UTC=['2025-06-21', '2025-12-21']` or `time_UTC=datetime(2025, 6, 21)`
    geometry : SpatialGeometry, optional
        Geometry object containing latitude information. If `lat` is not provided, latitude will be extracted from `geometry.lat`.

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

        # If DOY is not provided, try to extract from time_UTC
        if day_of_year is None and time_UTC is not None:
            def to_doy(val):
                if isinstance(val, str):
                    val = parser.parse(val)
                return int(pd.Timestamp(val).dayofyear)

            # Handle array-like or single value
            if isinstance(time_UTC, (list, np.ndarray)):
                day_of_year = np.array([to_doy(t) for t in time_UTC])
            else:
                day_of_year = to_doy(time_UTC)

        # Ensure day_of_year is a numpy array if it's a list (for downstream math)
        if isinstance(day_of_year, list):
            day_of_year = np.array(day_of_year)
        # Compute SHA_deg using DOY and latitude
        SHA_deg = SHA_deg_from_DOY_lat(day_of_year, lat)

    # Compute daylight hours from SHA_deg
    daylight_hours = daylight_from_SHA(SHA_deg)

    return daylight_hours
