from geopy.geocoders import Nominatim

class Geo():
    def get_geoloc(self, address):
        geolocator = Nominatim(user_agent="uber")
        try:
            location = geolocator.geocode(address)
            return {
                "lat": location.latitude,
                "long": location.longitude
            }
        except Exception as err:
            print("[ERROR] Cannot find geoloc. {}".format(err))
            return {}