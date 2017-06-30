#!/usr/bin/env python2.7
import sys, os
import argparse
from pbutils import configure_logging, jobs_list, browse_job, delete_job
import logging
from pprint import pprint

logger = logging.getLogger('pb-data')

def parse_args():
    parser = argparse.ArgumentParser(description = 'Browse and modify the datastore')
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
        pprint(jobs_list()['jobs'])
    elif args.show:
        job_id = int(args.show)
        pprint(browse_job(job_id)['perfdata'])
    elif args.delete:
        job_id = int(args.delete)
        delete_job(job_id)
