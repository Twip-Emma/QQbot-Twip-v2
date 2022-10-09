import asyncio
import time
# 第一层加密（ascii移位）
def _encrypt_string(message):
    encode_result = ""
    for char in message:
        char_int = ord(char)
        if char.isalpha():
            if 64 < char_int < 78 or 96 < char_int < 110:
                encode_result += "K0" + str((char_int + 13) * 2) + "|"
            else:
                encode_result += "K1" + str(char_int - 23) + "|"

        elif '\u4e00' <= char <= '\u9fff':
            encode_result += "K2" + str(char_int + 24) + "|"
        else:
            encode_result += "K3" + str(char_int) + "|"
    encode_result = _tenTotwo(encode_result)
    return encode_result


# 解密
def _decrypt_string(message):
    decode_result = ""
    message_list = message.split("|")
    message_list.remove("")
    for i in message_list:
        type_ = i[:2]
        char_number = int(i[2:])
        if type_ == "K0":
            char_number = int(char_number / 2 - 13)
        elif type_ == "K1":
            char_number = char_number + 23
        elif type_ == "K2":
            char_number = char_number - 24
        else:
            char_number = char_number

        decode_result += chr(char_number)
    return decode_result


def _ten_to_two(num):
    num = str(bin(int(num)))
    num = num.replace("0b","")
    return num


def _two_to_ten(num):
    num = str(int(str(num),2))
    return num


# 第二层加密（转二进制）
def _tenTotwo(message):
    encode_getter = ""
    message_list = message.split("|")
    message_list.remove("")
    for item in message_list:
        item = item.replace("K","")
        item = "1" + item
        binstring = _ten_to_two(item)
        encode_getter += binstring + "|"
    return encode_getter


# 第三层加密（S盒压缩）
def _s_zip(message):
    encode_getter = ""
    message_list = message.split("|")
    message_list.remove("")
    for item in message_list:
        er_type = ["","","",""]
        item = "P".join(item)
        item = item.split("P")
        er_type[0] = item[0]
        er_type[1] = item[1]
        er_type[3] = item[len(item)-1]
        er_type[2] = item[len(item)-2]
        item.pop(0)
        item.pop(0)
        item.pop(len(item)-1)
        item.pop(len(item)-1)
        a = ""
        b = "1"
        for a_i in er_type:
            a += a_i
        for b_i in item:
            b += b_i
        a = _two_to_ten(a)
        b = _two_to_ten(b)
        finall_num = a + "G" + b
        encode_getter += finall_num + "|"
    return encode_getter


# 解密主程序
def _return_box_qs(message):
    message_list = message.split("|")
    message_list.remove("")
    encode_getter = ""
    for item in message_list:
        k = ""
        # 破解S盒
        item = item.split("G")
        a = _ten_to_two(item[0])
        b = _ten_to_two(item[1])
        b = "P".join(b)
        b = b.split("P")
        b.pop(0)
        b_str = ""
        for b_ii in b:
            b_str += b_ii
        b = b_str
        a = "P".join(a)
        a = a.split("P")
        er_type = ["","","","",""]
        er_type[0] = a[0]
        er_type[1] = a[1]
        er_type[2] = b
        er_type[3] = a[2]
        er_type[4] = a[3]
        for er_y in er_type:
            k += er_y
        # 反向生成二层ascii
        k = _two_to_ten(k)
        k = "P".join(k)
        k = k.split("P")
        k.pop(0)
        k_str = ""
        for k_ii in k:
            k_str += k_ii
        k = k_str
        encode_getter += "K" + k + "|"
    encode_getter = _decrypt_string(encode_getter)
    return encode_getter


def qs_box_to_lock(message):
    mes = _encrypt_string(message)
    mes = _s_zip(mes)
    return mes


def qs_box_unlock(mes):
    b_i = _return_box_qs(mes)
    return b_i