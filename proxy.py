import math

class CProxy(object):
	
	def __init__(self,no_of_threads,group_index):
		self.proxy_list = []
		self.current_proxy = None
		self.no_of_threads = no_of_threads
		self.group_index = group_index
		self._prepare_proxy_list()

	def _get_offset(self):
		proxy_start_index = 0
		proxy_end_index = 0
		proxy_in_a_group = int(math.floor(float(len(self.proxy_list))/float(self.no_of_threads)))
		proxy_start_index = self.group_index*proxy_in_a_group
		if self.no_of_threads == (self.group_index+1):
			proxy_end_index = len(self.proxy_list)
		else:
			proxy_end_index = proxy_start_index+(proxy_in_a_group)
		return proxy_start_index,proxy_end_index


	def _add_https_prefix(self,proxy):
		return "https://"+proxy

	def _prepare_proxy_list(self):
		proxy_list = ["192.126.202.127:3128","192.126.202.188:3128","179.43.130.100:3128","192.126.204.59:3128","166.88.124.240:3128","45.33.157.60:3128","179.43.129.249:3128","45.33.145.194:3128","166.88.120.174:3128","192.126.202.7:3128","45.33.157.129:3128","166.88.120.31:3128","192.126.204.252:3128","166.88.120.87:3128","166.88.124.123:3128","45.33.145.185:3128","45.33.145.190:3128","166.88.120.27:3128","179.43.129.109:3128","192.126.202.172:3128","192.126.204.148:3128","45.33.145.108:3128","45.33.157.188:3128","45.33.157.195:3128","45.33.157.240:3128","45.33.145.29:3128","192.126.204.25:3128","179.43.130.159:3128","179.43.130.50:3128","192.126.202.218:3128","166.88.124.6:3128","166.88.120.149:3128","179.43.130.118:3128","179.43.130.70:3128","179.43.129.89:3128","166.88.124.224:3128","192.126.202.95:3128","179.43.130.123:3128","179.43.129.78:3128","45.33.157.78:3128","192.126.204.254:3128","179.43.129.19:3128","192.126.204.154:3128","179.43.130.127:3128","166.88.120.100:3128","179.43.129.211:3128","45.33.145.178:3128","166.88.124.35:3128","179.43.130.150:3128"]
		if proxy_list is not None and len(proxy_list)>0:
			all_proxies = []
			for proxy in proxy_list: 
				all_proxies.append(self._add_https_prefix(proxy))
			self.proxy_list = all_proxies
			start_index, end_index = self._get_offset()
			self.proxy_list = all_proxies[start_index:end_index+1]


	def _get_next_proxy_index(self):
		next_proxy_index = 0
		if self.current_proxy is not None:
			current_proxy_index = self.proxy_list.index(self.current_proxy)
			next_proxy_index =   (current_proxy_index+1) % len(self.proxy_list)
		return next_proxy_index

	def get_proxy(self):
		if self.proxy_list is not None and len(self.proxy_list)>0:
			self.current_proxy = self.proxy_list[self._get_next_proxy_index()]
		return self.current_proxy

	