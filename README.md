# news_text_modifier

##### Стек: Python, FastAPI, Beautifulsoup, httpx, pytest
***

### Что умеет news_text_modifier
Приложение котрое показывает содержимое страниц Hacker News, изменяя текст на страницах по следующему правилу: после каждого слова из шести букв стоит значок «™».

Доступ осуществляется по адресу: http://127.0.0.1:8000/item?id={int}, где id - id статьи с сайта https://news.ycombinator.com/

Пример: 
* https://news.ycombinator.com/item?id=13719368
* http://127.0.0.1:8000/item?id=13719368

***
### Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone git@github.com:pashpiter/news_text_modifier.git
```
* Перейти в папку news_text_modifier
* Создать виртуальное окружение
```
python3 -m venv venv
```
* Активировать виртуальное окружение

на macOS и Ubuntu
```
source venv/bin/activate
```
на Windows
```
source venv/Scripts/activate.bat
```
* Установить зависимости
```
pip install -r requirements.txt
```
* Запустить проект
```
python main.py
```
***
Проект покрыт тестами, команда для запуска тестов:
```
pytest
```