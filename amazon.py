from .models import AmazonRun,AmazonRunDetails,EbayProductsCsvData
import math
from .utils import normalize_amazon_url

class CAmazon(object):
	
	def __init__(self,no_of_threads=1,group_index=0,amazon_run_id = None):
		self.amazon_url_list = []
		self.current_url = None
		self.no_of_threads = no_of_threads
		self.group_index = group_index
		self.amazon_run_id = amazon_run_id
		self._prepare_amazon_url_list()
		

	def _get_offset(self):
		amazon_url_start_index = 0
		amazon_url_end_index = 0
		amazon_url_in_a_group = int(math.floor(float(len(self.amazon_url_list))/float(self.no_of_threads)))
		amazon_url_start_index = self.group_index*amazon_url_in_a_group
		if self.no_of_threads == (self.group_index+1):
			amazon_url_end_index = len(self.amazon_url_list)
		else:
			amazon_url_end_index = amazon_url_start_index+(amazon_url_in_a_group)
		return amazon_url_start_index,amazon_url_end_index


	def _prepare_amazon_url_list(self):
		# amazon_url_list = EbayProductsCsvData.objects.all()
		amazon_url_list = AmazonRunDetails.objects.filter(run_id="")
		amazon_run_list = []
		# if self.amazon_run_id:
		# 	amazon_run_details = AmazonRunDetails.objects.filter(run_id=self.amazon_run_id)
		# 	for a in amazon_run_details:
		# 		amazon_run_list.append(a.amazon_url)
		if amazon_url_list is not None and len(amazon_url_list)>0:
			all_amazon_urls = []
			for amazon_instance in amazon_url_list:
				ebay_id = amazon_instance.ebay_id
				# if normalize_amazon_url(amazon_url.vendor_url) in amazon_run_list:
				# 	continue
				all_amazon_urls.append(amazon_instance.amazon_url+"@"+ebay_id)
			self.amazon_url_list = all_amazon_urls
			start_index, end_index = self._get_offset()
			self.amazon_url_list = all_amazon_urls[start_index:end_index+1]

	def _get_next_url_index(self):
		next_url_index = 0
		if self.current_url is not None:
			current_url_index = self.amazon_url_list.index(self.current_url)
			next_url_index =  (current_url_index+1) % len(self.amazon_url_list) 
		return next_url_index

	def get_amazon_url(self):
		if self.amazon_url_list is not None and len(self.amazon_url_list)>0:
			next_url_index = self._get_next_url_index() 
			print("next_url_index:",next_url_index)
			self.current_url = self.amazon_url_list[next_url_index]
			if len(self.amazon_url_list)-1 == next_url_index: 
				self.amazon_url_list = None
		else:
			self.current_url = None
		return self.current_url