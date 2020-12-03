#! /usr/bin/env python
"""Download a set of DECAM FITS files containing given EXPNUM values."""

# Example:
#   cd ~/sandbox/wrap_api1
#   python -m helpers.contrib.download_decam_expnum -e 938946 -e 938950 --outdir /home/someuser/Downloads/decam

# To get some EXPNUMs over a date range:
# curl -X POST "https://astroarchive.noao.edu/api/adv_search/fasearch/?limit=1000" -H  "accept: application/json" -H  "Content-Type: application/json" -H  "X-CSRFToken: gFHNwAns1RjX5JnVOC4p8TaltxnzdLShRsDBvPVUQ50wUNasbYu0rjBwAL59SRdR" -d "{  \"outfields\": [    \"md5sum\",    \"release_date\",    \"EXPNUM\"  ],  \"search\": [    [\"release_date\", \"2019-11-28\", \"2020-11-15\"],    [\"instrument\", \"decam\"],    [\"proc_type\",\"raw\"]  ]}"

import argparse
from pathlib import Path, PosixPath
import argparse
from pprint import pformat
# Local
import helpers.api


def get_files(expnum_list, outdir, fapi, verbose=False):
    gotfiles = set()
    for expnum in expnum_list:
        outfilepath = Path(PosixPath(outdir).expanduser(),
                           f'DECam_{str(expnum).zfill(8)}.fits.fz')
        jj = {"outfields": ["md5sum",],
              "search": [ ["instrument", "decam"],  ["proc_type", "raw"],
                          ["EXPNUM", expnum, expnum]]}
        if verbose:
            print(f'Searching for raw DECam files with EXPNUM={expnum}')
        info,rows = fapi.search(jj, limit=1)
        if verbose:
            print(f'Found {len(rows)} files. Info={pformat(info)}')
        
        for row in rows:  # we only expect ONE expnum to match
            try:
                fid = row['md5sum']
                if verbose:
                    print(f'Downloading file {fid} to {outfilepath}')
                open(outfilepath, 'wb').write(fapi.retrieve(fid))
                #!print(f'Wrote file {fid} to {outfilepath}')
                gotfiles.add(str(outfilepath))
            except Exception as err:
                print(f'ERROR: {str(err)}; Record={row}')
                print(f'Could not retrieve file ({fid}) '
                      f'and write it to {outfilepath}')
    return(gotfiles)

##############################################################################


def main():
    parser = argparse.ArgumentParser(
        version='1.0.0',
        description='Download DECAM files given EXPNUMs',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('-e', '--expnum', type=int,
                        action='append',
                        help='EXPNUM of DECam file to retrieve' )
    parser.add_argument('--outdir', type=Path,
                        help='Directory to download files into. (must exist)' )
    parser.add_argument('--username',
                        help='Username (email) of an authenticated user' )
    parser.add_argument('--password',
                        help='Password of an authenticated user' )
    args = parser.parse_args()

    fapi =  helpers.api.FitsFile(verbose=True,
                                 username=args.username, password=args.password)
    get_files(args.expnum, args.outdir, fapi)

if __name__ == '__main__':
    main()
