# Сбор данных из сети Интернет

## Сбор данных об открытых вакансиях "python"


---
### Для работы необходимо:

1. Установить scrapy и pymongo
```commandline
pip install scrapy
pip install pymongo
```
или
```commandline
pip install -r requirements.txt
# или
python -m pip install -r requirements.txt
```
2. Запустить контейнер с MongoDB:
```python
docker run -d --name mongo_scrap -p 27017:27017 -v mongodb_scrap:/data/db mongo
```
В файле mongo_settings.py необходимо указать IP-адрес и порт сервера MongoDB:
```python
python HOST = '192.168.2.230' # укажите IP-адрес
PORT = 27017 # укажиите порт (27017 стандартный порт MongoDB)
```
Так же можно указать базу данных (jobs_db):
```python
db = client['vacancies_db']
```
и коллекцию:
```python
vacancies = db['vacancies']  # вакансии
```
3. запустите runner.py
