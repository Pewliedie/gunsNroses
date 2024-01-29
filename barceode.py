import qrcode
import datetime
import random
import pyautogui


# Получение текущей даты и времени
current_datetime = datetime.datetime.now()
# Генерация случайного числа из секунд
random_number = random.randint(0, 59)
# Получение текущих координат мыши
mouse_position = pyautogui.position()

# Создание строки, объединяющей дату, случайное число и координаты мыши
data_string = f"{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}+{random_number}"
data_string = ''.join(c for c in data_string if c.isdigit())
# Создание QR-кода из строки данных
data = data_string
print(data)
