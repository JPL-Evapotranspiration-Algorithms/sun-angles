# Type hinting for flexible input types
from typing import Union
# Numerical operations
import numpy as np
# Custom Raster type for geospatial data
from rasters import Raster

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
