from dotmap import DotMap
import os

K = DotMap()
K.url.api.base = os.environ.get('PB_API_BASE_URL', 'http://127.0.0.1:5000/api/1.0')
K.url.api.post.perfdata = K.url.api.base + '/perfdata/'
K.url.api.userinfo = K.url.api.base + '/userinfo/'
K.path.settings = "{0}/.perfbrowser".format(os.environ['HOME'])
K.path.token = "{0}/.authtoken".format(K.path.settings)
