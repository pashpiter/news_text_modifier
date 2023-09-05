from fastapi import FastAPI
import uvicorn
import httpx


app = FastAPI()


@app.get('/')
async def index() -> str:
    return "Parsing Server ver 1.0"


@app.get('/send')
async def testing_pars():
    async with httpx.AsyncClient() as client:
        url = 'https://www.google.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        r = await client.get(url, headers=headers)
        print(r.status_code)
        return r.text


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
