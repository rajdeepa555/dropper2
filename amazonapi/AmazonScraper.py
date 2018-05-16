from amazonapi import log
from requests import Request, Session
import time

class AmazonScraper(object):
    
    def __init__(self,locale=None):
        self.domain = self._get_domain(locale)
        self.method = "GET"
        self.request = None
        self.response = None
        self.timeout = 10
        self.proxies = dict()
        self.session = Session()

    def scrape(self,url):
        return self._excute(url)

    def _execute(self, url):
        "Executes the HTTP request."
        log.debug('execute: url=%s' % (url))

        self.build_request(url)
        self.execute_request()

        log.debug('total time=%s' % (time.time() - self._time))

        return self.response

    def build_request(self, url):
        headers = self.build_request_headers(url)
        headers.update({'User-Agent': UserAgent})

        request = Request(self.method,
                          url,
                          headers=headers
                          )

        self.request = request.prepare()

    def build_request_headers(self, verb):
        return {}

    def build_request_data(self, verb, data, verb_attrs):
        return ""

    def execute_request(self):

        log.debug("REQUEST : %s %s"
                  % ( self.request.method, self.request.url))
        log.debug('headers=%s' % self.request.headers)
        log.debug('body=%s' % self.request.body)

        self.response = self.session.send(self.request,
                                          verify=True,
                                          proxies=self.proxies,
                                          timeout=self.timeout,
                                          allow_redirects=True
                                          )

        log.debug('elapsed time=%s' % self.response.elapsed)
        log.debug('status code=%s' % self.response.status_code)
        log.debug('headers=%s' % self.response.headers)
        log.debug('content=%s' % self.response.text)

        

    def _get_domain(locale):
        DOMAINS = {
                'CA': 'ca',
                'DE': 'de',
                'ES': 'es',
                'FR': 'fr',
                'IN': 'in',
                'IT': 'it',
                'JP': 'co.jp',
                'UK': 'co.uk',
                'US': 'com',
                'CN': 'cn'
            }
        return DOMAINS[locale]

