# -*- coding: utf-8 -*-

class EbaySDKError(Exception):

    def __init__(self, msg, response=None):
        super(EbaySDKError, self).__init__(u'%s' % msg)
        self.message = u'%s' % msg
        self.response = response

    def __str__(self):
        return repr(self.message)


class ConnectionError(EbaySDKError):
    pass


class ConnectionConfigError(EbaySDKError):
    pass


class ConnectionResponseError(EbaySDKError):
    pass


class RequestPaginationError(EbaySDKError):
    pass


class PaginationLimit(EbaySDKError):
    pass