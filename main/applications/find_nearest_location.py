import numpy as np
import pandas as pd
import geopy.distance

#tsunami_evac_df = pd.read_csv('main/applications/tsunami_evac.csv')

def find_nearest_location(current_location, evac_df):
  min_distance = float('inf')
  nearest_location = None
  
  for index, row in evac_df.iterrows():
    location = (row['緯度'], row['経度'])
    distance = geopy.distance.distance(current_location, location).km
    if distance < min_distance:
      min_distance = distance
      nearest_location = row
  
  return nearest_location, min_distance

"""
current_location = (35.504666, 139.620566)
nearest_location, distance = find_nearest_location(current_location, tsunami_evac_df)

if nearest_location is not None:
  print(f"最寄りの津波避難場所: {nearest_location['施設・場所名']}")
  print(f"住所: {nearest_location['住所']}")
  print(f"緯度: {nearest_location['緯度']}, 経度: {nearest_location['経度']}")
  print(f"現在位置からの距離: {distance:.2f} km")
  google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={nearest_location['緯度']},{nearest_location['経度']}"
  print(f"Google Maps URL: {google_maps_url}")
else:
  print("津波避難場所が見つかりませんでした。")
"""