# EXAMPLES:
#   cd ~/sandbox/wrap_api
#   python -m pytest -rA -m "not slow"    # Do this often!
#
#   python -m pytest
#   python -m pytest -rA   # with individual pass/fail/skip reported
#   python -m pytest tests/test_helpers_contrib.py
#   python -m pytest tests/test_helpers_contrib.py::test_night_files
#
# With captured output of passed tests
#   python -m pytest -rP tests/test_helpers_contrib.py::test_exposure_map

# Python Standard Library
from pprint import pformat
import warnings
# External Packages
import pytest
import numpy as np
# Local Packages
import helpers.api

#rooturl = 'https://astroarchive.noao.edu/' #@@@
rooturl = 'http://marsnat1.pat.dm.noao.edu:8000/' #@@@
fapi = helpers.api.FitsFile(rooturl, verbose=False, limit=5)

def test_night_files():
    from helpers.contrib.night_files import get_night_list

    fl = get_night_list('ct4m', 'decam', '2017-08-15', ['md5sum'], fapi)
    assert len(fl) == 370

@pytest.mark.slow
def test_download_decam_expnum(verbose=False):
    from helpers.contrib.download_decam_expnum import get_files

    # To find expnum of recent public files:
    #! info,rows=fapi.search({"outfields": ["EXPNUM"], "search":[ ["instrument","decam"],["proc_type","raw"], ["release_date", "2019-11-28", "2020-11-28"]]})
    
    #!nums = [797795, 782077, 795357, 772298, 844631]
    nums = [797795, 782077]
    files = get_files(nums, "~/Downloads/noirlab", fapi, verbose=verbose)
    assert len(files) == len(nums)
    
#@pytest.mark.skip(reason="UNDER CONSTRUCTION")    
def test_exposure_map():
    import helpers.contrib.exposure_map as em
    warnings.filterwarnings('ignore') # suppress ALL warnings (dangerous)
    
    hapi = helpers.api.FitsHdu(rooturl)
    map = em.gen_exposure_map(fapi, hapi)
    #print(f'test_exposure_map: count_nonzero(map)={np.count_nonzero(map)}')
    assert np.count_nonzero(map) >= 106052

