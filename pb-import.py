#!/usr/bin/env python2.7
import sys, os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description = 'Uploads perfbrowser data from one or more files or directores')
    parser.add_argument('-j', '--job-id', action='store', help="Import the data into an existing job")
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase logging level. Can be used multiple times')
    parser.add_argument('-r', '--recurse', action='store_true', default=False,
        help='Directories specified on the command-line will be recursively scanned for files to upload')
    parser.add_argument('-V', '--version', action='store_true', help='Print program version and exit')
    parser.add_argument('upload', metavar='PATH', nargs=argparse.REMAINDER,
        help='One or more files or directories to upload data from. Defaults to the working directory if none is specified')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    import logging
    from pbutils import pb_version, configure_logging, upload
    if args.version:
        print pb_version()
        sys.exit(0)

    logger = logging.getLogger('import')
    configure_logging(verbose=args.verbose)

    for p in args.upload:
        if not(os.path.exists(p)):
            logger.error("{path} does not exist".format(path=p))
            sys.exit(1)

    if (not(args.upload)):
        # use the current directory if none specified
        args.upload.append('.')

    rc =  upload(args.upload, args.job_id, args.recurse)
    sys.exit(rc)
