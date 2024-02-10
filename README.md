# Proof Vault

Требования:
- Python 3

Основной стек:
- PyQt6 - GUI
- SQLite3 - БД
- SQLAlchemy - ORM
- pydantic - Валидация

Пакеты и зависимости:
- PyAutoGUI
- qrcode
- Pillow
- python-ecspos
- black
- pylint

## Установка и запуск
```
1. Скачать код
git clone https://github.com/5kif4a/proof-vault.git
2. Перейди в директорию с кодом
cd proof-vault
3. Создать виртуальное окружение
py -m venv venv
4. Активировать виртуальное окружение
.\venv\Scripts\activate
5. Скачать требуемые пакеты и зависимости для проекта
pip install -r requirements.txt
6. Запустить код
python main.py
```
## Как собирать в .exe
```
python build.py
```
## Форматирование кода и линтер
```
python format_and_lint.py
```