import datetime
import string
import re
import math
from datetime import datetime

LATIN_1_CHARS = (
    ('\xe2\x80\x99', "'"),
    ('\xc3\xa9', 'e'),
    ('\xe2\x80\x90', '-'),
    ('\xe2\x80\x91', '-'),
    ('\xe2\x80\x92', '-'),
    ('\xe2\x80\x93', '-'),
    ('\xe2\x80\x94', '-'),
    ('\xe2\x80\x94', '-'),
    ('\xe2\x80\x98', "'"),
    ('\xe2\x80\x9b', "'"),
    ('\xe2\x80\x9c', '"'),
    ('\xe2\x80\x9c', '"'),
    ('\xe2\x80\x9d', '"'),
    ('\xe2\x80\x9e', '"'),
    ('\xe2\x80\x9f', '"'),
    ('\xe2\x80\xa6', '...'),
    ('\xe2\x80\xb2', "'"),
    ('\xe2\x80\xb3', "'"),
    ('\xe2\x80\xb4', "'"),
    ('\xe2\x80\xb5', "'"),
    ('\xe2\x80\xb6', "'"),
    ('\xe2\x80\xb7', "'"),
    ('\xe2\x81\xba', "+"),
    ('\xe2\x81\xbb', "-"),
    ('\xe2\x81\xbc', "="),
    ('\xe2\x81\xbd', "("),
    ('\xe2\x81\xbe', ")")
)

def clean_latin1(data):
    try:
        return data.encode('utf-8')
    except UnicodeDecodeError:
        data = data.decode('iso-8859-1')
        for _hex, _char in LATIN_1_CHARS:
            data = data.replace(_hex, _char)
        return data.encode('utf8')

def get_simple_list_from_list_dict(list_of_dict,key_to_use):
	simple_list = []
	if list_of_dict:
		for item in list_of_dict:
			if key_to_use and key_to_use in item:
				simple_list.append(item.get(key_to_use))
	return simple_list

def normalize_amazon_url(url):
	amazon_url = url
	#remove everything after hash
	amazon_url = amazon_url.split("#")[0]
	if 'https' not in amazon_url and 'http' in amazon_url:
		amazon_url = amazon_url.replace('http','https')
	return amazon_url

def get_random_string():
	return "testing"

def get_run_id():
	current_datetime = datetime.now().strftime("%Y%m%d%H%M")
	random_id = 'RUN_{}'.format(get_random_string())
	return random_id+"_"+current_datetime

def make_amazon_url(asin):
	return "https://amazon.com/dp/"+str(asin)

def make_amazon_url_for_list_primes(asin):
	return "https://www.amazon.com/gp/offer-listing/%s?f_primeEligible=true"+str(asin)

def is_eligible_for_ebay_update(price,in_stock,is_prime,stock):
	is_eligible = False
	price_str = ""
	stock_str = "0"
	print("is_prime",is_prime)
	print("is_prime_type: ",type(is_prime))
	if price is not None and in_stock is not None and len(price)>0 and is_prime is not False:
		clear_price = re.findall("[0-9.]+",price)
		if len(clear_price)>0:
			print("clear_price",clear_price)
			price_str = str(float("".join(clear_price)))
			if in_stock == "True" or in_stock==True:
				if stock:
					stock_str = stock
				else:
					stock_str = "2"
		is_eligible = True

	return is_eligible,price_str,stock_str

def get_float(num):
	return_value = 0.00
	try:
		return_value = math.ceil(num*100)/100
	except:
		pass
	return return_value

def get_current_time():
	return datetime.datetime.now()

def get_time_diff_from_now(old_time):
	now = datetime.datetime.now()
	previous = old_time
	time_delta = now - previous
	exact_diff = divmod(time_delta.days*86400+time_delta.seconds,60)
	second_diff = exact_diff[1]
	return second_diff


def format_val(value):
	return format(value,'.2f')

def get_value_from_dict(dict_object,attrs_list):
	final_value = dict_object
	if len(attrs_list)>0:
		for attr in attrs_list:
			if attr in final_value:
				final_value = final_value.get(attr)
			else:
				final_value = None
				break
	else:
		final_value = None
	return final_value