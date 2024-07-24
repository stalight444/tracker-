import webbrowser

def open_in_google_maps(lat, lng):
    url = f"https://www.google.com/maps?q={lat},{lng}"
    webbrowser.open(url)

if __name__ == "__main__":
    latitude = 10.6463232
    longitude = -61.489152
    open_in_google_maps(latitude, longitude)
