#! /usr/bin/env python
"""Get list of all files for specific telescope,instrument,night."""

# EXAMPLES:
#
# python -m helpers.contrib.night_files --telescope ct4m --instrument decam --night 2017-08-15 -f archive_filename -f md5sum
#
# python3
# from helpers.contrib.night_files import get_night_list
# fapi = helpers.api.FitsFile()
# get_night_list('ct4m', 'decam', '2017-08-15', ['md5sum','archive_filename'], fapi)

# Python Standard Library
import argparse
from pathlib import Path
import argparse
from pprint import pformat as pf
# Local Packages
import helpers.api



def get_night_list(telescope, instrument, night, outfields, fapi):
    jdata = dict(outfields=outfields,
                 search=[
                     ["telescope", telescope],
                     ["instrument", instrument],
                     ["caldat", night, night]
                 ])
    info,rows = fapi.search(jdata, limit=10000)
    #!print(f'Search INFO={info}')
    return rows

##############################################################################


def main():
    parser = argparse.ArgumentParser(
        #version='1.0.0',
        description='Download DECAM files given EXPNUMs',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    dflt_outfields = ["md5sum", "filesize", "proposal",
                      "original_filename", "archive_filename",
                      "ra_min", "ra_max", "dec_min", "dec_max",
                      "exposure", "seeing", "depth", "ifilter",
                      "caldat", "dateobs_min", "dateobs_max", "release_date",
                      "instrument", "telescope", "site",
                      "obs_mode", "obs_type", "proc_type", "prod_type",
                      "url"]

    parser.add_argument('-f', '--outfield', 
                        action='append',
                        help=(f'Name of field to include in output (multi allowed). '
                              f'Default = {dflt_outfields}' ))
    parser.add_argument('--telescope',
                        help='Name of telescope that created the FITS file.' )
    parser.add_argument('--instrument',
                        help='Name of instrument that created the FITS file.' )
    parser.add_argument('--night',
                        help='Night (YYYY-MM-DD) of observation.' )
    args = parser.parse_args()
    
    
    outfields = dflt_outfields if 'outfield' in args else args.outfield

    print(f'DBG outfields={outfields}')
    fapi =  helpers.api.FitsFile(verbose=True)

    nf = get_night_list(args.telescope, args.instrument, args.night, outfields,
                        fapi)
    print(','.join([str(k) for k in nf[1].keys()]))
    print('\n'.join([','.join([str(v) for v in d.values()]) for d in nf[1:]]))

if __name__ == '__main__':
    main()
