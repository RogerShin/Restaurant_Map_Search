from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
import os
import phone_data

os.system("clear")

class Window(ThemedTk):
    def __init__(self,theme="arc", **kwargs):
        super().__init__(theme=theme, **kwargs)
        self.title("今天要吃什麼")
        self.geometry('800x500')
        self.widgets()

    def widgets(self):
       phone_type = phone_data.phone_list
       mainFrame = ttk.Frame(borderwidth=1, relief='groove')
       city_label = ttk.Label(mainFrame, text="請選擇電話號碼:")

       # 創建 StringVar 物件
       self.combobox_number= tk.StringVar()
       self.select_city = ttk.Combobox(mainFrame, textvariable= self.combobox_number, values = phone_type)

       self.confirm_button = ttk.Button(mainFrame, text="確認", command=self.ok_btn)

       #test
       self.format_phone_label = ttk.Label(mainFrame,text="顯示轉換完成後的電話:")
       self.show_phone_value = ttk.Label(mainFrame)

       mainFrame.pack(ipadx=20, ipady=20)
       city_label.grid(column=0, row=0, sticky="w", padx=10, pady=(10, 5))
       self.select_city.grid(column=1, row=0, sticky="w", pady=(10, 5))
       self.format_phone_label.grid(column=0,row=1, sticky="w", padx=10, pady=(5, 5))
       self.show_phone_value.grid(column=1, row=1, sticky="w", pady=(5, 5))
       self.confirm_button.grid(column=3, row=2)

    def ok_btn(self):
        combobox_number = self.combobox_number.get()
        format_phone_number = phone_data.format_phone_number(combobox_number)
        # 更新標籤的文本
        self.show_phone_value.config(text=f"{format_phone_number}")
        
def main():
    window = Window()
    window.mainloop()

if  __name__ == '__main__':
    main()
