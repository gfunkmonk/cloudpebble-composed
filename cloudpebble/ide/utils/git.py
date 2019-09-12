from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
import base64
import hashlib

__author__ = 'katharine'


def git_sha(content):
    return hashlib.sha1('blob %d\x00%s' % (len(content), content)).hexdigest()


def git_blob(repo, sha):
    return base64.b64decode(repo.get_git_blob(sha).content)