from typing import Union

from fastapi import FastAPI
import amp_scraper

app = FastAPI()


@app.get("/games")
def read_root():
    return {"games": amp_scraper.list_games()}
