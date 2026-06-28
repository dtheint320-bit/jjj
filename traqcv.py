from googletrans import Translator
import streamlit as dc
import json
import os
import sqlite3
import hashlib
import pytesseract as cd
from PIL import Image
from groq import Groq

def ck():
    df = sqlite3.connect("ju.db")
    we = df.cursor()
    we.execute(('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT)'''))
    df.commit()
    df.close()


try:
    def pc(username, password):
        df = sqlite3.connect("ju.db")
        we = df.cursor()
        ex = hashlib.sha256(password.encode()).hexdigest()
        we.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, ex))
        m = we.fetchone()
        if m:
            return True
        else:
            return False


except Exception as v:
    dc.write(f"errors {v}")

ck()



ec = dc.sidebar.selectbox(label= "=", options= ["Home", "Bugs", "History"])

Fi = "your.json"

def of():
    if os.path.exists(Fi):
        with open(Fi, "r", encoding= "utf-8") as c:
            return json.load(c)
    return []
  
def ld(his):
    with open(Fi, "w", encoding= "utf-8") as k:
        json.dump(his, k, ensure_ascii= False, indent= 2)

if "his" not in dc.session_state:
    dc.session_state.his = of()

if ec == "Home":
    dc.set_page_config("Hello my name is Devloper Kevin")
    dc.write("Developed by")
    dc.image("naq.jpg", caption= "@kevingman3")
    dc.page_link("https://www.tiktok.com/@kevingman3", label= "Here my tiktok Link")
    Tra = Translator()

    if "chat" not in dc.session_state:
        dc.session_state.chat = ""

    chat = dc.text_area("Enter", value= dc.session_state.chat)
    dc.write("choose your language to translate")

    c = dc.file_uploader("choose yor image to text", type= ["jpg", "jfif", "png", "jpeg"]
                         )

    if dc.button("Image to text"):
        if c is not None:
            cd.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            img = Image.open(c)
            fr = cd.image_to_string(img)
            dc.session_state.chat = fr
            dc.rerun()

    v = dc.file_uploader(label= "Voice file to text", type= ["m4a", "flac", "mp3", "mp4", "wav"])

    try:
        if dc.button("Speech into text"):
            if v is not None:
                md = Groq(api_key= "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")
                sc = md.audio.transcriptions.create(model= "whisper-large-v3", file= (v.name, v.read()), response_format= "text")
                dc.session_state.chat = sc
                dc.rerun()

    except Exception as d:
        dc.write(f"errors{d}")

    except Exception as c:
        print(f"Errors {c}")

    cd = {
    "myanmar": "my",
    "english": "en",
    "french": "fr",
    "Russian": "ru",
    "Indonesia": "id",
    "Arabic": "ar",
    "Ukrainian": "uk",
    "German": "de",
    "Turkey": "tr",
    "Polish": "pl",
    "Romanian": "ro",
    "Latin": "la"
}

    mc = dc.selectbox("select your language", list(cd.keys()))
    bu = dc.button("translate")

    if bu:
        if chat.lower == "":
            dc.write("error pls type your text")
        else:
            cs = Tra.translate(chat, dest= cd[mc])
            mca = dc.text_area(label= "success", value= cs.text)
            dc.session_state.his.append({"Type": chat,
                                         "Result": cs.text,
                                         "Dig L": mc})
            ld(dc.session_state.his)
        try:
            if dc.session_state.chat.lower == None:
                dc.success("Error! To download the Text file, "
            "You must atleast translate the result")
            else:
                dc.download_button(label= "Download Your Translated Text", 
                           data= cs.text,
                           file_name= "TrText.txt")
        except Exception as w:
            dc.success(f"Errors {w}")

if ec == "History":
    if len(dc.session_state.his) == 0:
        dc.write("no ones appear")
    else:
        for mc in dc.session_state.his[::-1]:
            dc.write(f"++Type surface++ {mc['Type']}")
            dc.write(f"++Resulte--++ {mc['Result']}")
            dc.write(f"Languages {mc['Dig L']}")
            dc.divider()


if ec == "Bugs":
    dc.header("There some bugs are")
    ac = '''Report a Bug

Help Us Improve

Found a bug or unexpected issue? We appreciate
 your feedback. Please provide as much detail 
 as possible, including the steps to reproduce
   the issue, screenshots (if available),
     and information about your device or browser.

Your reports help us improve the quality, performance,
 and user experience of our platform.

What to Include:

Description of the issue
Steps to reproduce
Expected behavior
Actual behavior
Browser and device information
Screenshots or screen recordings (optional)

Response Time
Our team reviews all bug reports and will investigate the issue as quickly as possible.

Thank you for helping us make our platform better.'''

    dc.markdown(ac)

