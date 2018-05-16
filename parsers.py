from .utils import clean_latin1
def parse_ebay_item(row,seller_id):
    data = {}
    photo = row.get("PictureDetails") or None
    if photo:
        photo = photo.get("GalleryURL","") or None
    
    listingdate = row.get("ListingDetails","") or None
    if listingdate:
        listingdate = listingdate.get("StartTime","") or None

    price = row.get("BuyItNowPrice","") or None
    if price:
        price = price.get("value","-1") or None

    quantitysold = row.get("SellingStatus","") or None
    if quantitysold:
        quantitysold = quantitysold.get("QuantitySold",-1) or -1
    else:
        quantitysold = -1

    data["photo"] = photo
    data["custom_label"] = row.get("SKU","") or None
    data["ebay_id"] = row.get("ItemID") or None
    data["product_name"] =  clean_latin1(row.get("Title")) or None
    data["quantity"] = row.get("QuantityAvailable",0) or 0
    data["date_of_listing"] = str(listingdate).split("T")[0].strip()
    data["price"] = price
    data["no_of_times_sold"] = quantitysold
    data["seller_id"] = seller_id
    return data