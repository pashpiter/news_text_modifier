from main import text_editing, app, get_item
from fastapi.testclient import TestClient
import httpx
from unittest.mock import Mock, patch
import main
import bs4

URL = 'https://news.ycombinator.com/'
client = TestClient(app)


async def test_connection():
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == 'Hacker™ News proxy ver 1.0'


async def test_get_item():
    id = 13713480
    r = await get_item(URL, id)
    assert r.status_code == 200


async def test_text_editing():
    text = "doesn't. He doesn't want nachos. they're they're. image), (image, \
        we're)) habbit))) they''re burito's"
    answer = await text_editing(text)
    correct = "doesn't™. He doesn't™ want nachos™. they're™ they're™. image), \
        (image, we're)) habbit™))) they''re burito's"
    assert answer == correct.split()


@patch('main.get_item')
@patch('main.static_replace')
async def test_response(mock_static: Mock, mock_item: Mock) -> None:
    with open('html_test/testing_html.html') as html_file:
        response = httpx.Response(status_code=200, text=html_file.read())
    mock_item.return_value = response
    r = client.get('/item?id=66666')
    with open('html_test/result_html.html') as result_file:
        assert r.text == result_file.read()
