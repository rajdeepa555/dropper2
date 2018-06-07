# -*- coding: utf-8 -*-
import sys
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf8')
import platform
import logging
from requests import Request, Session
import time
import lxml.html
import datetime
# import urllib2
import urllib.request  as urllib2 
from random import randint

UserAgent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'


class AmazonScraper(object):
    
    def __init__(self,locale=None):
        self.domain = self._get_domain(locale)
        self.method = "GET"
        self.request = None
        self.response = None
        self.timeout = 10
        self.proxies = dict()
        self.session = Session()
        self._time = time.time()
        self.response_html = None
        self.response_dict = dict()
        self.is_captcha_in_response = False
        self.proxy_checker = dict()
        self.current_proxy = ""
        self.opener = None
        self.ua_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5','Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 Mobile/14F89 Safari/602.1','Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/59.0.3071.109 Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36 OPR/46.0.2597.32','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:54.0) Gecko/20100101 Firefox/54.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36','Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)','Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 OPR/46.0.2597.39','Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36']
        self.response_code = None
        self.get_prime_detail = False
        self.prime_price = ''
        self.in_stock = False
        self.is_prime = False
        self.asin = None
        self.need_to_fetch_prime_further = True


    def _init(self):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36')]
        # opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0')]

    def scrape(self,url):
        self._reset()
        self._execute(url)
        return self.response_dict

    def scrape_with_error(self,url):
        print("inside scrape_with_error")
        self._reset()
        r = self._execute2(url)
        if r and "503" in r:
            self.response_dict["503"] = True
        return self.response_dict



    def _reset(self):
        self.is_captcha_in_response = False
        self.response_dict = dict()
        self.response = None
        self.response_html = None
        self.request = None
        self.response_code = None

    def change_proxy(self,proxy):
        print("captcha found waiting for 10 sec")
        time.sleep(10)
        self.proxies.update({"https":proxy})
        print("updated proxy",self.proxies)


    def _execute(self, url):
        proxy = urllib2.ProxyHandler(self.proxies)
        opener = urllib2.build_opener(proxy)
        # opener = urllib2.build_opener()
        ua = self.ua_list[randint(0,70)]
        opener.addheaders = [('User-Agent', ua)]
        urllib2.install_opener(opener)
        try:
            self.response = urllib2.urlopen(url,timeout=5)
        except Exception as e:
            print("error in execute method",e)
            return {}
        self.process_response()

    def _execute2(self,url):
        proxy = urllib2.ProxyHandler(self.proxies)
        opener = urllib2.build_opener(proxy)
        # opener = urllib2.build_opener()
        ua = self.ua_list[randint(0,70)]
        opener.addheaders = [('User-Agent', ua)]
        urllib2.install_opener(opener)
        try:
            print("insedie _execute2")
            self.response = urllib2.urlopen(url,timeout=5)
            print("self.response",self.response)
            # raw_input("self.response")
        except Exception as e:
            print(e)
            res = {}
            if "503" in str(e) or "urlopen error timed out" in str(e):
                res["503"] = True
            return res
        self.process_response()


    def _unicode_text(self,text):
        return text.encode("ascii","ignore")

    def _is_prime(self,hxs):
        print("checking if prime")
        prime_strings = ["Fulfilled by Amazon","Dispatched from and sold by Amazon","Dispatched from Amazon","Ships from and sold by Amazon.com"]
        is_prime = False
        xpaths = []
        xpaths = ["//span[@id = 'merchant-info']//a[contains(text(),'%s')]","//div[@id='merchant-info']//a[contains(text(),'%s')]","//div[@id='shipsFromSoldBy_feature_div']//*[contains(text(),'%s')]","//span[@id='merchant-info'][contains(text(),'%s')]","//div[@id='merchant-info'][contains(text(),'%s')]"]
        for prime_string in prime_strings:
            for path in xpaths:

                path = path % (prime_string)
                if len(hxs.xpath(path))>0:
                    is_prime = True
                    break
            if is_prime == True:
                break
        self.response_dict.update({"is_prime":is_prime})

    def _get_prime_from_offer_page(self):
        if self.asin:
            url = "https://www.amazon.com/gp/offer-listing/%s?f_new=true&f_primeEligible=true" % (self.asin)
            headers = {'user-agent': user_agent}
            r = requests.get(url, headers=headers,proxies={"https":proxy})
            doc  = lxml.html.document_fromstring(r.content)
            if_captcha = False
            if "api-services-support@amazon.com" in r.content or "Robot Captcha" in r.content:
                if_captcha = True
                print("Captcha found")
            price_list = []
            price_blocks = doc.xpath('//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()')
            count = 0
            if len(price_blocks)>0:
                for p_block in price_blocks:
                    if count == 3:
                        break
                    price_list.append(p_block.strip())
                    count += 1
            
            return price_list,if_captcha

    def _in_stock(self,hxs):
        stock_strings = ["In stock","In Stock","In stock.","In Stock.","left in stock"]
        in_stock = False
        for stock_string in stock_strings:
            xpaths = ['//div[@id="availability"]//*[contains(text(),"%s")]','//div[@id="availability-brief"]//*[contains(text(),"%s")]']
            for path in xpaths:
                path = path % (stock_string)
                get_path = hxs.xpath(path)
                if len(get_path)>0:
                    in_stock = True
                    break
            if in_stock == True:
                break
        self.response_dict.update({"in_stock":in_stock})


    def _get_price(self,hxs):
        try:
            price_xpaths = ['//*[@id="priceblock_dealprice"]/text()','//span[@id="priceblock_ourprice"]/text()','//span[@id="priceblock_saleprice"]/text()','//span[@class="a-size-medium a-color-price offer-price a-text-normal"]/text()']
            price_found = False
            for xpath in price_xpaths:
                price = hxs.xpath(xpath)
                if len(price)>0:
                    price = price[0]
                    price_found = True
                    break
            if price_found == False:
                price = ""
            self.response_dict.update({"price":price})
        except:
            log.debug("price not found")

    def _get_prime_price(self,hxs):
        try:
            self.in_stock = False
            price_xpaths = ["//span[contains(text(),'Prime TM')]/parent::i/parent::span/parent::div/span[contains(@class, 'a-size-large')]//text()"]
            price_found = False
            for xpath in price_xpaths:
                price = hxs.xpath(xpath)
                print("price xpath",xpath,len(price))
                if len(price)>0:
                    price = price[0].strip()
                    price_found = True
                    self.prime_price = price
                    self.is_prime = True
                    break
            if price_found == False:
                price = ""
            else:
                stock_xpaths = ['//div[@class="a-row a-spacing-mini olpOffer"]//div[@class="olpBadgeContainer"]//following-sibling::ul//text()']
                for xpath in stock_xpaths:
                    stock = hxs.xpath(xpath)
                    print("stock xpath",xpath,len(stock))
                    if len(stock)>0:
                        stock = ''.join(stock)
                        stock = stock.strip().replace("\n","").replace(" ","")
                        if "shippingratesandreturnpolicy" in stock.lower():
                            self.in_stock = True
                            break
            self.prime_price = price
        except:
            log.debug("price not found")

    def _get_title(self,hxs):
        try:
            price_xpaths = ['//span[@id="productTitle"]/text()','//span[@id="ebooksProductTitle"]/text()']
            title_found = False
            for xpath in price_xpaths:
                title = hxs.xpath(xpath)
                
                if len(title)>0:
                    title = title[0].replace("\n","")
                    title = title.strip()
                    price_found = True
                    break
            if price_found == False:
                title = ""
            self.response_dict.update({"title":title})
        except:
            log.debug("title not found")

    def _parse_response(self):
        if "Robot Check" in self.response_html.decode('UTF-8'):
            print("captcha found")
            # f = open("captcha.html","wb")
            # f.write(self.response_html)
            # f.close()
            self.is_captcha_in_response = True
        elif self.response_html:
            # print("inside response_html",type(self.response_html))
            # responsesponse_html = self.response_html.split(b'Frequently bought together')[0]
            # response_html = self.response_html.split(b'Frequentlyfdsfgsdfboughttogether')[0]
            # print("1111")
            # check = open("ff.html","w")
            # print("2222")
            # check.write(str(response_html))
            # print("333")
            # check.close()
            # print("writing success")
            doc = lxml.html.document_fromstring(self.response_html)
            self._get_price(doc)
            if "price" in  self.response_dict and len(self.response_dict["price"].strip())>0:
                self._is_prime(doc)
            else:
                print("price not found and so we are not scraping prime")
            self._in_stock(doc)
            self._get_title(doc)


    def _update_response(self):
        if "Robot Check" in self.response_html.decode('UTF-8'):
            print("captcha found")
            # f = open("captcha.html","wb")
            # f.write(self.response_html)
            # f.close()
            self.is_captcha_in_response = True
        elif self.response_html:
            doc  = lxml.html.document_fromstring(self.response_html)
            self._get_prime_price(doc)


    def process_response(self):
        self.response_code = self.response.code
        if self.response.code==200:
            # self.response_html = self._unicode_text(self.response.read())
            self.response_html = self.response.read()
            if self.get_prime_detail == False:
                self._parse_response()
            else:
                self._update_response()
  

    def _get_domain(self,locale):
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



    def get_url_for_keyword(self,keyword):
        keyword = keyword.replace(" ","%20")
        url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+keyword
        # url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=LG%20OLED55C7P%2055-Inch%204K%20Ultra%20HD%20Smart%20OLED%20TV"
        product_url = ""
        try:
            response = urllib2.urlopen(url,timeout=5)
            doc  = lxml.html.document_fromstring(response.read())
            # file = open("url.txt","wb")
            # file.write(doc)
            if doc:
                product_url=doc.xpath("//li[1]//a[contains(@class,'a-link-normal s-access-detail-page')][contains(@class,'s-color-twister-title-link a-text-normal')][1]/@href")
                product_url = product_url[0].strip()
        except Exception as e:
            print("error",e)
            pass       
        return product_url