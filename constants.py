from dotmap import DotMap
import os

K = DotMap()
K.url.api.base = os.environ.get('PB_BASE_URL', 'http://127.0.0.1:5000/api/1.0')
K.url.api.post.perfdata = K.url.api.base + '/perfdata/'
K.url.api.userinfo = K.url.api.base + '/userinfo/'
K.url.api.jobs = K.url.api.base + '/jobs/'
K.url.api.perfdata = lambda jobId: "{0}/{1}/perfdata/".format(K.url.api.base, jobId)
K.url.api.job.delete = lambda jobId: "{0}/jobs/{1}/".format(K.url.api.base, jobId)
K.path.settings = "{0}/.perfbrowser".format(os.environ['HOME'])
K.path.token = "{0}/.authtoken".format(K.path.settings)
