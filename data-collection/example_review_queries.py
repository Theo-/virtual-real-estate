from basic_request import client_id, get_airbnb_listing

'''
Make a query where we want the language to be in english, currency in english,
guests to be 2, maximum price of $400 and in the Montreal area (longitude and latitude)
'''


params = {"locale":"en-US",
          "currency":"USD",
          "min_bedrooms":"2",
          "price_max":"400",
          "location":"Montreal",
          "_limit":"10"}

query_dict = get_airbnb_listing(client_id,**params)

# Example Uses:

# 1. Get Number of listings that match:
number_results = len(query_dict)
print(number_results)

# 2. Get a list of which city the listings are in:
cities = [ listing['listing']['city'] for listing in query_dict]

# 3. Get the picture urls for one listing.
picture_urls = query_dict[0]['listing']['picture_urls']
print(picture_urls)

# 4. Get the prices for all of the listings
prices = [ listing['pricing_quote']['nightly_price'] for listing in query_dict]
print(prices)
