#!/usr/bin/env python2.7
import sys, os
import argparse
from pbutils import configure_logging, jobs_list, browse_job, delete_job
import logging
import json
from pprint import pprint

logger = logging.getLogger('rest')

def parse_args():
    parser = argparse.ArgumentParser(description = 'REST client to browse and modify the PerfBrowser database')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase logging level. Can be used multiple times')
    parser.add_argument('-l', '--list', action='store_true', help="List all jobs owned by user")
    parser.add_argument('-s', '--show', metavar='JOB_ID', action='store', help="Dump data for the specified job")
    parser.add_argument('-d', '--delete', metavar='JOB_ID', action='store', help="Delete specified job")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()

    configure_logging(verbose=args.verbose)

    if args.list:
        print json.dumps(jobs_list()['jobs'], indent=4)
    elif args.show:
        job_id = int(args.show)
        print json.dumps(browse_job(job_id)['perfdata'], indent=4)
    elif args.delete:
        job_id = int(args.delete)
        delete_job(job_id)
