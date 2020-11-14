# TODO:
#   API should return seperate versions for SIA and ADS.
#   Validate response from requests.  PPrint error if not success.
#   Generalized: LIMIT, error handling
#   Always JSON output (or pandas dataframe? or VOTABLE?)
#   ENUM for File, Hdu
# 
#   Cache calls to relatively static content:
#      cat_lists, version, *_*_fields, *adoc,
#     

class AdaApi():
    """Astro Data Archive"""
    expected_version = 5.0

    def __init__(self, url='https://astroarchive.noao.edu'):
        self.apiurl = f'{url}/api'
        self.adsurl = f'{url}/api/adv_search'
        self.siaurl = f'{url}/api/sia'
        self.default_limit = 1000 # @@@
        self.categoricals = None
        self.version = None

    def check_version(self):
        """Insure this library in consistent with the API version."""
        res = requests.get(f"{self.apiurl}​/version​/")
        return(False)
    
    def get_categoricals(self):
        if self.categoricals is None:
            res = requests.get(f'{self.adsurl}/cat_lists​/')
            self.categoricals = res.json()  # dict(catname) = [val1, val2, ...]
        return(self.categoricals)

    def get_aux_fields(instrument, proctype):
        # @@@ VALIDATE instrument, proctype, type
        res = requests.get(f'{adsurl}/aux_{self.type}_fields/{instrument}​/{proctype}​/')
        return(res.json())

    def get_core_fields(instrument, proctype, type='file'):
        # @@@ VALIDATE instrument, proctype, type
        res = requests.get(f'{adsurl}/core_{self.type}_fields/')
        return(res.json())

    def search(self, jspec):
        t = 'h' if self.type=='hdu' else 'f'
        res = requests.post(f'{adsurl}/{t}asearch/', json=jspec)
        return(res.json())

    def vosearch(self, ra, dec, size, limit=False):
        t = 'hdu' if self.type=='hdu' else 'img'
        if not limit:
            limit = self.default_limit 
        res = requests.post(f'{siaurl}/vo{t}?POS={ra},{dec}&SIZE={size}&limit={limit}')
        return(res.json())        

        
class FitsFile(AdaApi):
    def __init__(self):
        self.type = 'file'
        

class FitsHdu(AdaApi):
    def __init__(self):
        self.type = 'hdu'


##############################################################################        


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

# POST
def get_token​():
    """Request an authorization token."""
​    url="/api​/get_token​/"
    pass

# GET
def header​(md5):  # @@@  HTML
    """Return full FITS headers as HTML."""
​    url="/api​/header​/{md5}​/"
    pass

# GET
def object_lookup​():
    """Retrieve the RA,DEC coordinates for a given object by name."""
​    url="/api​/object-lookup​/"
    pass

# GET
def retrieve​(md5):
    """Download one FITS file from the Archive."""
​    url="/api​/retrieve​/{md5}​/"
    pass


#!# GET
#!def version​():
#!    """Get version of this API library."""
#!​    url="/api​/version​/"
#!    pass
