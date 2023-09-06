from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import httpx
from bs4 import BeautifulSoup


app = FastAPI()


@app.get('/')
async def index() -> str:
    return "Hacker™ News proxy ver 1.0"


@app.get('/send')
async def adding_tm():
    async with httpx.AsyncClient() as client:
        url = 'https://news.ycombinator.com/item?id=13713480'
        r = await client.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        all_comm = soup.find_all('tr', 'athing comtr')
        for comm in all_comm:
            c = comm.find('span', 'commtext c00')
            if c:
                t = [text for text in c.stripped_strings]
                # t = c.get_text(strip=True)
                print(*t, end='\n----------------------------------------\n')
        return HTMLResponse(r.text, status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
