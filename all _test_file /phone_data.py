import re
def format_phone_number(phone_number):

    if phone_number is None:
        phone_number = "未提供電話號碼"
        return phone_number
    
    # 去掉空格
    phone_number = phone_number.replace(" ", "")

    if phone_number.startswith("09") and len(phone_number)==10:
        # 使用正則表達式匹配並格式化電話號碼
        mobile_phone = re.match(r'^(\d{4})(\d{3})(\d{3})$', phone_number)
        if mobile_phone:
            phone_number = f"{mobile_phone.group(1)}-{mobile_phone.group(2)}-{mobile_phone.group(3)}"
    elif phone_number.startswith("0") and len(phone_number)==10:
        local_phone = re.match(r'^(\d{2})(\d{4})(\d{4})$', phone_number)
        if local_phone:
            phone_number = f"{local_phone.group(1)}-{local_phone.group(2)}-{local_phone.group(3)}"
    elif phone_number.startswith("0") and len(phone_number)>10:
         # #抓取後面的字
        special_number = re.match(r'^(\d{2})(\d{4})(\d{4})#(\d+)$', phone_number)
        if special_number:
            phone_number = f"{special_number.group(1)}-{special_number.group(2)}-{special_number.group(3)} #{special_number.group(4)}"
    else:
        phone_number = "電話號碼格式有錯誤"
    
    return phone_number

phone_list=['0916 682 230', '02 1234 5678', '02 2833 9696 #336', '0928 512 265', '03 2235 5678']
