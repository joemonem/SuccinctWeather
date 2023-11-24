from django.shortcuts import render
import requests
import geocoder


def temperature_forecast(request):
    # Get the user's location
    user_latitude = 33.9317
    user_longitude = 35.6353

    # Make the request to the weather API
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={user_latitude}&longitude={user_longitude}&hourly=temperature_2m&forecast_days=1"
    ).json()

    # Extract temperature data
    tempArray = response["hourly"]["temperature_2m"]

    # Sort temperature array
    tempArray.sort()

    # Get lowest and highest temperature
    lowestTemp = tempArray[0]
    highestTemp = tempArray[-1]

    # Pass the temperature data to the template
    return render(
        request,
        "home.html",
        {"highestTemp": highestTemp, "lowestTemp": lowestTemp},
    )
