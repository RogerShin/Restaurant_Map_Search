from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk, messagebox
import all_data
import folium
import os
import time
import tool
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
        # 按鈕
        self.submit = ttk.Button(self, text="確認", command=self.submit_address)

        # 測試创建一个标签来显示输出结果
        self.result_label = ttk.Label(self, text="地址: ")

        
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
        self.submit.pack()
        self.result_label.pack(pady=10)
        tableFrame.pack()
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 綁定Treeview點擊事件
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)
        
        
    def submit_address(self):

        combobox_value = self.combobox_var.get()
        entry_value = self.entry_address.get().strip()
        address = combobox_value + entry_value

        if not entry_value:
            messagebox.showwarning("輸入錯誤", "輸入不能為空白，請重新輸入。")
        else:
            lat, lng= all_data.input_address(address)
            self.restaurants:list = all_data.get_nearby_restaurants(lat, lng)
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
                          )
                self.tree.insert('', tk.END, values=value)
                print(restaurant)

    def on_tree_select(self, event):
        gmaps = all_data.gmaps
        selected_item = self.tree.selection()[0]
        restaurant_details = self.tree.item(selected_item, 'values')
        address = restaurant_details[4]
        geocode_result = gmaps.geocode(address)
        if not geocode_result:
            messagebox.showerror("錯誤", "無法獲取地理編碼，請檢查地址是否正確。")
            return
        
        location = geocode_result[0]['geometry']['location']
        lat, lng = location['lat'], location['lng']
        print("經維度:", lat, lng)

        map = folium.Map(location=[lat, lng], zoom_start=20)
        restaurantname =restaurant_details[0]
        folium.Marker([lat, lng], tooltip=restaurantname, popup=restaurantname).add_to(map)

        # 保存地圖為 HTML 文件
        map_file = "restaurant_location.html"
        map.save(map_file) 

        # 開啟電腦預設網頁
        tool.open_map(map_file)

        time.sleep(3)  # Adjust the sleep time as needed

        # Delete the HTML file after opening it
        if os.path.exists(map_file):
            os.remove(map_file)
            print(f"{map_file} has been deleted.")
        else:
            print(f"{map_file} does not exist.")
        




def main():
   window = Window()
   window.mainloop()

if __name__ == "__main__":
    main()