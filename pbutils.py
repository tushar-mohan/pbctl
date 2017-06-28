import os
import sys
import glob
import csv
import json
from constants import K
from pprint import pprint
from requests import post
from requests.auth import HTTPBasicAuth

import logging
logger = logging.getLogger('utils')

# FIXME:
# 1. Make constants for PB.collector, precs, PB.inputfile

def configure_logging(log_file = "app.log", log_level = 1, append = False):
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    lvl = min(len(levels)-1, log_level)
    if log_file:
        logging.basicConfig(filename=log_file, filemode='a' if append else 'w', level=levels[lvl], format="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt='%m/%d/%Y %H:%M:%S')
    stderrLogger = logging.StreamHandler()
    stderrLogger.setLevel(levels[lvl])
    stderrFormatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    stderrLogger.setFormatter(stderrFormatter)
    logger = logging.getLogger()
    logger.addHandler(stderrLogger)
    return


def _get_files_list_to_upload(paths, recurse, verbose):
    files = []
    for p in paths:
        if os.path.isdir(p):
            # dir
            files += glob.glob('{0}/*.papiex.csv'.format(p))
            if (recurse):
                try:
                    subdirs = [os.path.join(p, subdir) for subdir in os.listdir(p) if os.path.isdir(os.path.join(p, subdir))]
                except OSError as e:
                    logger.warn("Could not get subdirectory listing for {0}: {1}".format(p, e))
                    continue
                files += _get_files_list_to_upload(subdirs, recurse, verbose)
        else:
            files.append(p)
    return files

def _conv_numeric(s):
    try:
        v = int(s)
    except:
        try:
            v = float(s)
        except:
            v = s
    return v

def _csv_to_json(infile):
    with open(infile, 'r') as f:
        dictlist = list(csv.DictReader(f))
    for d in dictlist:
        for k in d:
            d[k] = _conv_numeric(d[k])
    return dictlist

# guesses collector based on string match in filename
def _guess_collector(infile):
    filename = infile.lower()
    # FIXME: read collector list from DB
    COLLECTORS = ['papiex', 'mpip', 'cpufreq', 'node_env', 'sysctl', 'job_env', 'mmpc']
    for c in COLLECTORS:
        if c in filename:
            return c
    raise Exception("Unknown collector: " + infile)

# def _guess_rank(rec):
#     # FIXME: these hardwired strings should come from the info field
#     # from the collector table. We probably want to do this post-processing
#     # in the REST api, as that has access to the DB already
#     rank = rec.get('Rank',
#                 rec.get('rank',
#                     rec.get('Mpi Rank', None)))
#     if (rank == None):
#         raise Exception("Unknown rank: ", rec)
#     return rank


# adds tags required for PB to the imported data
# reclist refers to the list of perf-records read from infile
def _add_tags_to_import(reclist, infile):
    collector = _guess_collector(infile)
    for rec in reclist:
        # add collector tag
        rec['PB.collector'] = collector
        rec['PB.inputfile'] = infile

def _get_reclist_from_files(files):
    reclist = []
    for f in files:
        recs = _csv_to_json(f)
        _add_tags_to_import(recs, f)
        reclist += recs
    return reclist


def upload(paths, recurse, verbose):
    paths = [os.path.abspath(p) for p in paths]
    files = _get_files_list_to_upload(paths, recurse, verbose)
    reclist = _get_reclist_from_files(files)
    logger.info('Uploading {0} records to: {1}'.format(len(reclist),  K.url.api.post.perfdata))
    data = {'precs': reclist, 'job_name': 'NAMD'}
    # auth = HTTPBasicAuth(os.environ.get('PB_USER'), os.environ.get('PB_PASSWD'))
    r = post(K.url.api.post.perfdata, json=data, auth=('tusharmohan@gmail.com','anandlok'))
    logger.debug(r.json())
    # pprint(reclist)


configure_logging('pbutils.log', 3, False)
