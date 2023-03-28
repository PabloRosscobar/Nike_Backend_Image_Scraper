import json
import platform
import sys
import time
import os
from random import randrange
from datetime import datetime
import time
from threading import Lock
from colorama import Fore, init
import sys
import Scraper
import PySimpleGUI as sg
from PIL import Image, ImageTk


end='\n'
init(autoreset=True)
machineOS = platform.system()
lock = Lock()
machineOS = platform.system()

now = str(datetime.now())[:-3]


def getImagesList():
    if machineOS == "Darwin":
        path = os.path.dirname(__file__).rsplit('/', 1)[0]
        x = os.path.join(os.path.dirname(sys.argv[0]), f"IMAGES/")
    elif machineOS == "Windows":
        path = os.path.dirname(__file__).rsplit('\\', 1)[0]
        x = os.path.join(os.path.dirname(sys.argv[0]), f"IMAGES\\")
    
    fileNames = os.listdir(x)
    
 
    return fileNames, x

def listFiles(window):
    if machineOS == "Darwin":
        path = os.path.dirname(__file__).rsplit('/', 1)[0]
        x = os.path.join(os.path.dirname(sys.argv[0]), f"IMAGES/")
    elif machineOS == "Windows":
        path = os.path.dirname(__file__).rsplit('\\', 1)[0]
        x = os.path.join(os.path.dirname(sys.argv[0]), f"IMAGES\\")
    
    file_list = os.listdir(x)
    
    for f in file_list:
        if "jpeg" not in f:
            print(f)
            file_list.remove(f)
    
    window["-FILE LIST-"].update(file_list)

    return file_list, x

def main():

    file_list_column = [
    [
            sg.Text("SCRAPE SKU:"),
            sg.In(size=(25, 1,), key="-SKU-"),
            sg.Button('Scrape', enable_events=True, key="-SCRAPE BUTTON-"),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]


    image_viewer_column = [
        [sg.Text("Choose an image from list on left:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column),
        ]
    ]

    window = sg.Window("NIKE IMAGE SCRAPER", layout, finalize=True)
    
    file_list, fileFolder = listFiles(window)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-SCRAPE BUTTON-":
            chosenSKU = values["-SKU-"]
            Scraper.Scraper(chosenSKU, window)
            file_list, fileFolder = listFiles(window)
            
            
            
        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            im = Image.open(f'{fileFolder}{values["-FILE LIST-"][0]}')
            im = im.resize(size=(300,300), resample=Image.BICUBIC)
            image = ImageTk.PhotoImage(image=im)
            try:
                window["-TOUT-"].update(values["-FILE LIST-"][0])
                window["-IMAGE-"].update(data=image)

            except:
                pass

    window.close()

main()
