import requests
from urllib.parse import urlencode
from enum import Enum,auto


# TODO:
#   API should return seperate versions for SIA and ADS.
#   Validate response from requests.  PPrint error if not success.
#   Generalize: error handling
#   Always JSON output (or pandas dataframe? or VOTABLE?)
#   ENUM for File, Hdu
#   ads search, HEADER in response should give full URL for 'endpoint'
#   Authentication.
#   VERBOSE mode (for debugging)
# 
#   Cache calls to relatively static content:
#      cat_lists, version, *_*_fields, *adoc,
#

class Rec(Enum):
    File = auto()
    Hdu = auto()

class AdaApi():
    """Astro Data Archive"""
    expected_version = 5.0

    def __init__(self,
                 url='https://astroarchive.noao.edu',  verbose=False,
                 username=None,  password=None):
        self.apiurl = f'{url}/api'
        self.adsurl = f'{url}/api/adv_search'
        self.siaurl = f'{url}/api/sia'
        self.categoricals = None
        self.version = None
        self.verbose = verbose
        if username is not None:
            res = requests.post(f'{apiurl}/get_token/',
                                json=dict(email=username, password=password))
            if res.status_code == 200:
                self.token = res.json()
            else:
                self.token = None
                msg = (f'Credentials given '
                       f'(username="{username}", password={password}) '
                       f'could not be authenticated. Therefore, you will '
                       f'only be allowed to retrieve PUBLIC files. '
                       f'You can still get any metadata.' )
                raise Exception(msg)
            
    def search(self, jspec, limit=False, format='json'):
        # VALIDATE params @@@
        qstr = urlencode(dict(limit=None if limit is None else (limit or self.limit),
                              format=format))
        t = 'h' if self.type == Rec.Hdu else 'f'
        url = f'{self.adsurl}/{t}asearch/?{qstr}'
        if self.verbose:
            print(f'Search invoking "{url}" with: {jspec}')
        res = requests.post(url, json=jspec)
        return(res.json())

    def vosearch(self, ra, dec, size, limit=100):
        t = 'hdu' if self.type == Rec.Hdu else 'img'
        qstr = urlencode(dict(POS=f'{ra},{dec}',SIZE=size))
        url = f'{self.siaurl}/vo{t}?'
        res = requests.get(url)
        return(res.content.decode("utf-8"))

    def check_version(self):
        """Insure this library in consistent with the API version."""
        res = requests.get(f"{self.apiurl}​/version​/")
        return(False)

    def get_categoricals(self):
        if self.categoricals is None:
            url = f'{self.adsurl}/cat_lists/'
            res = requests.get(url)
            self.categoricals = res.json()  # dict(catname) = [val1, val2, ...]
        return(self.categoricals)

    def get_aux_fields(self, instrument, proctype):
        # @@@ VALIDATE instrument, proctype, type
        t = 'hdu' if self.type == Rec.Hdu else 'file'
        url = f'{self.adsurl}/aux_{t}_fields/{instrument}/{proctype}/'
        res = requests.get(url)
        print(f"url={url}; res={res}; content={res.content}")
        return(res.json())

    def get_core_fields(self):
        t = 'hdu' if self.type == Rec.Hdu else 'file'
        # @@@ VALIDATE instrument, proctype, type
        res = requests.get(f'{self.adsurl}/core_{t}_fields/')
        return(res.json())

        
class FitsFile(AdaApi):
    def __init__(self, 
                 url='https://astroarchive.noao.edu',
                 verbose=False,
                 limit=10,
                 username=None,  password=None):
        super().__init__(url=url.rstrip('/'), verbose=verbose,
                         username=username, password=password)
        self.type = Rec.File
        self.limit = limit

    def retrieve(self, fileid, hdu=None):
        # VALIDATE params @@@
        qparams = '' if hdu is None else f'/?hdu={hdu}'
        url = f'{self.apiurl}/retrieve/{fileid}/{qparams}'
        if self.token is None:
            res = requests.get(url)
        else:
            res = requests.get(url, headers=dict(Authorization=self.token))
        return res

class FitsHdu(AdaApi):
    def __init__(self, 
                 url='https://astroarchive.noao.edu',
                 limit=20,
                 verbose=False,
                 username=None,  password=None):
        super().__init__(url=url.rstrip('/'), verbose=verbose,
                         username=username, password=password)
        self.type = Rec.Hdu
        self.limit = limit

##############################################################################        


#@@@ # POST
#@@@ def get_token​():
#@@@     """Request an authorization token."""
#@@@     url="/api​/get_token​/"
#@@@
#@@@ # GET
#@@@ def retrieve​(md5):
#@@@     """Download one FITS file from the Archive."""
#@@@     url="/api​/retrieve​/{md5}​/"
#@@@     pass
#@@@ 

#! # GET
#! def vohdu():
#!     """Find HDUs matching rectangle spatial query."""
#! ​    url="/api​/sia​/vohdu"
#!     pass
#! 
#! # GET
#! def voimg():
#!     """Find FITS Images matching rectangle spatial query."""
#! ​    url="/api​/sia​/voimg"
#!     pass
#!
#! # GET
#! def aux_file_fields(instrument, proctype):
#!     """Get names of fields for INSTRUMENT,PROCTYPE combination."""
#! ​    url="/api​/adv_search​/aux_file_fields​/{instrument}​/{proctype}​/"
#!     pass 
#! 
#! # GET
#! def aux_hdu_fields(instrument,proctype):
#!     """Get names of fields for INSTRUMENT,PROCTYPE combination."""
#! ​    url="/api​/adv_search​/aux_hdu_fields​/{instrument}​/{proctype}​/"
#!     pass
#! 
#! # GET
#! def cat_lists​():
#!     """List the currently acceptable values for each *categorical field* associated with Archive files."""
#! ​    url="/api​/adv_search​/cat_lists​/"
#!     pass
#! 
#! # GET
#! def core_file_fields​():
#!     """Get names of fields that are available in all Archive Files."""
#! ​    url="/api​/adv_search​/core_file_fields​/"
#!     pass
#! 
#! # GET
#! def core_hdu_fields​():
#!     """Get names of fields that are available in all Archive HDUs."""
#! ​    url="/api​/adv_search​/core_hdu_fields​/"
#!     pass
#! 
#! # GET
#! def fadoc​(): # @@@ HTML
#!     """How to construct the JSON payload for Advance Search queries."""
#! ​    url="/api​/adv_search​/fadoc​/"
#!     pass
#! 
#! # POST
#! def fasearch​():
#!     """Search for Files in Archive using json search spec."""
#! ​    url="/api​/adv_search​/fasearch​/"
#!     pass
#! 
#! # GET
#! def hadoc​(): # @@@ HTML
#!     """How to construct the JSON payload for Advance Search queries."""
#! ​    url="/api​/adv_search​/hadoc​/"
#!     pass
#! 
#! # POST
#! def hasearch​():
#!     """Search for HDUs in Archive using json search spec."""
#! ​    url="/api​/adv_search​/hasearch​/"
#!     pass
#! 
#! # GET
#! def fields​(): # @@@  HTML
#!     """Get fields known to be associated with given Instrument and Proctype."""
#! ​    url="/api​/fields​/"
#!     pass


#@@@ # GET
#@@@ def header​(md5):  # @@@  HTML
#@@@     """Return full FITS headers as HTML."""
#@@@     url="/api​/header​/{md5}​/"
#@@@     pass
#@@@ 
#@@@ # GET
#@@@ def object_lookup​():
#@@@     """Retrieve the RA,DEC coordinates for a given object by name."""
#@@@     url="/api​/object-lookup​/"
#@@@     pass
#@@@ 
#!# GET
#!def version​():
#!    """Get version of this API library."""
#!    url="/api​/version​/"
#!    pass
