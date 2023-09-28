from unittest.mock import Mock, patch

import bs4
import httpx
from fastapi.testclient import TestClient

from main import app, get_item, static_replace, text_editing

URL = 'https://news.ycombinator.com/'
client = TestClient(app)


async def test_connection() -> None:
    """Проверка соединения к серверу"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == 'Hacker™ News proxy ver 1.0'


async def test_get_item() -> None:
    """Проверка получения страницы по заданному ID"""
    id = 13713999
    r = await get_item(URL, id)
    assert r.status_code == 200


async def test_text_editing() -> None:
    """Проверка корректного добавления ™ в слова, где 6 букв"""
    text = "doesn't. He doesn't want nachos. they're they're. image), (image, \
        we're)) habbit))) they''re burito's"
    answer = await text_editing(text)
    correct = "doesn't™. He doesn't™ want nachos™. they're™ they're™. image), \
        (image, we're)) habbit™))) they''re burito's"
    assert answer == correct.split()


@patch('main.get_item')
@patch('main.static_replace')
async def test_response(mock_static: Mock, mock_item: Mock) -> None:
    """Проверка основной логики программы с поиском тегов и заменой текста"""
    with open('html_test/testing_html.html') as html_file:
        response = httpx.Response(status_code=200, text=html_file.read())
    mock_item.return_value = response
    r = client.get('/item?id=66666')
    assert r.status_code == 200
    with open('html_test/result_html.html') as result_file:
        assert r.text == result_file.read()


async def test_static_replace() -> None:
    """Проверка корректной замены ссылок в html"""
    url = 'www.testing_url.ai/'
    with open('html_test/testing_replace.html') as html_file:
        soup = bs4.BeautifulSoup(html_file, 'lxml')
    await static_replace(url, soup)
    with open('html_test/result_replace.html') as result_file:
        assert soup == bs4.BeautifulSoup(result_file.read(), 'lxml')
