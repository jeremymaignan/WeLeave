from geopy.geocoders import Nominatim

class Geo():

    def get_coordinates_from_address(self, input_text):
        address = input(input_text)
        geolocator = Nominatim(user_agent="uber")
        try:
            location = geolocator.geocode(address)
        except:
            print("geopy.geocoders Error")
            return {}
        if None == location:
            print("Address not found, try again")
            return self.get_coordinates_from_address(input_text)
        return {
            "input": address,
            "location": location,
            "lat": location.latitude,
            "long": location.longitude
        }
