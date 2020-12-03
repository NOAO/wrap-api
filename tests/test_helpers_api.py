# EXAMPLE:
#   cd ~/sandbox/wrap_api
#   python -m pytest

# Python Standard Library
from pprint import pformat
from pathlib import Path, PosixPath
# Local Packages
import helpers.api
# External Packages
import pytest


#rooturl = 'https://astroarchive.noao.edu/' #@@@
rooturl = 'http://marsnat1.pat.dm.noao.edu:8000/' #@@@

fapi = helpers.api.FitsFile(rooturl, verbose=False, limit=5)

def test_fapi():
    assert fapi.limit == 5
    pass
    
def test_search():
    info,rows = fapi.search({"outfields": ["archive_filename"], "search":[]})
    assert len(rows) == 5

@pytest.mark.skip(reason="CSV and XML return itertools.chain in response")    
def test_search_csv():
    info,rows = fapi.search({"outfields": ["md5sum","caldat"], "search":[]},
                           format='csv')
    assert len(rows) == 5
    
def test_vosearch():
    info,rows = fapi.vosearch(13, -34, 1, format='json')
    assert not info['RESULTS']['MORE']
    assert len(rows) == 3

    
def test_retrieve_proprietary():
    proprietaryFileId = 'a96e55509a4cf89ebcc3126bef2e6aa7' # from S&F
    fits = fapi.retrieve(proprietaryFileId)

def test_retrieve_public():
    publicFileId = '0000298c7e0b3ce96b3fff51515a6100'
    local_file_path = Path(PosixPath('~/Downloads/noirlab').expanduser(),
                           f'fits{publicFileId}')
    with open(local_file_path,'wb') as fits:
        fits.write(fapi.retrieve(publicFileId))
