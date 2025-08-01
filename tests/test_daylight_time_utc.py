import unittest
import numpy as np
from datetime import datetime
from sun_angles.daylight import calculate_daylight

class TestCalculateDaylight(unittest.TestCase):
    def test_time_utc_single_datetime(self):
        # Test with a single datetime object
        doy = 100
        lat = 34.0
        dt = datetime(2025, 4, 10)  # DOY 100
        # Should match result with explicit DOY
        daylight1 = calculate_daylight(day_of_year=doy, lat=lat)
        daylight2 = calculate_daylight(time_UTC=dt, lat=lat)
        np.testing.assert_allclose(daylight1, daylight2, rtol=1e-6)

    def test_time_utc_single_string(self):
        # Test with a single string
        doy = 200
        lat = 45.0
        dt_str = '2025-07-19'  # DOY 200
        daylight1 = calculate_daylight(day_of_year=doy, lat=lat)
        daylight2 = calculate_daylight(time_UTC=dt_str, lat=lat)
        np.testing.assert_allclose(daylight1, daylight2, rtol=1e-6)

    def test_time_utc_array_datetime(self):
        # Test with an array of datetime objects
        lats = np.array([0.0, 45.0, -45.0])
        dts = [datetime(2025, 1, 1), datetime(2025, 6, 21), datetime(2025, 12, 21)]
        doys = [1, 172, 355]
        daylight1 = calculate_daylight(day_of_year=doys, lat=lats)
        daylight2 = calculate_daylight(time_UTC=dts, lat=lats)
        np.testing.assert_allclose(daylight1, daylight2, rtol=1e-6)

    def test_time_utc_array_string(self):
        # Test with an array of strings
        lats = np.array([10.0, 20.0, 30.0])
        dt_strs = ['2025-03-01', '2025-06-01', '2025-09-01']
        doys = [60, 152, 244]
        daylight1 = calculate_daylight(day_of_year=doys, lat=lats)
        daylight2 = calculate_daylight(time_UTC=dt_strs, lat=lats)
        np.testing.assert_allclose(daylight1, daylight2, rtol=1e-6)

if __name__ == '__main__':
    unittest.main()
