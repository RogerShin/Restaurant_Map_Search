from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
import all_data

class Window(ThemedTk):
    def __init__(self, theme:str='arc', **kwargs):
        super().__init__(theme=theme, **kwargs)
        county:list = all_data.twn_county()
    
        # 创建一个 StringVar 变量
        self.combobox_var = tk.StringVar()

        select_county = ttk.Combobox(self, textvariable=self.combobox_var, values=county, state='readonly')

        # 初始值顯示台北市
        select_county.current(0)
        select_county.pack()


def main():
   window = Window()
   window.mainloop()

if __name__ == "__main__":
    main()