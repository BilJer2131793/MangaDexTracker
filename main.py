import json
import os
import keyboard
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

#checks if data files exist and makes them if they dont
def CheckData():
    # creates data file if it doesnt exist
    if not os.path.exists("ChapterData.json"):
        with open("ChapterData.json", 'w') as json_file:
            json.dump({}, json_file)
        print("Default file created")
    # created user file if it doesnt exist
    if not os.path.exists("UserData.json"):
        user = ["", "en"]
        with open("UserData.json", 'w') as json_file:
            json.dump(user, json_file)
        print("User file created")
    return None
def ChangeEmail():
    email = input("Please enter your email : ")
    with open("UserData.json", 'r') as json_file:
        data = json.load(json_file)
        data[0] = email
    with open("UserData.json", "w") as json_file:
        json.dump(data, json_file)
    return email
def ChangeLanguage():
    print("You must enter the shortened version ex: english is en")
    language = input("Please enter the language you want : ").upper()
    with open("UserData.json", 'w') as json_file:
        data = json.load(json_file)
        data[1] = language
        json.dump(data, json_file)
    return language
def AddManga():
    base_url = "https://api.mangadex.org"

    print("Copy paste the big title when on the page")
    title = input("Title : ")

    r = requests.get(
        f"{base_url}/manga",
        params={"title": title}
    )
    if r.json()["total"] == 0:
        print("The title you entered was wrong")
        return None

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
#main process
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
            print(" ")
            Loading(3600)
    except:
        Loading(1800)
        Run()
    return None
def Loading(time):
	sleepTime = 1
	maxSleep = time
	while(sleepTime < maxSleep):
		LoadingBar(sleepTime, maxSleep)
		sleepTime = sleepTime + 1	
	
	return None
def LoadingBar(i, maximum):
    length = 64
    blackBox = "■"
    whiteBox = "□"
    
    pourcentage = int(i/maximum*100)
    pourcentageFini = int(length*pourcentage/100)
    print((blackBox*pourcentageFini)+((length-pourcentageFini)*whiteBox),end="\r")
    time.sleep(1)
    
    return None
def CompareData(oldData, newData):
    for i, data in enumerate(oldData):
        if tuple(data) != newData[i]:
            NewChapter(newData[i])
    return None
#notifies user when there is a new chapter
#If you're reading this you have access to the hotmail account
#Have fun?
#if you want to change it the easiest way is to make a new microsoft account since I encountered lots of problems with a gmail account
def NewChapter(data):
    with open("UserData.json","r") as json_file:
        user = json.load(json_file)
    email = user[0]
    print("Chapter "+data[2]+" of "+data[0]+" has been released!")
    sender_email = "MangaDexTracker@hotmail.com"
    sender_password = "verySecurePassWord"
    recipient_email = email

    subject = "Chapter "+data[2]+" of "+data[0]+" has been released!"
    body = MIMEText('<h1><a href="https://mangadex.org/title/'+data[1]+'">Chapter '+data[2]+' of '+data[0]+' has been released!</h1>','html')
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(body)

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, message.as_string())
    return None
#if the program crashes while running, sends email
def SendErrorEmail():
    sender_email = "MangaDexTracker@hotmail.com"
    sender_password = "verySecurePassWord"

    recipient_email = email

    subject = "Program crashed"
    body = "The program had an error and was closed"
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
    print("Tracked Titles: ")
    with open("ChapterData.json", 'r') as json_file:
        data = json.load(json_file)
    for chapter in data:
        print(chapter[0])

    return None


# ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※ ※　※　※　※　※　※


baseUrl = "https://api.mangadex.org/manga/"

CheckData()
with open("UserData.json","r") as json_file:
    user = json.load(json_file)
email = user[0]
language = user[1]
print("Current email : "+email)
print("Current language : "+language)
while(True):
    print("Add Titles          (A)")
    print("Change Email        (E)")
    print("Change Language     (L)")
    print("Run Program         (R)")
    print("Show Tracked Titles (S)")
    print("Exit                (X)")
    choice = input("Choice: ")
    if choice.upper() == "A":
        AddManga()
    elif choice.upper() == "E":
        email = ChangeEmail()
    elif choice.upper() == "L":
        language = ChangeLanguage()
    elif choice.upper() == "S":
        ShowTracked()
    elif choice.upper() == "R":
        Run()
    elif choice.upper() == "X":
        exit()
    print("\n")






