from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
from bs4 import BeautifulSoup
import bs4

CHR = 10000
LOCALHOST = 'http://127.0.0.1:8000/'

app = FastAPI()


@app.get('/')
async def index() -> str:
    return "Hacker™ News proxy ver 1.0"


@app.get('/item')
async def adding_tm(id: int) -> HTMLResponse:
    async with httpx.AsyncClient() as client:
        url = 'https://news.ycombinator.com/'
        item = f'item?id={id}'
        r = await client.get(url+item)
        soup = BeautifulSoup(r.text, "lxml")
        await static_replace(url, soup)
        all_comm = soup.find_all('tr', 'athing comtr')  # Находим все комменты
        for comm in all_comm:
            comm_text = comm.find('span', 'commtext c00')  # Находим текст в комменте
            if comm_text:
                for content in comm_text.contents:
                    await text_extracting(content)
        return HTMLResponse(soup, status_code=200)


async def text_editing(text):
    r = []
    for word in text.split():
        if word.isalpha() and len(word) == 6:
            r.append(word+'™')
        elif not word.isalpha() and len(word) == 7:
            r.append(word[:-1]+'™'+word[-1])
        else:
            r.append(word)
    return r


async def text_extracting(st):
    if type(st) == bs4.element.NavigableString:
        sen = await text_editing(st)
        st.replace_with(' '. join(sen))
    else:
        text = st.find(text=True)
        if len(st.contents) > 1:
            await text_extracting(st.contents[1])
        if text:
            sen = await text_editing(text)
            text.replace_with(' '. join(sen))


async def static_replace(url: str, soup: BeautifulSoup):
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
