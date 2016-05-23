# -*- coding: utf-8 -*-

import traceback
import StringIO
import logging
import pprint
from X.settings import debugging


def get_exc():
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    error = fp.getvalue()
    return error


def log(title, content=None, logger='common', level='debug'):
    log = logging.getLogger(logger)
    if level == 'error':
        error = get_exc()
        if content is None:
            if error == 'None\n':
                log.error('%s' % title)
            else:
                log.error('%s\n%s' % (title, error))
        else:
            if error == 'None\n':
                log.error('%s\n%s' % (title, pprint.pformat(content)))
            else:
                log.error('%s\n%s\n%s' % (title, pprint.pformat(content), error))
    elif level == 'debug':
        if content is None:
            log.debug('%s' % title)
        else:
            log.debug('%s\n%s' % (title, pprint.pformat(content)))
    elif level == 'info':
        if content is None:
            log.info('%s' % title)
        else:
            log.info('%s\n%s' % (title, pprint.pformat(content)))
