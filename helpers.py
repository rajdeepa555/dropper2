import re
from utils import get_float

def is_value_empty(value):
	is_empty = True
	if value and len(str(value))>0:
		is_empty = False
	return is_empty


def is_eligible_for_out_of_stock(item):
	return_value = False
	if is_value_empty(item.get("price")) or item.get("in_stock") == False or item.get("is_prime") == False:
		return_value = True
	return return_value

def get_final_cost(ebay_item_obj,formula_obj,amazon_obj):
	price = re.findall("[0-9.]+",amazon_obj.get("price"))
	if len(price)>0:
		price = get_float(float("".join(price)))
	print("initial price before formula",price)
	if ebay_item_obj.margin_perc:
		margin_perc = ebay_item_obj.margin_perc * price/100
	else:
		margin_perc = formula_obj.perc_margin * price/100

	if ebay_item_obj.minimum_margin:
		fixed_margin = ebay_item_obj.minimum_margin
	else:
		fixed_margin = formula_obj.fixed_margin

	cost = price + formula_obj.ebay_listing_fee +  formula_obj.paypal_fees_fixed
	if margin_perc < fixed_margin:
		cost = cost + fixed_margin
	else:
		cost = cost + margin_perc
	p = 1-((formula_obj.ebay_final_value_fee + formula_obj.paypal_fees_perc)/100)
	cost_after_profit = get_float(cost / p) 

	print("price after formula",cost_after_profit)
	return cost_after_profit

def backup():
	from .models import EbaySellerItems
	import csv
	csv_writer = csv.writer(open("ebay_item.csv","w"))
	all_ebay_items = EbaySellerItems.objects.all()
	csv_writer.writerow(["photo","product_name","ebay_id","custom_label","price","quantity","no_of_times_sold","date_of_listing","is_active","margin_perc","minimum_margin","stock_level","status","flag"])
	for itm in all_ebay_items:
		csv_writer.writerow([itm.photo,itm.product_name,itm.ebay_id,
					itm.custom_label,itm.price,itm.quantity,
					itm.no_of_times_sold,itm.date_of_listing,
					itm.is_active,itm.margin_perc,itm.minimum_margin,
					itm.stock_level,itm.status,itm.flag])




def get_final_stock(custom_stock):
	final_stock = "2"
	if custom_stock:
		final_stock = custom_stock
	return final_stock


