import subprocess
import platform

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