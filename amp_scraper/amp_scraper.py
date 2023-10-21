
import requests
import json

# Scraped CubeCoders for Generically Supported Module Applications
# (OS Compatibility and Special Case/SRCDS Table Scraping Not Yet Implemented)
def list_games():
    r = requests.get('https://discourse.cubecoders.com/t/supported-applications-compatibility/1828')
    listpage = r.text
    table_start_id = "<th style=\"text-align:left\">Application</th>\n<th style=\"text-align:left\">Windows</th>\n<th style=\"text-align:left\">Linux</th>\n<th style=\"text-align:left\">Notes</th>"
    table_end_id = "</div>"
    app_start_id = "<tr>\n<td style=\"text-align:left\">"
    app_end_id = "</td>"
    for i in range(0, len(listpage)):
        if listpage[i:i + len(table_start_id)] == table_start_id:
            table = listpage[i:listpage[i:len(listpage)].find(table_end_id)]
            for x in range(0, len(table)):
                if table[x:x + len(app_start_id)] == app_start_id:
                    print(table[x + len(app_start_id):table.find(app_end_id, x)])