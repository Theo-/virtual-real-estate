import requests
import json


LISTING_ENDPOINT= "https://api.airbnb.com/v2/search_results"


url = "locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=10&_offset=0&fetch_facets=true&guests=1&ib=false&ib_add_photo_flow=true&location=Lake%20Tahoe%2C%20CA%2C%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&min_num_pic_urls=10&price_max=210&price_min=40&sort=1&user_lat=37.3398634&user_lng=-122.0455164"

client_id="3092nxybyb0otqw18e8nh5nty"

def parse_get_request(url):
    '''
    Returns a dictionary of a url with all of the get params extracted.
    '''
    url = url.split("&")
    url2 = [ tuple(item.split('='))  for item in url]
    url3 = dict(url2)
    return url3


def json_prettyprint(dictionary):
    print(json.dumps(dictionary,sort_keys=True,indent=4))


def get_airbnb_listing(client_id,**kwargs):
    '''
    See this doc on airbnb for info on parameters accepted: http://airbnbapi.org/#listing-search

    This method will return a Python dictionary which has various values describing the listings
    for your query. See LISTINGS_EXAMPLE.txt to see what kind of values are returned.

    '''
    url = "https://api.airbnb.com/v2/search_results"
    kwargs['client_id'] = client_id
    r = requests.get(url,params=kwargs)
    json_obj = r.json()
    listings_overhead = json_obj['search_results']
    each_listing = [ listing['listing'] for listing in listings_overhead]
    return each_listing


get_airbnb_listing(client_id,**params)

def get_airbnb_review(client_id, **kwargs):

    '''
    This requires :
        client_id:	3092nxybyb0otqw18e8nh5nty //This works for the moment
        role:	all  //Not sure, but it's required.
        listing_id	2056659 //ID of the listing you'd like to view reviews for.
    Optional :
        locale	en-US	Desired lagnuage
        currency USD	Desired currency
        _format	for_mobile_client || for_search_results || for_search_results_with_minimal_pricing	Not sure what the difference is.
        _limit	10	Number of reviews to show at a time.
        _offset	0	Number of reviews to offset.
    '''

    url = "https://api.airbnb.com/v2/reviews?role=all&client_id="+client_id
    r = requests.get(url,params=kwargs)
    json_resp = r.json()
    json_reviews = json_resp['reviews']
    each_review = [ review for review in json_reviews]
    return each_review


def get_airbnb_hosts(client_id,**kwargs):
    pass


def get_airbnb_listing_info(client_id,**kwargs):
    pass


#r = requests.get("https://api.airbnb.com/v2/search_results",params=url3)
#print(r.text)
