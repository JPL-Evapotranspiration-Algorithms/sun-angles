from typing import Union
import numpy as np
from rasters import Raster

def sunrise_from_SHA(SHA_deg: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    Calculate the sunrise hour from the sunrise hour angle (SHA) in degrees.

    This function takes a `Raster` or `numpy.ndarray` of sunrise hour angles (SHA) 
    in degrees and converts it to the corresponding sunrise hours. The conversion 
    is based on the fact that the Earth rotates 15 degrees per hour.

    Parameters:
    SHA_deg (Union[Raster, np.ndarray]): A `Raster` or `numpy.ndarray` containing 
                                         sunrise hour angles in degrees.

    Returns:
    Union[Raster, np.ndarray]: A `Raster` or `numpy.ndarray` containing the 
                               calculated sunrise hours.

    Example:
    >>> import numpy as np
    >>> SHA_deg = np.array([0, 15, 30, 45])
    >>> sunrise_from_SHA(SHA_deg)
    array([12., 11., 10.,  9.])

    The formula used for this calculation is:
    sunrise hour = 12 - (SHA_deg / 15)

    Reference:
    [1] Duffie, J.A., & Beckman, W.A. (2013). Solar Engineering of Thermal Processes. 
    John Wiley & Sons. 
    """
    return 12.0 - (SHA_deg / 15.0)