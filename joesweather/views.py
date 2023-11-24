from django.shortcuts import render, HttpResponse
import requests
import os


# def get(request):
#     # Create a GeoIP instance
#     g = GeoIP2()

#     # Get the client's IP address from the request's META data
#     client_ip = request.META['REMOTE_ADDR']

#     # Use GeoIP to get the latitude and longitude based on the client's IP address
#     lat, long = g.lat_lon(client_ip)


def temperature_forecast(request):
    # Get the user's IP Address
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]

    else:
        ip = request.META.get("REMOTE_ADDR")

    # Use abstract API to get the users' coordinates through their IP address
    abstract_api_key = os.environ.get("ABSTRACT_API_KEY")
    api_url = "https://ipgeolocation.abstractapi.com/v1/?api_key=" + abstract_api_key

    # Temporarily use a hard-coded IP address until the website's live. The code doesn't work locally
    response = requests.get(api_url + "&ip_address=" + "93.126.151.129").json()

    latitude = response["latitude"]
    longitude = response["longitude"]

    # Use Open Meteo's API to get the users' weather based off their latitude and longitude
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&forecast_days=1"
    ).json()

    tempArray = response["hourly"]["temperature_2m"]

    # Sort the day's temperatures
    tempArray.sort()

    # Extract the lowest and highest
    lowestTemp = tempArray[0]
    highestTemp = tempArray[-1]

    # Pass the temperature data to the template
    return render(
        request,
        "home.html",
        {"highestTemp": highestTemp, "lowestTemp": lowestTemp, "ip": ip},
    )
