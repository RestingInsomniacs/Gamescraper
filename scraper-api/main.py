from typing import Union

from fastapi import FastAPI
import amp_scraper

app = FastAPI()


@app.get("/servers/amp")
def scrape_amp():
    return {"games": amp_scraper.list_games()}

@app.get("/games/{name}")
def get_game_description(name):
    return {
        "name": name,
        "description": f"the description of {name}",
        "images": ["https://media.giphy.com/media/nw01v68VBElqkxppKa/giphy.gif"],
        "videos": ["https://www.youtube.com/watch?v=ESOjt2_yJrU"]
    }