from django.http import HttpResponse
from django.shortcuts import render
from .models import UserVisit
import requests
import json
from ipware import get_client_ip
from django.conf import settings
from ua_parser import user_agent_parser

def track_visit(request):
    client_ip, is_routable = get_client_ip(request)
    ua_string = request.META.get('HTTP_USER_AGENT')
    parsed_ua = user_agent_parser.Parse(ua_string)
    
    # Extract device, browser, and OS information
    device_info = parsed_ua['device']['family']
    browser_info = parsed_ua['user_agent']['family']
    os_info = parsed_ua['os']['family']
    browser_version = parsed_ua['user_agent']['major']
    os_version = parsed_ua['os']['major']

    # Extract screen and viewport size
    screen_width = request.META.get('HTTP_SCREEN_WIDTH', 'unknown')
    screen_height = request.META.get('HTTP_SCREEN_HEIGHT', 'unknown')
    viewport_width = request.META.get('HTTP_VIEWPORT_WIDTH', 'unknown')
    viewport_height = request.META.get('HTTP_VIEWPORT_HEIGHT', 'unknown')

    # Extract timezone and language
    time_zone = request.META.get('HTTP_TIME_ZONE', 'unknown')
    language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'unknown')

    # Prepare data with IP address included
    data = {
        'considerIp': 'true',
        'wifiAccessPoints': [],  # Optional, if you want to include this in the request
        'cellTowers': [],        # Optional, if you want to include this in the request
        'ipAddress': client_ip   # Add IP address here
    }

    geolocation_url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={settings.GOOGLE_API_KEY}'
    geolocation_response = requests.post(geolocation_url, json=data)
    geolocation_data = geolocation_response.json()

    # Include additional details in the geolocation data
    geolocation_data['ipAddress'] = client_ip
    geolocation_data['device'] = device_info
    geolocation_data['browser'] = browser_info
    geolocation_data['browserVersion'] = browser_version
    geolocation_data['os'] = os_info
    geolocation_data['osVersion'] = os_version
    geolocation_data['screen'] = {
        'width': screen_width,
        'height': screen_height
    }
    geolocation_data['viewport'] = {
        'width': viewport_width,
        'height': viewport_height
    }
    geolocation_data['timeZone'] = time_zone
    geolocation_data['language'] = language

    # Save geolocation data including IP address to a JSON file
    with open('geolocation_data.json', 'w') as json_file:
        json.dump(geolocation_data, json_file, indent=4)

    # Save to database if needed
    user_visit = UserVisit(device_info=device_info, geolocation=json.dumps(geolocation_data))
    user_visit.save()

    return HttpResponse('Visit tracked successfully!')

def tracker_view(request):
    return render(request, 'tracker/tracker.html')
