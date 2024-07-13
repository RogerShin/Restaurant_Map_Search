import subprocess
import platform
import requests
from io import BytesIO
from PIL import Image

# 判斷電腦作業系統， 開啟網頁
def open_map(filename):
    system = platform.system()
    try:
        if system == 'Darwin':  # macOS
            subprocess.run(['open', filename], check=True)
        elif system == 'Windows':  # Windows
            subprocess.run(['start', filename], shell=True, check=True)
        else:
            raise NotImplementedError(f'Unsupported operating system: {system}')
    except Exception as e:
        print(f"Failed to open map: {e}")



def get_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Error loading image")

def decode_image(image_content):
    return BytesIO(image_content)
