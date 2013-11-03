# vim: fileencoding=utf-8 tw=100 expandtab ts=4 sw=4 :

from ._utils import *
from os import path as _path

BOWER_COMPONENTS_ROOT = _path.join(FOG_ROOT, 'bower')

BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = (
    'jquery#2.0.3',
    'angular#1.2.0-rc.3',
    'lodash',
    'bootstrap#3.0.1',
)
