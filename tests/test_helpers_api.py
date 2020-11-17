# EXAMPLE:
#   python -m pytest

import helpers.api
from pprint import pformat

fapi = helpers.api.FitsFile(url='http://marsnat1.pat.dm.noao.edu:8000/',
                            verbose=True)

res = fapi.search({"outfields": ["archive_filename"], "search":[]}, limit=5)
# Search invoking "http://marsnat1.pat.dm.noao.edu:8000/api/adv_search/fasearch/?limit=5&format=json" with: {'outfields': ['archive_filename'], 'search': []}

print(f'Result={pformat(res)}')

# Result=[{'HEADER': {'archive_filename': 'string'},
#   'META': {'endpoint': 'adv_search/fasearch'},
#   'PARAMETERS': {'format': 'json',
#                  'json_payload': {'outfields': ['archive_filename'],
#                                   'search': []},
#                  'last': 5,
#                  'limit': 5,
#                  'offset': 0,
#                  'oldest': None,
#                  'previd': None},
#   'RESULTS': {'COUNT': 5, 'MORE': True}},
#  {'archive_filename': '/net/archive/mtn/20181129/ct4m/2012B-0001/c4d_181130_010546_ori.fits.fz'},
#  {'archive_filename': '/net/archive/mtn/20170307/kp4m/2016A-0453/k4m_170308_045842_ori.fits.fz'},
#  {'archive_filename': '/net/archive/mtn/20181205/ct4m/2012B-0001/c4d_181205_224438_zri.fits.fz'},
#  {'archive_filename': '/net/archive/mtn/20150413/bok23m/2015A-0801/ksb_150414_104425_ori.fits.fz'},
#  {'archive_filename': '/net/archive/mtn/20180328/ct4m/2018A-0159/c4d_180329_035427_ori.fits.fz'}]

def test_search():
    res = fapi.search({"outfields": ["archive_filename"], "search":[]}, limit=5)
    assert len(res) == 6
    
def test_vosearch():
    res = fapi.vosearch(13,-34,1,limit=5, format='json')
    assert len(res) == 6

    
