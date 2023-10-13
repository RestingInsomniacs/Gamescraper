# CUBE CODERS GAME DESCRIPTION SCRAPER

The cube coders amp server has a list of games that it can host. However, that list doesn't include a lot of information about the game which makes discovery hard. GameScraper takes the list of games that the server supports and then pulls data from steam to make discovery easier. 

## Current state

It only scrapes the list of the generic modules and doesn't scrape the compatibility info and notes. It also doesn't automatically search for the pages of Steam pages, it simply lists them out. It's also not compiled and is just in script-form, so to open it, you need to download the Requests library and Python.

## Plans for the future. 

1. Play with current implementation
2. Create an API that returns returns the data
3. Create a UI that displays the data. 
4. Extend it where it makes sense. 