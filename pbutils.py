import os
import sys
import glob
import csv
import json
from getpass import getpass
from constants import K
from pprint import pprint
import requests

import logging
logger = logging.getLogger('utils')

# FIXME:
# 1. Make constants for PB.collector, precs, PB.inputfile
# 2. Refactor into smaller libraries

def configure_logging(log_file = "perfbrowser.log", verbose = 0, append = False):
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    lvl = min(len(levels)-1, verbose+2)
    if log_file:
        logging.basicConfig(filename=log_file, filemode='a' if append else 'w', level=levels[lvl], format="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt='%m/%d/%Y %H:%M:%S')
    stderrLogger = logging.StreamHandler()
    stderrLogger.setLevel(levels[lvl])
    stderrFormatter = logging.Formatter('%(message)s')
    stderrLogger.setFormatter(stderrFormatter)
    logger = logging.getLogger()
    logger.addHandler(stderrLogger)
    return


def _get_files_list(paths, recurse):
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

# reads the user/pass or token from the environment
def _load_credentials(allow_token = True, quiet = False):
    if allow_token:
        token = os.getenv('PB_TOKEN', '')
        if (token):
            logger.debug("read auth token from environment")
            return (token,'')
        else:
            try:
                with open(K.path.token) as f:
                    token = f.read()
                if (token):
                    logger.debug("read auth token from file-system")
                    return (token, '')
            except:
                logger.debug("could not find auth token on file-system")
        logger.debug("no auth token found. Trying user/pass auth")
    user = os.getenv('PB_USER', '')
    if not quiet and (not user):
        logger.warn('You must set PB_TOKEN or (PB_USER, PB_PASSWD) in the environment')
    if not user:
        return None
    passwd = os.getenv('PB_PASSWD')
    if not quiet and (not passwd):
        logger.warn('PB_USER requires PB_PASSWD to be set')
    if not passwd:
        return None
    return (user, passwd)

def login():
    if (_load_credentials(quiet = True)):
        return
    user = ''
    while not user:
        user = raw_input("Username or e-mail: ")
    passwd = ''
    while not passwd:
        passwd = getpass("Password: ")
    token = get_token(user, passwd)
    if token:
        try:
            if not os.path.exists(K.path.settings):
                os.mkdir(K.path.settings)
            oldmask = os.umask(077)
            with open(K.path.token, 'w') as f:
                f.write(token)
            os.umask(oldmask)
            logger.info('saved auth token for future use')
        except Exception as e:
            logger.error("Could not save auth token: {0}".format(e))
    else:
        logger.warn("Could not retrieve auth token")

def logout():
    try:
        os.unlink(K.path.token)
        logger.debug("successfully logged out and removed all auth info")
    except:
        pass

def upload(paths, job_id=None, recurse=True):
    paths = [os.path.abspath(p) for p in paths]
    files = _get_files_list(paths, recurse)
    reclist = _get_reclist_from_files(files)
    data = {'precs': reclist}
    if job_id:
        logger.debug('using existing job ID: ' + job_id)
        data['job_id'] = job_id
    # auth = HTTPBasicAuth(os.environ.get('PB_USER'), os.environ.get('PB_PASSWD'))
    logger.info('uploading {0} records to: {1}'.format(len(reclist),  K.url.api.post.perfdata))
    r = requests.post(K.url.api.post.perfdata, json=data, auth=_load_credentials())
    if (r.status_code < 400):
        logger.info(('upload success: {0}').format(r.status_code))
        d = r.json()
        if not job_id:
            logger.info('Job name: {0}, JobId: {1}'.format(d['name'], d['id']))
        logger.debug(d)
    else:
        logger.info(('upload failed: {0}').format(r.json()))
    # pprint(reclist)

def jobs_list():
    url = K.url.api.jobs
    logger.debug('GET {0}'.format(url))
    r = requests.get(url, auth=_load_credentials())
    jsn = r.json()
    if (r.status_code < 400):
        logger.debug('jobs listing retrieved')
    else:
        logger.error(jsn)
    return jsn

def browse_job(job_id):
    url = K.url.api.perfdata(job_id)
    logger.debug('GET {0}'.format(url))
    r = requests.get(url, auth=_load_credentials())
    jsn = r.json()
    if (r.status_code < 400):
        logger.debug(jsn)
    else:
        logger.error(jsn)
    return jsn

def delete_job(job_id):
    url = K.url.api.job.delete(job_id)
    logger.debug('DELETE {0}'.format(url))
    r = requests.delete(url, auth=_load_credentials())
    if (r.status_code < 400):
        logger.info('deleted jobId {0}'.format(job_id))
    else:
        logger.error('could not delete job: {0}'.format(r.json()))
    return

def get_token(user, passwd):
    token = ''
    r = requests.get(K.url.api.userinfo, auth=(user, passwd))
    if (r.status_code < 400):
        token = r.json().get('token', '')
        logger.debug("Successfully acquired token for login")
    else:
        logger.error(r.json())
    return token

login()
