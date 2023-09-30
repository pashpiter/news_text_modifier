# news_text_modifier

##### Стек: Python, FastAPI, Beautifulsoup, httpx, pytest
***

### Что умеет news_text_modifier
Приложение котрое показывает содержимое страниц Hacker News, изменяя текст на страницах по следующему правилу: после каждого слова из шести букв стоит значок «™».

Доступ осуществляется по адресу: http://127.0.0.1/item?id={int}, где id - id статьи с сайта https://news.ycombinator.com/

Пример можно найти в конце файла

***
### Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone git@github.com:pashpiter/news_text_modifier.git
```
* Перейти в папку news_text_modifier

* Запустить проект используя docker-compose
```
docker-compose up -d
```
***
Проект покрыт тестами, которые выполняются при создании контейнера

***
Примеры запросов:
```
http://127.0.0.1/
```
```
http://127.0.0.1/item?id=13719368
```
