from ebayapi.trading import Connection as Trading

class EbayHandler(object):
	
	def __init__(self):
		self.token = None
		# self.api = Trading(config_file = 'config.yaml')
		self.api = Trading(config_file = 'config.yaml',token=self.token)

	def _is_success(self,response):
		is_success = False
		if response and isinstance(response.dict(),dict):
			if response.dict().get("Ack","") == "Success" or response.dict().get("Ack","") == "Warning":
				is_success = True
		return is_success

	def get_session_id(self):
		ru_name = "Dean_Ku-DeanKu-GDOshipp-yiqngira"
		response = self.api.execute('GetSessionID',{'RuName':ru_name})
		if response and self._is_success(response):
			print("session id",response.dict())
			return response.dict()["SessionID"]

	def get_token_id(self,sessionId):
		response = self.api.execute('FetchToken',{'SessionID':sessionId})
		if response and self._is_success(response):
			return response.dict()["eBayAuthToken"]


	def get_all_orders(self,no_of_days=7):
		all_orders = []
		response = self.api.execute('GetOrders',{'NumberOfDays':no_of_days})
		if response and self._is_success(response):
			all_orders = response.dict().get("OrderArray",{}).get("Order",[])
		return all_orders

	def update_trading_api(self):
		self.api = Trading(config_file = 'config.yaml',token=self.token)

	def get_all_items(self,page_number=1):
		all_orders = []
		# response = self.api.execute('GetSellerList',{'EndTimeFrom': "2017-08-15T00:00:00",'EndTimeTo': "2017-11-15T00:00:00",'DetailLevel': "ItemReturnDescription",'Pagination' :{'EntriesPerPage':10,'PageNumber':page_number}})
		response = self.api.execute('GetMyeBaySelling',{'ActiveList':{'Include':True,'Pagination' :{'EntriesPerPage':10,'PageNumber':page_number},'SoldList': {'Include':False},'UnsoldList': {'Include':False},'DetailLevel':"ReturnAll"}})
		if response and self._is_success(response):
			all_orders = response.dict()
		return all_orders
		
	def get_order_status(self,order):
		order_status = "Pending"
		if order and isinstance(order,dict):
			order_status = order.get("OrderStatus",order_status)
		return order_status

	def is_order_contain_shipped_time(self,order):
		is_order_contain_shipped_time = False
		if order and isinstance(order,dict):
			if order.get("ShippedTime",None) is not None:
				is_order_contain_shipped_time = True
		return is_order_contain_shipped_time

	def _is_shipped(self,order):
		is_shipped = False
		if order and isinstance(order,dict):
			if self.is_order_contain_shipped_time(order) == True:
				is_shipped = True
		return is_shipped

	def get_awaiting_shipment_orders(self,no_of_days=7):
		all_orders = self.get_all_orders(no_of_days)
		unshipeed_orders = []
		if len(all_orders)>0:
			for order in all_orders:
				if self._is_shipped(order) == True:
					continue
				else:
					unshipeed_orders.append(order)
		return unshipeed_orders

	def set_shipment_tracking_info(self,shipment_info_dict):
		is_updated = False
		if shipment_info_dict and isinstance(shipment_info_dict,dict):
			response = self.api.execute('CompleteSale',shipment_info_dict)
			if response and self._is_success(response):
				is_updated = True
		return is_updated

	def set_item_price(self,item_price_dict):
		is_updated = False
		if item_price_dict and isinstance(item_price_dict,dict):
			try:
				response = self.api.execute('ReviseFixedPriceItem',item_price_dict)
				if response and self._is_success(response):
					is_updated = True
			except Exception as e:
				print("item has been deleted from ebay",e)
				pass
		return is_updated