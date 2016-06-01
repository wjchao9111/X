# -*- coding: utf-8 -*-
from X.tools.log import log


class VerifyException(Exception):
    def __init__(self, message=None):
        Exception.__init__(self)
        self.message = message


def sms_exception(function):
    def decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            log(
                title='SMS_EXCEPTION',
                content=[function, args, kwargs],
                logger='sms',
                level='error'
            )

    return decorator
