import json
import os
import keyboard
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

def LoadData():
    with open("ChapterData.json", 'r') as json_file:
        data = json.load(json_file)

    return data

def AddManga(title):
    base_url = "https://api.mangadex.org"
    r = requests.get(
        f"{base_url}/manga",
        params={"title": title}
    )
    id = [manga["id"] for manga in r.json()["data"]]
    chapter = GetRecentChapter(title, id[0])
    with open("ChapterData.json", 'r') as json_file:
        data = json.load(json_file)
    if not isinstance(data, list):
        data = []
    data.append(chapter)
    print(title + " has been added")
    with open("ChapterData.json", 'w') as json_file:
        json.dump(data, json_file, indent=2)

    return None

def get_chapter(chapter):
    if chapter[2] is None:
        return float(0)
    return float(chapter[2])

def GetRecentChapter(title, id):
#    r = requests.get(baseUrl +id+"/feed",
#                     params={"translatedLanguage[]": language}, )
    r = requests.get(baseUrl +id+"/feed?order[readableAt]=desc&offset=0&translatedLanguage[]="+language)
    chapterList = [(title, id, chapter["attributes"]["chapter"], chapter["attributes"]["title"],
                    chapter["attributes"]["readableAt"], chapter["attributes"]["translatedLanguage"]) for chapter in
                   r.json()["data"]]
    recentChapter = max(chapterList, key=get_chapter)
    print(recentChapter)
    return recentChapter

def SaveData(newData):
    filePath = "ChapterData.json"
    with open(filePath, 'w') as json_file:
        json.dump(newData, json_file, indent=2)
    return None

def Run():
    print("Started")
    try:
        count = 0
        while True:
            with open("ChapterData.json", 'r') as json_file:
                oldData = json.load(json_file)
            chapterInfo = [(entry[0], entry[1]) for entry in oldData]

            newData = []
            for info in chapterInfo:
                newData.append(GetRecentChapter(info[0], info[1]))
            CompareData(oldData,newData)
            SaveData(newData)
            count = count + 1
            print("cycle "+str(count)+" done")
            time.sleep(3600)
    except:
        SendErrorEmail()
    return None

def CompareData(oldData, newData):

    for i, data in enumerate(oldData):
        if tuple(data) != newData[i]:
            NewChapter(newData[i])
    return None

def NewChapter(data):
    print("Chapter "+data[2]+" of "+data[0]+" has been released!")
    sender_email = "jeromeTesting@hotmail.com"
    sender_password = "testing554"

    recipient_email = "jerome.bilodeau418@gmail.com"

    subject = "Chapter "+data[2]+" of "+data[0]+" has been released!"
    body = "https://mangadex.org/title/"+data[1]
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, message.as_string())
    return None

def SendErrorEmail():
    sender_email = "jeromeTesting@hotmail.com"
    sender_password = "testing554"

    recipient_email = "jerome.bilodeau418@gmail.com"

    subject = "Program crashed"
    body = "it is dead"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, message.as_string())
def ShowTracked():
    with open("ChapterData.json", 'r') as json_file:
        data = json.load(json_file)
    print(data)

    return None

# ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※


baseUrl = "https://api.mangadex.org/manga/"
language = "en"

if not os.path.exists("ChapterData.json"):
    with open("ChapterData.json", 'w') as json_file:
        json.dump({}, json_file)
    print("Default file created")
while(True):
    choice = input("Choice: ")
    if choice.upper() == "A":
        AddManga("School Zone")
    elif choice.upper() == "S":
        ShowTracked()
    elif choice.upper() == "R":
        Run()
    elif choice.upper() == "E":
        exit()






