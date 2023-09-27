import string
from typing import Union

import bs4
import httpx
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

LOCALHOST = 'http://127.0.0.1:8000/'

app = FastAPI()


@app.get('/')
async def index() -> Response:
    return Response('Hacker™ News proxy ver 1.0')


async def get_item(url: str, id: int):
    async with httpx.AsyncClient() as client:
        item = f'item?id={id}'
        r = await client.get(url+item)
        return r


@app.get('/item')
async def get_handler(id: int) -> HTMLResponse:
    url = 'https://news.ycombinator.com/'
    r = await get_item(url, id)
    soup = BeautifulSoup(r.text, "lxml")
    await static_replace(url, soup)
    all_comm = soup.find_all('tr', 'athing comtr')  # Находим все комменты
    for comm in all_comm:
        comm_text = comm.find('span', 'commtext c00')  # Текст в комменте
        if comm_text:
            for content in comm_text.contents:
                await text_extracting(content)
    return HTMLResponse(soup, status_code=200)


async def text_editing(text: str) -> list[str]:
    r = []
    for word in text.split():
        w = word.translate(str.maketrans(
            '', '', string.punctuation[:6]+string.punctuation[7:]
        ))
        if word.isalpha() and len(w) == 6:
            r.append(word+'™')
        elif not word.isalpha() and (len(w) == 7 or len(w) == 6):
            new_word = []
            for letter in word[::-1]:
                if letter.isalpha() and '™' not in new_word:
                    new_word.append('™')
                    new_word.append(letter)
                else:
                    new_word.append(letter)
            r.append(''.join(new_word[::-1]))
        else:
            r.append(word)
    return r


async def text_extracting(
        content: Union[bs4.element.NavigableString, bs4.Tag]
) -> None:
    if type(content) == bs4.element.NavigableString:
        sen = await text_editing(content)
        content.replace_with(' '. join(sen) + ' ')
    elif content.name == 'pre':
        pass
    else:
        text = content.string
        if len(content.contents) > 1:
            for i in content.contents[1:]:
                await text_extracting(i)
        if text:
            sen = await text_editing(text)
            text.replace_with(' '. join(sen) + '')


async def static_replace(url: str, soup: BeautifulSoup) -> None:
    links = soup.find_all('link')
    for link in links:
        link['href'] = url + link.get('href')

    links_a = soup.find_all('a')
    for link_a in links_a:
        if url in link_a['href']:
            link_a['href'] = LOCALHOST + link_a.get('href').rpartition('/')[-1]

    scrtipt = soup.find('script')
    scrtipt['src'] = url + scrtipt.get('src')
    img_link = soup.find('tr').find('img')
    img_link['src'] = url + img_link.get('src')


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
