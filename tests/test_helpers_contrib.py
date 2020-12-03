# EXAMPLE:
#   cd ~/sandbox/wrap_api
#   python -m pytest
#   python -m pytest tests/test_helpers_contrib.py
#   python -m pytest tests/test_helpers_contrib.py::test_night_files

# Python Standard Library
from pprint import pformat
# Local Packages
import helpers.api
# External Packages
import pytest

#rooturl = 'https://astroarchive.noao.edu/' #@@@
rooturl = 'http://marsnat1.pat.dm.noao.edu:8000/' #@@@
fapi = helpers.api.FitsFile(rooturl, verbose=False, limit=5)

def test_night_files():
    from helpers.contrib.night_files import get_night_list

    fl = get_night_list('ct4m', 'decam', '2017-08-15', ['md5sum'], fapi)
    assert len(fl) == 370

def test_download_decam_expnum(verbose=False):
    from helpers.contrib.download_decam_expnum import get_files

    # To find expnum of recent public files:
    #! info,rows=fapi.search({"outfields": ["EXPNUM"], "search":[ ["instrument","decam"],["proc_type","raw"], ["release_date", "2019-11-28", "2020-11-28"]]})
    
    #!nums = [797795, 782077, 795357, 772298, 844631]
    nums = [797795, 782077]
    files = get_files(nums, "~/Downloads/noirlab", fapi, verbose=verbose)
    assert len(files) == len(nums)
    
@pytest.mark.skip(reason="UNDER CONSTRUCTION")    
def test_exposure_map():
    from helpers.contrib.exposure_map import gen_exposure_map    

    res = fapi.vosearch(13,-34,1,limit=5, format='json')
    print(f'test_exposure_map: len(res)={len(res)}')
    hapi = helpers.api.FitsHdu(rooturl, verbose=False, limit=5)
    gen_exposure_map(fapi, hapi)
    assert len(res) == 4

