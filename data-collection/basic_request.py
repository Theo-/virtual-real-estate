import requests
import json


LISTING_ENDPOINT= "https://api.airbnb.com/v2/search_results"


url = "https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=10&_offset=0&fetch_facets=true&guests=1&ib=false&ib_add_photo_flow=true&location=Lake%20Tahoe%2C%20CA%2C%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&min_num_pic_urls=10&price_max=210&price_min=40&sort=1&user_lat=37.3398634&user_lng=-122.0455164"

url = url.split("&")

url[0] = url[0].split("?")[1]


url2 = [ tuple(item.split('='))  for item in url]

url3 = dict(url2)


r = requests.get("https://api.airbnb.com/v2/search_results",params=url3)
print(r.text)
