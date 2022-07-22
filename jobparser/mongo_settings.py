"""
Параметры соединения с MongoDB.
"""

from pymongo import MongoClient


HOST = '192.168.2.230'  # IP-адрес
PORT = 27017  # порт

# для подключения к MongoDB
# создаем объект класса MongoClient
client = MongoClient(HOST, PORT)
# указатель на базу данных:
db = client['vacancies_db']
# коллекции:
vacancies = db['vacancies']  # вакансии
