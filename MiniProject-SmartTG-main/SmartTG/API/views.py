# API/views.py
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

OPENWEATHER_API_KEY = "Api_Key"

@require_GET
def get_weather(request):
    """
    Expects GET parameters: city (required), state (optional)
    Returns JSON with city, temperature (°C), description.
    """
    city = request.GET.get('city')
    state = request.GET.get('state')  # optional

    if not city:
        return JsonResponse({'error': 'City not provided'}, status=400)

    # Build query - OpenWeather accepts "city,state,country" but state is optional
    q = city
    if state:
        q = f"{city},{state},IN"
    else:
        q = f"{city},IN"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={q}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        resp = requests.get(url, timeout=8)
        data = resp.json()
    except Exception as e:
        return JsonResponse({'error': 'Request failed', 'details': str(e)}, status=500)

    if resp.status_code != 200 or 'main' not in data:
        # pass the message from API (if any) for debugging
        msg = data.get('message', 'Unable to fetch weather data')
        return JsonResponse({'error': msg}, status=resp.status_code if resp.status_code else 400)

    result = {
        "city": data.get("name"),
        "temperature": f"{data['main']['temp']}",   # send number as string/plain
        "description": data['weather'][0]['description'].capitalize(),
        "humidity": data['main'].get('humidity'),
        "wind_speed": data.get('wind', {}).get('speed'),
    }
    return JsonResponse(result)
