from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .applications.find_nearest_location import find_nearest_location
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import json

tsunami_evac_df = pd.read_csv('main/applications/tsunami_evac.csv')

# Create your views here.
def main(request):
  return render(request, 'index.html')

@csrf_exempt
def provide_nearest_location(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      current_latitude = data.get('latitude')
      current_longitude = data.get('longitude')
      current_location = (current_latitude, current_longitude)
      
      nearest_location, distance = find_nearest_location(current_location, tsunami_evac_df)
      
      if nearest_location is not None:
        response_data = {
          'facility_name': nearest_location['施設・場所名'],
          'address': nearest_location['住所'],
          'latitude': nearest_location['緯度'],
          'longitude': nearest_location['経度'],
          'distance': round(distance, 2),
          'google_maps_url': f"https://www.google.com/maps/dir/?api=1&destination={nearest_location['緯度']},{nearest_location['経度']}"
        }
        return JsonResponse(response_data)
      else:
        return JsonResponse({'error': '津波避難場所が見つかりませんでした'}, status=404)
      
    except json.JSONDecodeError:
      return JsonResponse({'error': '無効なデータが送信されました'}, status=400)
  
  return JsonResponse({'error': 'POSTリクエストが必要です'}, status=405)