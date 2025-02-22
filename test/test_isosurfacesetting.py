import pytest
from batoms.utils.butils import removeAll
from batoms.batoms import Batoms
from batoms.bio.bio import read
import numpy as np
from time import time

try:
    from _common_helpers import has_display, set_cycles_res

    use_cycles = not has_display()
except ImportError:
    use_cycles = False

extras = dict(engine="cycles") if use_cycles else {}
import os

skip_test = bool(os.environ.get("NOTEST_CUBE", 0))


def test_slice():
    if skip_test:
        pytest.skip("Skip tests on cube files since $NOTEST_CUBE provided.")
    removeAll()
    h2o = read("/home/xing/ase/batoms/h2o-homo.cube")
    h2o.isosurfacesetting["1"] = {"level": -0.001}
    h2o.isosurfacesetting["2"] = {"level": 0.001, "color": [0, 0, 0.8, 0.5]}
    h2o.isosurfacesetting.draw_isosurface()
    h2o.planesetting[(1, 0, 0)] = {"distance": 6, "slicing": True}
    h2o.planesetting.draw_lattice_plane()
    if use_cycles:
        set_cycles_res(h2o)
    h2o.get_image([0, 0, 1], **extras)


def test_diff():
    if skip_test:
        pytest.skip("Skip tests on cube files since $NOTEST_CUBE provided.")
    removeAll()
    ag_pto_fe = read("/home/xing/ase/batoms/ag-pto-fe.cube")
    ag_pto = read("/home/xing/ase/batoms/ag-pto.cube")
    ag_pto.hide = True
    fe = read("/home/xing/ase/batoms/fe.cube")
    fe.hide = True
    volume = ag_pto_fe.volume - ag_pto.volume - fe.volume
    # volume = ag_pto_fe.isosurfacesetting.volume*2
    # print(volume)
    ag_pto_fe.volume = volume
    ag_pto_fe.isosurfacesetting[1].level = 0.008
    ag_pto_fe.isosurfacesetting[2] = {"level": -0.008, "color": [0, 0, 1, 0.8]}
    ag_pto_fe.model_style = 1
    ag_pto_fe.isosurfacesetting.draw_isosurface()
    if use_cycles:
        set_cycles_res(ag_pto_fe)
    else:
        ag_pto_fe.render.resolution = [3000, 3000]
    ag_pto_fe.get_image([0, 0, 1], output="top.png", **extras)
    ag_pto_fe.get_image([1, 0, 0], output="side.png", **extras)


if __name__ == "__main__":
    test_slice()
    test_diff()
    print("\n Isosurfacesetting: All pass! \n")
