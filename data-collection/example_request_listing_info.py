from basic_request import client_id, get_airbnb_listing_info, listing_id_example

'''
let's say we want to get the info for the listing with id 2056659
'''

params={
    "listing_id": listing_id_example,
    "locale": "en-US",
    "number_of_guests": 2
}

results = get_airbnb_listing_info(client_id, **params)

#EXAMPLES

# Description
description = results["description"]
print("description: " + description)

# Title
title = results["name"]
print("title: " + title)

# Location
location = results["address"]
print("location: " + location)

# City
city = results["city"]
print("city: " + city)

# Array of Image URLS
images = results["photos"]
print("image URL: " + images[0]["picture"])

# Rating
rating = results["star_rating"]
print("rating: " + str(rating))

# Number of rooms
bedrooms = results["bedrooms"]
bathrooms = results["bathrooms"]
print("bedrooms: " + str(bedrooms))
print("bathrooms: " + str(bathrooms))

# Price
price = results["price"]
print("price per day: " + str(price))

# Property Type
property_type = results["property_type"]
print("property type: " + property_type)