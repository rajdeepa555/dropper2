import urllib2 
proxy_list = ["170.130.58.123:3128","173.232.7.49:3128","104.140.164.94:3128","104.140.164.91:3128","89.32.71.12:3128","192.161.166.158:3128","173.232.7.46:3128","170.130.58.140:3128","173.232.7.169:3128","89.32.71.185:3128","50.2.15.35:3128","192.161.166.180:3128","170.130.58.158:3128","89.32.71.118:3128","89.32.71.35:3128","192.161.166.109:3128","192.161.166.12:3128","104.140.164.248:3128","50.2.15.187:3128","170.130.58.152:3128","50.2.15.95:3128","170.130.58.40:3128","50.2.15.188:3128","104.140.164.158:3128","173.232.7.61:3128"]

good = []
bad = []
for p in proxy_list:
	try:
		proxy = "https://"+ p
		proxies = {"https":proxy}
		opener = urllib2.build_opener()
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.382.93 Safari/527.36'),
								('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
								('accept-encoding','gzip, deflate, br')]
		opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.382.93 Safari/527.36')]
		proxy_handle = urllib2.ProxyHandler(proxies)
		opener = urllib2.build_opener(proxy_handle)
		urllib2.install_opener(opener)
		# url = "https://www.ipchicken.com/"
		# url = "http://pythonforbeginners.com"
		url = "https://www.amazon.com"
		# url = ""
		response = urllib2.urlopen(url,timeout=10)
		print("response",response)
		print(response.code)
		good.append(p)
		if response.code == 503 or response:
			print("proxy giving 503 status",proxy)
	except Exception as e:
		print("Exceptions",e)
		bad.append(proxy)


print("good proxies",good)
print("bad proxies",bad)

