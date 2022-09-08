from django.utils import timezone
from . import jalali
import os, re
import datetime
from random import randint, choice


def is_email(email):
    return bool(re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)').match(str(email)))

def is_phone(phone):
    return bool(re.compile(r'0?9([0-1][0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}').match(str(phone)))

def is_national_code(value):
    return bool(re.compile(r'(^[0-9]{10}$)').match(str(value)))

def is_shaba(value):
    return bool(re.compile(r'(^(?:IR)(?=.{24}$)[0-9]*$)').match(str(value)))


def write_action(action):
    """ 
        this function write user actions in actions.log file in root directory 
    """
    with open('actions.log', 'a') as file:
        file.write(f'Date: {datetime.datetime.now()} .:. Action: {action}')
        file.write('\n')


def jalali_convertor(time, output='date_time', number=False):
    jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    time = timezone.localtime(time)

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    if number == True:
        time_to_list_num = list(time_to_tuple)
        for index, month in enumerate(intmonth):
            if time_to_list_num[1] == index + 1:
                time_to_list_num[1] = month
                break

    if output == 'date_time':        # ۲۱ دی ۱۴۰۰, ساعت ۲۱:۲۸
        output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت {time.hour}:{time.minute}'
        return persian_numbers(output)
    elif output == 'j_date':         # ۲۱ دی ۱۴۰۰
        output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}'
        return persian_numbers(output)
    elif output == 'date' and number == True:           # ۲۱ - ۱۰ - ۱۴۰۰
        output = f'{time_to_list_num[2]} - {time_to_list_num[1]} - {time_to_list_num[0]}'
        return persian_numbers(output)
    elif output == 'j_month':        # دی 
        return persian_numbers(time_to_list[1])
    else:
        return 'No OutPut!'


def persian_numbers(myStr):
    numbers = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    for e, p in numbers.items():
        myStr = myStr.replace(e,p)
    return myStr

def get_ext_file(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.png', '.jpg', 'jpeg']
    for i in extesion_allowed:
        if extesion == i:
            return 'yes'
    return 'no'


# =============== start static path

# before function File storage
def get_filename_ext_rand(filepath):
    time = datetime.datetime.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random = randint(100, 999)
    output = f'{time_to_list[2]}{time_to_list[1]}{time_to_list[0]}{random}'
    return ext.lower(), output


# ######### for users imgs ######### #
def user_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"users/{final_name}"


# ######### for users imgs ######### #
def file_chat_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"file-chats/{final_name}"


# ######### for doctors degrees ######### #
def doctor_degree_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"degrees/{final_name}"


# ######### for ticket images ######### #
def ticket_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"tickets/{final_name}"


# ######### for blogs imgs ######### #
def blog_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"blogs/{final_name}"

# =============== end static path


# ######### get user code ######### #
def get_user_code():
    time = datetime.datetime.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    random = randint(1000, 9999)
    year = time_to_list[0]
    month = time_to_list[1]
    day = time_to_list[2]
    if month < 10:
        month = f'0{month}'
    if day < 10:
        day = f'0{day}'
    output = f'1{str(year)[-2:]}{month}{day}{random}'
    return output
    # 10012017817 => 1 => user  // 00 => 1400 // 12 => month // 01 => day // 7898 => random


def get_blog_code():
    time = datetime.datetime.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    random = randint(1000, 9999)
    year = time_to_list[0]
    month = time_to_list[1]
    day = time_to_list[2]
    if month < 10:
        month = f'0{month}'
    if day < 10:
        day = f'0{day}'
    output = f'2{str(year)[-2:]}{month}{day}{random}'
    return output
    # 20012017817 => 2 => blog  // 00 => 1400 // 12 => month // 01 => day // 7898 => random


def get_links_code():
    char_list = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]
    code = ''
    for _ in range(1, 20):
        code += choice(char_list)
    return code


def get_random_code():
    return randint(10000, 99999)

