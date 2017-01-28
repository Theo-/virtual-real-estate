import requests
import json


LISTING_ENDPOINT= "https://api.airbnb.com/v2/search_results"


url = "https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=10&_offset=0&fetch_facets=true&guests=1&ib=false&ib_add_photo_flow=true&location=Lake%20Tahoe%2C%20CA%2C%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&min_num_pic_urls=10&price_max=210&price_min=40&sort=1&user_lat=37.3398634&user_lng=-122.0455164"


def parse_get_request(url):
    '''
    Returns a dictionary of a url with all of the get params extracted.
    '''
    url = url.split("&")
    url[0] = url[0].split("?")[1]
    url2 = [ tuple(item.split('='))  for item in url]
    url3 = dict(url2)
    return url3


print(parse_get_request(url))


#r = requests.get("https://api.airbnb.com/v2/search_results",params=url3)
#print(r.text)


def json_prettyprint(dictionary):
    print(json.dumps(dictionary,sort_keys=True,indent=4))

#json_prettyprint(url3)


def get_airbnb_listing(client_id,**kwargs):
    pass


def get_airbnb_review(client_id,**kwargs):
    pass


def get_airbnb_hosts(client_id,**kwargs):
    pass


def get_airbnb_listing_info(client_id,**kwargs):
    pass


#r = requests.get("https://api.airbnb.com/v2/search_results",params=url3)
#print(r.text)
