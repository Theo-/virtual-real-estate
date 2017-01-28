import requests
import json


LISTING_ENDPOINT= "https://api.airbnb.com/v2/search_results"


url = "locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=10&_offset=0&fetch_facets=true&guests=1&ib=false&ib_add_photo_flow=true&location=Lake%20Tahoe%2C%20CA%2C%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&min_num_pic_urls=10&price_max=210&price_min=40&sort=1&user_lat=37.3398634&user_lng=-122.0455164"

client_id="3092nxybyb0otqw18e8nh5nty"

def request_error_catching(URL, parameter):
    try:
        r = requests.get(URL, params=parameter)
    except requests.exceptions.Timeout as e:
        print e
        return 1
    except requests.exceptions.TooManyRedirects as e:
        print e
        return 1
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    return r

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
    r = request_error_catching(url,kwargs)
    if (r != 0):
        json_obj = r.json()
        listings = json_obj['search_results']
        return listings
    else:
        return 'ERROR: listing not found'

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
    r = request_error_catching(url,kwargs)
    if (r != 0):
        json_resp = r.json()
        json_reviews = json_resp['reviews']
        each_review = [ review for review in json_reviews]
        return each_review
    else:
        return 'ERROR: listing not found'


#get_airbnb_listing_info only needs client_id and listing_id
def get_airbnb_listing_info(client_id,**kwargs):

    '''
    this requires:
    client_id: 3092nxybyb0otqw18e8nh5nty
    listing_id	2056659 //ID of the listing you'd like to view reviews for.
    Optional:
        locale: en-US // language you want the output to be
        number_of_guests: 1 // Determines listing availability dates based on the # of guests.
    '''

    listing_info_url = "https://api.airbnb.com/v2/listings/" + str(kwargs["listing_id"]) + "?client_id=" + client_id + "&_format=v1_legacy_for_p3"
    kwargs.pop("listing_id")
    r = request_error_catching(listing_info_url, kwargs)
    if (r != 0):
        json_resp = r.json()
        return json_resp["listing"]
    else:
        return 'ERROR: listing not found'

'''
example object returned from get_airbnb_listing_info:
{
    "city": "Los Angeles",
    "collection_ids": null,
    "country": "United States",
    "has_double_blind_reviews": false,
    "id": 5116458,
    "instant_bookable": false,
    "lat": 34.02991065328165,
    "lng": -118.39945477165404,
    "medium_url": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=medium",
    "name": "Private Studio with Patio",
    "native_currency": "USD",
    "picture_url": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=large",
    "preview_encoded_png": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAECAIAAADJUWIXAAAAS0lEQVQIHQFAAL//AczIvxAE5fPs+fP19QoRFwHIxrwG/NYYFjXf2tINFygB3t7m/vvz7OHO9/byCxUpAdra7fz79NjNtOPYyB0pQb0GJtQJmKBIAAAAAElFTkSuQmCC",
    "price": 57,
    "price_formatted": "$57",
    "price_native": 57,
    "scrim_color": "#382A1F",
    "smart_location": "Los Angeles, CA",
    "thumbnail_url": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=small",
    "user": {
        "user": {
            "about": "Kim-Los Angeles, CA",
            "first_name": "Kim",
            "has_profile_pic": true,
            "id": 2917444,
            "identity_verified": true,
            "is_superhost": false,
            "picture_url": "https://a0.muscache.com/im/users/2917444/profile_pic/1359360836/original.jpg?aki_policy=profile_x_medium",
            "reviewee_count": 13,
            "thumbnail_url": "https://a0.muscache.com/im/users/2917444/profile_pic/1359360836/original.jpg?aki_policy=profile_small"
        }
    },
    "user_id": 2917444,
    "x_medium_picture_url": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_medium",
    "xl_picture_url": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_large",
    "address": "Los Angeles, CA 90034, United States",
    "bathrooms": 1,
    "bedrooms": 0,
    "beds": 1,
    "cancellation_policy": "strict",
    "country_code": "US",
    "has_availability": true,
    "hosts": [
        {
            "about": "Kim-Los Angeles, CA",
            "first_name": "Kim",
            "has_profile_pic": true,
            "id": 2917444,
            "identity_verified": true,
            "is_superhost": false,
            "picture_url": "https://a0.muscache.com/im/users/2917444/profile_pic/1359360836/original.jpg?aki_policy=profile_x_medium",
            "reviewee_count": 13,
            "thumbnail_url": "https://a0.muscache.com/im/users/2917444/profile_pic/1359360836/original.jpg?aki_policy=profile_small"
        }
    ],
    "listing_native_currency": "USD",
    "market": "Los Angeles",
    "min_nights": 14,
    "neighborhood": "South Robertson",
    "person_capacity": 2,
    "picture_count": 7,
    "picture_urls": [
        "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=large"
    ],
    "preview_encoded_pngs": [
        "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAECAIAAADJUWIXAAAAS0lEQVQIHQFAAL//AczIvxAE5fPs+fP19QoRFwHIxrwG/NYYFjXf2tINFygB3t7m/vvz7OHO9/byCxUpAdra7fz79NjNtOPYyB0pQb0GJtQJmKBIAAAAAElFTkSuQmCC"
    ],
    "primary_host": {
        "about": "Kim-Los Angeles, CA",
        "first_name": "Kim",
        "has_profile_pic": true,
        "id": 2917444,
        "identity_verified": true,
        "is_superhost": false,
        "picture_url": "https://a0.muscache.com/im/users/2917444/profile_pic/1359360836/original.jpg?aki_policy=profile_x_medium",
        "reviewee_count": 13,
        "thumbnail_url": "https://a0.muscache.com/im/users/2917444/profile_pic/1359360836/original.jpg?aki_policy=profile_small"
    },
    "property_type": "Apartment",
    "reviews_count": 14,
    "room_type": "Entire home/apt",
    "room_type_category": "entire_home",
    "scrim_colors": [
        "#382A1F"
    ],
    "special_offer": null,
    "state": "CA",
    "thumbnail_urls": [
        "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=small"
    ],
    "xl_picture_urls": [
        "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_large"
    ],
    "zipcode": "90034",
    "bed_type": "Real Bed",
    "bed_type_category": "real_bed",
    "currency_symbol_left": "$",
    "force_mobile_legal_modal": false,
    "require_guest_profile_picture": false,
    "access": "Everything in this unit is available for your use.  Outdoor patio set, private bathroom, and kitchenette.",
    "amenities": [
        "Internet",
        "Wireless Internet"
    ],
    "amenities_ids": [
        3,
        4,
        30,
        35,
        36,
        39,
        40,
        49,
        50
    ],
    "calendar_updated_at": "a week ago",
    "cancel_policy": 5,
    "cancel_policy_short_str": "Strict",
    "check_in_time": 16,
    "check_in_time_end": "22",
    "check_in_time_ends_at": 22,
    "check_in_time_start": "16",
    "check_out_time": 11,
    "cleaning_fee_native": 45,
    "currency_symbol_right": null,
    "description": "lmao",
    "description_locale": "en",
    "experiences_offered": "none",
    "extra_user_info": null,
    "extras_price_native": 45,
    "guests_included": 2,
    "has_agreed_to_legal_terms": null,
    "has_license": false,
    "has_viewed_cleaning": null,
    "has_viewed_ib_perf_dashboard_panel": null,
    "has_viewed_terms": true,
    "house_rules": "Please be respectful of other people living on the property.  No loud music, no musical instruments after 9pm, and no parties.  Please also leave the unit in the same condition that you found it in.",
    "instant_book_welcome_message": null,
    "instant_booking_allowed_category": "off",
    "interaction": "Since this is a private unit, there is little to no interaction.",
    "is_location_exact": true,
    "jurisdiction_names": [
        "City of Los Angeles",
        " CA"
    ],
    "jurisdiction_rollout_names": [
        "City of Los Angeles",
        " CA"
    ],
    "language": "en",
    "license": null,
    "listing_cleaning_fee_native": 45,
    "listing_monthly_price_native": 1400,
    "listing_price_for_extra_person_native": 25,
    "listing_security_deposit_native": 250,
    "listing_weekend_price_native": null,
    "listing_weekly_price_native": 399,
    "locale": "en",
    "localized_check_in_time_window": "4PM - 10PM",
    "localized_check_out_time": "11AM",
    "localized_city": "Los Angeles",
    "map_image_url": "https://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&markers=34.02991065328165%2C-118.39945477165404&size=480x320&zoom=15&client=gme-airbnbinc&channel=monorail-prod&signature=MixEmCP330Lnuf4I8BdP4CQ_TWw%3D",
    "max_nights": 90,
    "max_nights_input_value": 90,
    "min_nights_input_value": 14,
    "monthly_price_factor": 0.8,
    "monthly_price_native": 1400,
    "neighborhood_overview": "There is a shopping center one block away with a grocery store, drugstore, Starbucks, Subway, Papa Johns Pizza, etc.",
    "notes": "",
    "photos": [
        {
            "id": 37701363,
            "picture": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=large",
            "sort_order": 1,
            "caption": "",
            "large": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=large",
            "large_cover": "https://a0.muscache.com/ac/pictures/64014962/fab0406b_original.jpg?interpolation=lanczos-none&size=large_cover&output-format=jpg&output-quality=70",
            "medium": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=medium",
            "mini_square": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=mini_square",
            "scrim_color": "#382A1F",
            "small": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=small",
            "thumbnail": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=small",
            "preview_encoded_png": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAECAIAAADJUWIXAAAAS0lEQVQIHQFAAL//AczIvxAE5fPs+fP19QoRFwHIxrwG/NYYFjXf2tINFygB3t7m/vvz7OHO9/byCxUpAdra7fz79NjNtOPYyB0pQb0GJtQJmKBIAAAAAElFTkSuQmCC",
            "x_large": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_large",
            "x_large_cover": "https://a0.muscache.com/ac/pictures/64014962/fab0406b_original.jpg?interpolation=lanczos-none&size=x_large_cover&output-format=jpg&output-quality=70",
            "x_medium": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_medium",
            "x_small": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_small",
            "xl_picture": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=x_large",
            "xx_large": "https://a0.muscache.com/im/pictures/64014962/fab0406b_original.jpg?aki_policy=xx_large"
        }
    ],
    "picture_captions": [
        "",
        "",
        "",
        "",
        "",
        "",
        ""
    ],
    "price_for_extra_person_native": 25,
    "property_type_id": 1,
    "public_address": "Los Angeles, CA 90034, United States",
    "require_guest_phone_verification": false,
    "requires_license": false,
    "security_deposit_formatted": "$250",
    "security_deposit_native": 250,
    "security_price_native": 250,
    "space": "lmao",
    "square_feet": null,
    "star_rating": 4,
    "summary": "Modern, bright, small studio space with all the essentials.\n\nFull sized bed, full bathroom with standup shower, kitchenette w/ fridge, micro, coffee maker, and sink.  Small indoor table for two and private outdoor patio area.\n\nEasy, free street parking.\n\nNot available to show before booking.\n\nDates available are shown.",
    "time_zone_name": "America/Los_Angeles",
    "transit": "There is a Big Blue Bus Line bus stop directly in front of the house and there is a Metro Expo Line stop 2 blocks away.",
    "weekly_price_factor": 0.9,
    "weekly_price_native": 399,
    "additional_house_rules": "Please be respectful of other people living on the property.  No loud music, no musical instruments after 9pm, and no parties.  Please also leave the unit in the same condition that you found it in.",
    "in_building": false,
    "in_toto_area": false,
    "recent_review": {
        "review": {
            "comments": "lmao",
            "created_at": "2016-12-22T19:33:09Z",
            "id": 122318465,
            "listing_id": 5116458,
            "reviewee_id": 2917444,
            "reviewer": {
                "user": {
                    "first_name": "Matthew",
                    "has_profile_pic": true,
                    "id": 26696740,
                    "picture_url": "https://a0.muscache.com/im/pictures/64f17e5f-b47a-44a6-a87f-9f4b139845db.jpg?aki_policy=profile_x_medium",
                    "smart_name": "Matthew",
                    "thumbnail_url": "https://a0.muscache.com/im/pictures/64f17e5f-b47a-44a6-a87f-9f4b139845db.jpg?aki_policy=profile_small"
                }
            },
            "reviewer_id": 26696740,
            "role": "guest"
        }
    },
    "toto_opt_in": null,
    "wireless_info": null,
    "commercial_host_info": null,
    "listing_occupancy_info": {
        "show_occupancy_message": true
    },
    "review_rating_accuracy": 9,
    "review_rating_checkin": 10,
    "review_rating_cleanliness": 9,
    "review_rating_communication": 9,
    "review_rating_location": 10,
    "review_rating_value": 9,
    "is_business_travel_ready": false
}
'''


json_prettyprint(get_airbnb_listing_info("3092nxybyb0otqw18e8nh5nty", listing_id=5116458))

#r = requests.get("https://api.airbnb.com/v2/search_results",params=url3)
#print(r.text)
