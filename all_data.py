import googlemaps
import json
from dotenv import load_dotenv
import os
import re
from pprint import pprint

load_dotenv()

gmaps = googlemaps.Client(key=os.environ['GOOGLEAPI_KEY'])

# 抓台灣行政區資料
def twn_county():
    with open("countyname.json", "r") as countyfile:
        countyname_data = json.load(countyfile)

    county_list=[]
    for county in countyname_data['countyitems']['countyitem']:
        countyname = county['countyname']
        county_list.append(countyname)

    return county_list

# 取得地址座標
def input_address(address):

    geocode_result = gmaps.geocode(address)
    # 判斷地理編碼是否為None
    if not geocode_result:
        raise ValueError("無效的地址")
    
    location = geocode_result[0]['geometry']['location']
    lat = location['lat']
    lng = location['lng']
    
    return lat, lng

# 定義一個格式化電話號碼的函數
def format_phone_number(phone_number):
    
    if phone_number is None:
        phone_number = "未提供電話號碼"
        return phone_number
    else:
        # 去掉空格
        phone_number = phone_number.replace(" ", "")
        # 使用正則表達式匹配並格式化電話號碼
        match = re.match(r'^(\d{2})(\d{4})(\d{4})$', phone_number)
        phone_number = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return phone_number

# 定義是否為None, 自設定為 “未提供”
def price_web(price_level, website):
    if price_level is None:
        price_level = "未提供價位範圍"
    elif price_level == 1:
        price_level = "300 以內"
    elif price_level == 2:
        price_level = "300 至 900"
    elif price_level == 3:
        price_level = "900 至 1,800"
    else:
        price_level = "超過 1800"

    if website is None:
        website = "此餐廳無網頁"

    return price_level, website

# 獲取附近餐廳資料
def get_nearby_restaurants(lat, lng, meter=100):
    # 執行附近搜索
    nearby_results = gmaps.places_nearby(
        location = (lat, lng),
        radius = meter,
        keyword = 'restaurant',
        open_now = True,
        type = 'restaurant',
        language = 'zh-TW'
    )

    # 創建一個空的列表來存儲餐廳信息
    restaurant_list = []

    # 抓取每個餐廳的詳細資訊
    for place in nearby_results['results']:
        place_id = place['place_id']

        # 獲取詳細信息
        place_details = gmaps.place(place_id=place_id, language='zh-TW')
        
        # 獲取餐廳的相關信息
        name = place_details['result'].get('name')
        address = place_details['result'].get('formatted_address')
        phone_number = place_details['result'].get('formatted_phone_number')
        rating = place_details['result'].get('rating')
        user_ratings_total = place_details['result'].get('user_ratings_total')
        price_level = place_details['result'].get('price_level')
        website = place_details['result'].get('website')

        # 格式化電話號碼
        phone_number = format_phone_number(phone_number)

        # 檢查是否為None, 自設定為 未提供
        price_level, website = price_web(price_level, website)

         # 創建一個字典來存儲餐廳的信息
        restaurant_info = {
            'restaurant_name': name,
            'rating': rating,
            'user_ratings_total': user_ratings_total,
            'price_level': price_level,
            'address': address,
            'phone_number': phone_number,
            'website': website
        }

        restaurant_list.append(restaurant_info)

    return restaurant_list
