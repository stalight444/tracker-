import requests

def get_geolocation(api_key):
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key
    data = {
        "considerIp": "true"
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        location = response.json()
        print("Location found:")
        print(f"Latitude: {location['location']['lat']}")
        print(f"Longitude: {location['location']['lng']}")
        print(f"Accuracy: {location['accuracy']} meters")
    else:
        print("Error:", response.status_code)
        print("Message:", response.text)

if __name__ == "__main__":
    api_key = 'AIzaSyDq51XiJP_QX0z-8Xc12mDggdE6fUCBzIA'
    get_geolocation(api_key)
