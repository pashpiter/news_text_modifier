from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
from bs4 import BeautifulSoup
import bs4

CHR = 10000
app = FastAPI()


@app.get('/')
async def index() -> str:
    return "Hacker™ News proxy ver 1.0"


@app.get('/item')
async def adding_tm():
    async with httpx.AsyncClient() as client:
        url = 'https://news.ycombinator.com/item?id=13713480'
        r = await client.get(url)
        soup = BeautifulSoup(r.text[:CHR], "lxml")
        print(soup.select("[data-testid=adResult]"))
        all_comm = soup.find_all('tr', 'athing comtr')  # Находим все комменты
        for comm in all_comm:
            text = comm.find('span', 'commtext c00')  # Находим текст в комменте
            if text:
                for content in text.contents:
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
        if len(st.contents) != 1:
            await text_extracting(st.contents[1])
        sen = await text_editing(text)
        text.replace_with(' '. join(sen))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
