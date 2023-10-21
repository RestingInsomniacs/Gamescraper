
import requests
import json
import amp_scraper

# Scans and Returns Array of Key Locations
def scan_key_loc(text: str, key: str, array_size: int):
    key_arr = [0 for size in range(0, array_size)]
    key_location = 0
    for key_index in range(0, array_size):
        key_arr[key_index] = text.find(key, key_location)
        key_location = key_arr[key_index] + 1

    return key_arr

# Scans String from Substring Index Up to Key Identifier and Returns Location
def scan_string(text: str, starting_point: int, key: str, trim: bool):
    offset = 0
    if not trim:
        offset = len(key)
    url_end = text.find(key, starting_point)
    return url_end + offset


# Scans String in Reverse from Substring Index Up to Key Identifier and Returns Location
def rscan_string(text: str, starting_point: int, key: str, trim: bool):
    r_scan_point = starting_point
    offset = 0
    if trim:
        offset = len(key)
    for r_scan in range(0, starting_point):
        if text[r_scan_point:r_scan_point+len(key)] != key:
            # print(text[r_scan_point:r_scan_point + len(key)])
            r_scan_point -= 1
        else:
            # print(text[r_scan_point:r_scan_point+len(key)])
            return r_scan_point + offset
            break


# Starts from Central Key Identifier and Scans for Start and End Identifiers of String and Returns Resulting Substring
def grab_string(text: str, starting_point: int, start_key: str, end_key: str, trim: bool):
    beginning = rscan_string(pageStr, starting_point, start_key, trim)
    end = scan_string(pageStr, starting_point, end_key, trim)
    return text[beginning:end]



inputText = input("Press Enter to Start Application:")

# Handles User Input For Help, Listing, and Output Commands
while inputText != "Exit" and inputText != "exit":
    print("\r")
    print("Type \"Help\" for list of commands")
    inputText = input("Input:")

    if inputText == "Help" or inputText == "help":
        print("List Games: Outputs a list of games with generic compatibility\nOutput [url]: Outputs a JSON with title, description, images. and videos of a listed Steam page in the local directory \n(non-steam urls may cause unexpected behavior or not function at all)\nExit: Closes application")
        inputText = ""

    elif inputText == "List Games" or inputText == "list games":
        print("Games:")
        amp_scraper.list_games()
        inputText = ""

    elif inputText == "Exit" or inputText == "exit":
        exit()

    elif inputText[0:6] == "Output" or inputText[0:6] == "output":
        url = inputText[7: len(inputText)]
        response = requests.get(url)
        pageStr = response.text

        # Title Key Identification
        titleStartID = "<title>"
        titleEndID = " on Steam</title>"

        # Description Key Identification
        descrStartID = "Description\" content=\""
        descrEndID = "\">"

        # Max Quality Image Key Identification
        hdImageID = "1080"
        hdImagesCount = 0
        hdImgStartID = "=\""
        hdImgEndID = "\" target="

        # Max Quality Video Key Identification
        hdVideoID = "movie_max.mp4?t"
        hdVideoCount = 0
        hdVideoStartID = "data-mp4-hd-source=\""
        hdVideoEndID = "\""

        # Scans for Media(Videos and Images)
        for i in range(0, len(pageStr)):

            if pageStr[i:i + len(hdImageID)] == hdImageID:
                hdImagesCount += 1
            if pageStr[i:i + len(hdVideoID)] == hdVideoID:
                hdVideoCount += 1

        # Initializes Arrays Based on the Number of Media Found
        hdImgLocations = [[0] for x in range(hdImagesCount)]
        hdImages = ["" for x in range(hdImagesCount)]
        hdVidLocations = [[0] for x in range(hdVideoCount)]
        hdVideos = ["" for x in range(hdVideoCount)]

        # Scans for Key IDs for Videos and Images and Returns Their Locations in Page String
        hdImgLocations = scan_key_loc(pageStr, hdImageID, hdImagesCount)
        hdVidLocations = scan_key_loc(pageStr, hdVideoID, hdVideoCount)

        # Scans Data from Steam Page to Apply to JSON File
        title = grab_string(pageStr, pageStr.find(titleStartID) + len(titleStartID), titleStartID, titleEndID, True)

        description = grab_string(pageStr, pageStr.find(descrStartID) + len(descrStartID), descrStartID, descrEndID, True)

        for imageScan in range(0, hdImagesCount):
            hdImages[imageScan] = grab_string(pageStr, hdImgLocations[imageScan], hdImgStartID, hdImgEndID, True)

        for videoScan in range(0, hdVideoCount):
            hdVideos[videoScan] = grab_string(pageStr, hdVidLocations[videoScan], hdVideoStartID, hdVideoEndID, True)


        # Formats Data to JSON
        outputFile = {
            "title": title,
            "description": description,
            "video_urls": hdVideos,
            "image_urls": hdImages
        }
        
        # Dumps and Writes JSON File To Local Directory Using Game's Title
        json_object = json.dumps(outputFile, indent=4)

        jsonName = title.replace(" ", "") + ".json"
        with open(jsonName, "w") as outfile:
            outfile.write(json_object)

        print("JSON", jsonName, "created in Local Directory")
        inputText = ""

    else:
        print("Command Not Recognized")
