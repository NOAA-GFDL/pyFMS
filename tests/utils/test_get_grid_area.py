import numpy as np

import pyfms


def test_get_grid_area():

    nxp = 20
    nyp = 40
    x1 = np.radians(list(range(nxp)), dtype=np.float64)
    y1 = np.radians(list(range(nyp)), dtype=np.float64)

    x_false, y_false = np.meshgrid(x1, y1)
    y_true, x_true = np.meshgrid(y1, x1)

    area_false = pyfms.grid_utils.get_grid_area(
        x_false, y_false, convert_cf_order=False
    )
    area_true = pyfms.grid_utils.get_grid_area(x_true, y_true, convert_cf_order=True)

    np.testing.assert_array_equal(area_false, area_true.T)
