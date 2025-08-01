# Usage

This package provides a set of functions for calculating solar geometry parameters. Below is a summary of each function and its usage:



[![CI](https://github.com/JPL-Evapotranspiration-Algorithms/sun-angles/actions/workflows/ci.yml/badge.svg)](https://github.com/JPL-Evapotranspiration-Algorithms/sun-angles/actions/workflows/ci.yml)

The `sun-angles` Python package calculates solar zenith and azimuth and daylight hours.

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

## Installation

This package is availabe on PyPi as a [pip package](https://pypi.org/project/sun-angles/) as `sun-angles` with a dash.

```bash
pip install sun-angles
```

## Usage

Import this package as `sun_angles` with an under-score.

```python
import sun_angles
```

### 1. `day_angle_rad_from_DOY(DOY)`
- **Description:** Calculates the day angle (in radians) from the day of the year.
- **Parameters:** `DOY` (int, numpy array, or Raster): Day of year (1–365).
- **Returns:** Day angle in radians.
- **Reference:** Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.


### 2. `solar_dec_deg_from_day_angle_rad(day_angle_rad)`
- **Description:** Computes the solar declination (in degrees) from the day angle (in radians).
- **Parameters:** `day_angle_rad` (float, numpy array, or Raster): Day angle in radians.
- **Returns:** Solar declination in degrees.
- **Reference:** Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.


### 3. `SHA_deg_from_DOY_lat(DOY, latitude)`
- **Description:** Calculates the sunrise hour angle (SHA, in degrees) from day of year and latitude.
- **Parameters:** 
	- `DOY` (int, numpy array, or Raster): Day of year.
	- `latitude` (float, numpy array, or Raster): Latitude in degrees.
- **Returns:** Sunrise hour angle in degrees.
- **Reference:** Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.


### 4. `daylight_from_SHA(SHA_deg)`
- **Description:** Converts sunrise hour angle (SHA, in degrees) to daylight hours.
- **Parameters:** `SHA_deg` (float, numpy array, or Raster): Sunrise hour angle in degrees.
- **Returns:** Daylight hours.
- **References:**
	- Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56. FAO, Rome, 300(9).
	- Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.


### 5. `calculate_daylight(day_of_year=None, lat=None, SHA_deg=None, time_UTC=None, geometry=None)`
- **Description:** Computes daylight hours for a specific day and location. Accepts multiple input types: you can provide the sunrise hour angle (SHA) directly, or supply day of year and latitude (or a datetime or geometry), and the function will calculate SHA as needed.
- **Parameters:** 
	- `day_of_year` (optional): Day of year (int, array, or Raster).
	- `lat` (optional): Latitude in degrees (float, array, or Raster).
	- `SHA_deg` (optional): Sunrise hour angle in degrees.
	- `time_UTC` (optional): Datetime in UTC (datetime, string, or array).
	- `geometry` (optional): Geometry object with latitude.
- **Returns:** Daylight hours (float, array, or Raster).


### 6. `sunrise_from_SHA(SHA_deg)`
- **Description:** Calculates the sunrise hour from the sunrise hour angle (SHA, in degrees).
- **Parameters:** `SHA_deg` (float, numpy array, or Raster): Sunrise hour angle in degrees.
- **Returns:** Sunrise hour.
- **Reference:** Duffie, J.A., & Beckman, W.A. (2013). Solar Engineering of Thermal Processes. John Wiley & Sons.


### 7. `SZA_deg_from_lat_dec_hour(latitude, solar_dec_deg, hour)`
- **Description:** Calculates the solar zenith angle (SZA, in degrees) from latitude, solar declination, and hour.
- **Parameters:** 
	- `latitude` (float, numpy array, or Raster): Latitude in degrees.
	- `solar_dec_deg` (float, numpy array, or Raster): Solar declination in degrees.
	- `hour` (float, numpy array, or Raster): Solar time in hours.
- **Returns:** Solar zenith angle in degrees.
- **Reference:** Muneer, T., & Fairooz, F. (2005). Solar radiation model. Applied energy, 81(4), 419-437.


### 8. `calculate_SZA_from_DOY_and_hour(lat, lon, DOY, hour)`
- **Description:** Calculates the solar zenith angle (SZA, in degrees) from latitude, longitude, day of year, and hour.
- **Parameters:** 
	- `lat` (float or array): Latitude in degrees.
	- `lon` (float or array): Longitude in degrees.
	- `DOY` (int or array): Day of year.
	- `hour` (float or array): Hour of day.
- **Returns:** Solar zenith angle in degrees.


### 9. `calculate_SZA_from_datetime(time_UTC, lat, lon)`
- **Description:** Calculates the solar zenith angle (SZA, in degrees) for a given UTC time, latitude, and longitude.
- **Parameters:** 
	- `time_UTC` (datetime): UTC time.
	- `lat` (float): Latitude in degrees.
	- `lon` (float): Longitude in degrees.
- **Returns:** Solar zenith angle in degrees.


### 10. `calculate_solar_azimuth(solar_dec_deg, SZA_deg, hour)`
- **Description:** Calculates the solar azimuth angle (in degrees) from solar declination, solar zenith angle, and hour.
- **Parameters:** 
	- `solar_dec_deg` (float, numpy array, or Raster): Solar declination in degrees.
	- `SZA_deg` (float, numpy array, or Raster): Solar zenith angle in degrees.
	- `hour` (float, numpy array, or Raster): Hour of the day.
- **Reference:** Muneer, T., & Fairooz, F. (2005). Solar radiation and daylight models: for the energy efficient design of buildings. Architectural Press.

# References

- Allen, R.G., Pereira, L.S., Raes, D., Smith, M., 1998. Crop evapotranspiration-Guidelines for computing crop water requirements-FAO Irrigation and drainage paper 56. FAO, Rome, 300(9).
- Duffie, J. A., & Beckman, W. A. (2013). Solar Engineering of Thermal Processes (4th ed.). Wiley.
- Muneer, T., & Fairooz, F. (2005). Solar radiation model. Applied energy, 81(4), 419-437.
- Muneer, T., & Fairooz, F. (2005). Solar radiation and daylight models: for the energy efficient design of buildings. Architectural Press.

