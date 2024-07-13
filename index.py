from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
import all_data
import webbrowser
import os
import time
import tool
import random
from PIL import Image, ImageTk

os.system("clear")

class Window(ThemedTk):
    def __init__(self, theme:str='arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.geometry('800x300')
        county:list = all_data.twn_county()
    
        # 创建一个 StringVar 变量
        self.combobox_var = tk.StringVar()

        # 下拉式選單
        self.select_county = ttk.Combobox(self, textvariable=self.combobox_var, values=county, state='readonly',width= 8)
        # 初始值顯示台北市
        self.select_county.current(0)
        # 輸入欄位
        self.entry_address = ttk.Entry(self)
        self.entry_address.focus()

        # 數值調整滑桿
        self.distance = tk.Scale(self, from_=100, to=3000, orient='horizontal',resolution=50, length=200)
        self.distance.set(100)

        # 按鈕
        self.submit = ttk.Button(self, text="確認", command=self.submit_address)

        # 顯示隨機餐廳的按鈕
        self.show_random_button = ttk.Button(self, text="顯示隨機餐廳", command=self.show_random_restaurant)

        # 測試创建一个标签来显示输出结果
        self.result_label = ttk.Label(self, text="地址: ")

        # 數值滑桿
        tableFrame = ttk.Frame(self, borderwidth=1, relief='groove')
        columns = ('restaurant_name', 'rating', 'user_ratings_total', 'price_level', 'address', 'phone_number')
        # browse 只能單選
        self.tree = ttk.Treeview(tableFrame, columns=columns, show='headings', selectmode='browse')

        # define headings
        self.tree.heading('restaurant_name', text='餐廳名稱')
        self.tree.heading('rating', text='餐廳評分')
        self.tree.heading('user_ratings_total', text='評論數')
        self.tree.heading('price_level', text='消費金額')
        self.tree.heading('address', text='地址')
        self.tree.heading('phone_number', text='電話')

        # 定義欄位寬度
        self.tree.column('restaurant_name', minwidth=100, anchor='center')
        self.tree.column('rating', width=100, anchor='center')
        self.tree.column('user_ratings_total', width=100, anchor='center')
        self.tree.column('price_level', width=130, anchor='center')
        self.tree.column('address', minwidth=300, anchor='center')
        self.tree.column('phone_number', width=250, anchor='center')

        # 水平滾動條
        h_scrollbar = ttk.Scrollbar(tableFrame, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # 垂直滾動條
        v_scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 關聯 Treeview
        self.tree.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        self.select_county.pack()
        self.entry_address.pack()
        self.distance.pack()
        self.submit.pack()
        self.show_random_button.pack()
        self.result_label.pack(pady=10)
        tableFrame.pack()
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 綁定Treeview點擊事件
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)

        # 追蹤隨機餐廳視窗的狀態
        self.random_window_open = False
        
    def submit_address(self):

        combobox_value = self.combobox_var.get()
        entry_value = self.entry_address.get().strip()
        distance_value = int(self.distance.get())
        address = combobox_value + entry_value

        if not entry_value:
            messagebox.showwarning("輸入錯誤", "輸入不能為空白，請重新輸入。")
        else:
            lat, lng= all_data.input_address(address)
            self.restaurants:list = all_data.get_nearby_restaurants(lat, lng, distance_value)
            # 測試輸出
            self.result_label.config(text=f"地址: {address}")
            print("資料數",len(self.restaurants))
            self.insert_data(self.restaurants)
    
    def insert_data(self, restaurants):
        # 清除现有数据
        for info in self.tree.get_children():
            self.tree.delete(info)

        # 將餐廳資料寫入
        for restaurant in restaurants:
                value = (restaurant['restaurant_name'],
                          restaurant['rating'],
                          restaurant['user_ratings_total'],
                          restaurant['price_level'],
                          restaurant['address'],
                          restaurant['phone_number'],
                          restaurant['website'],
                          restaurant['place_id'],
                          restaurant['photo_url']
                        )
                self.tree.insert('', tk.END, values=value)

    def on_tree_select(self, event):
        gmaps = all_data.gmaps
        selected_item = self.tree.selection()[0]
        restaurant_details = self.tree.item(selected_item, 'values')
        address = restaurant_details[4]
        geocode_result = gmaps.geocode(address)
        if not geocode_result:
            messagebox.showerror("錯誤", "無法獲取地理編碼，請檢查地址是否正確。")
            return
        
        place_id = restaurant_details[7]  # assuming place_id is at index 7 in restaurant_details
    
        # Generate the Google Maps query URL
        query = f"https://www.google.com/maps/search/?api=1&query={address}&query_place_id={place_id}"
        
        # Open the query URL in the default web browser
        webbrowser.open(query)


    def show_random_restaurant(self):
        
        if not self.tree.get_children():
            messagebox.showwarning("警告", "餐廳資料表格中沒有資料。")
            return

        if self.random_window_open:
            messagebox.showinfo("提示", "隨機餐廳視窗已經開啟。")
            return
        
         # 標記為已打開隨機餐廳視窗
        self.random_window_open = True
        

        # 隨機選擇一個餐廳
        random_restaurant = random.choice(self.restaurants)
        
        # 創建一個新窗口來顯示餐廳資訊和圖片
        new_window = tk.Toplevel(self)
        new_window.title(random_restaurant['restaurant_name'])

        # 抓取餐廳的照片的url
        photo_url = random_restaurant['photo_url']
        print(photo_url)

        # 顯示照片
        if photo_url:
            try:
                # 讀取url和顯示照片
                image_byt = tool.get_image(photo_url)
                image_b64 = tool.decode_image(image_byt)
                image = Image.open(image_b64)
                # image = image.resize((300, 300), Image.ANTIALIAS)
                self.photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(new_window, image=self.photo)
                image_label.pack()
                # 監聽視窗關閉事件，標記隨機餐廳視窗已關閉
                new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_random_window_close(new_window))
            except Exception as e:
                error_label = ttk.Label(new_window, text="圖片加載失敗", justify=tk.LEFT, foreground="red")
                error_label.pack()
                # 監聽視窗關閉事件，標記隨機餐廳視窗已關閉
                new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_random_window_close(new_window))
        
        # 顯示餐廳資訊
        info_text = f"餐廳名稱: {random_restaurant['restaurant_name']}\n"
        info_text += f"評分: {random_restaurant['rating']}\n"
        info_text += f"評論數: {random_restaurant['user_ratings_total']}\n"
        info_text += f"消費金額: {random_restaurant['price_level']}\n"
        info_text += f"地址: {random_restaurant['address']}\n"
        info_text += f"電話: {random_restaurant['phone_number']}\n"
        info_text += f"網站: {random_restaurant['website']}\n"
        
        info_label = ttk.Label(new_window, text=info_text, justify=tk.LEFT)
        info_label.pack(pady=10)

    def on_random_window_close(self, window):
        # 視窗關閉時
        window.destroy()
        # 標記隨機餐廳視窗已關閉
        self.random_window_open = False

def main():
   window = Window()
   window.mainloop()

if __name__ == "__main__":
    main()