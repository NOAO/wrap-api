
class ShortcutApi(AdaApi):

    def __init__(self, url='https://astroarchive.noao.edu'):
        self.adsurl = f'{url}/api/adv_search'
        #!self.shorturl = f'{url}/short'
    
    
    def night_files​(self, telescope, instrument, caldat):
        """Get list of all files for specific telescope,instrument,night."""
        # @@@ VALIDATE args
        self.type = 'file'
        jspec = dict(
            outfields = [
                "md5sum",
                "filesize",
                "proposal",
                "original_filename",
                "archive_filename",
                "ra_min",
                "ra_max",
                "dec_min",
                "dec_max",
                "exposure",
                "seeing",
                "depth",
                "ifilter",
                "dateobs_min",
                "dateobs_max",
                "release_date",
                "instrument",
                "telescope",
                "site",
                "obs_mode",
                "obs_type",
                "proc_type",
                "prod_type",
                "url",
                "caldat"
            ],
            search = [
                ["telescope", telescope],
                ["instrument", instrument],
                ["caldat", caldat, caldat]
            ])

        res = self.search(jspec)
        return(res.json())

