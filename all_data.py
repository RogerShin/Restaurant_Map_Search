import googlemaps
import re
from dotenv import load_dotenv
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.environ['GOOGLEAPI_KEY'])

#取得台北市士林區士東路299巷的地理編碼
geocode_result = gmaps.geocode(address = "台北中山北路")
print(geocode_result)