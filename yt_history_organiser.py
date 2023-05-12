import mysql.connector as mysql
import re
import sys
from getpass import getpass
import requests
import json as js
import time
from multiprocessing.pool import ThreadPool
import random

user_agents = js.load(open('user agents.json','r')) #json data of user agents to be used to request video category from youtube.

#Functions to parse through strings and extract date/time/title/category of video.
def ext(video_info, video_subinfo):
    if video_subinfo == 'date':
        return re.findall('(.*)T', video_info)[0]
    elif video_subinfo == 'time':
        return re.findall('T(.*)Z', video_info)[0]
    elif video_subinfo == 'title':
        return re.findall(' (.*)', video_info)[0]
    elif video_subinfo == 'channel':
        return video_info
    elif video_subinfo == 'category': #Find category of the video online
        while True: #loop till you get a response from youtube.
            try:
                r = requests.get(video_info,headers= {'User-Agent': random.choice(user_agents)['ua']}) #different user agents are used to prevent youtube from blocking.
                break
            except:
                pass

        try:
            return re.findall('"category":"(.+?)"',r.text)[0]
        except:  #In case video is removed by youtube
            return None

def data(video,video_info,video_subinfo): #look if the video data (from json file) contains specific contents (date,time,title,channel,etc)
    if video_info in video:
        return ext(video[video_info],video_subinfo)[:250] #Fetch first 250 characters
    else:
        return None
    

while True: #A loop to ask user for their mysql database, password and user.
    host = input('Enter the host name\n')
    user = getpass('Please enter MYSQL user\n')
    password = getpass('Please enter MYSQL password\n')
    try:
        db = mysql.connect(host=host, user= user, password= password)
        print('database successfully connected')
        cur = db.cursor()
        break
    except:
        print('database connection not successfull.')
        i = input('Do you want to try again? (Y/N)\n')
        if i == 'n':
            sys.exit('Thank you for using this program')

#Create databases and tables neccessary
cur.execute('''CREATE DATABASE IF NOT EXISTS
             yt_history''')
cur.execute('USE yt_history')
cur.execute('''CREATE TABLE IF NOT EXISTS video(
            sr_no INT(250) PRIMARY KEY, 
            title VARCHAR(250), 
            channel VARCHAR(250), 
            category varchar(250),
            time VARCHAR(250), 
            date VARCHAR(250))''')


#A loop to ask whether to create new history or extend a previously stored history.
while True:
    res = input('Select from the following tasks\n1. Store a new history\n2. Extend a previously stored history\n')
    if res.isdigit(): #To prevent further errors while typecasting response.
        if int(res) == 1:
            ask_str = 'Please write the file name that contains the history you want to store\n'
            new = True
            extend = False
            break
        elif int(res) == 2:
            ask_str = 'Please write the file name that contains the history you want to extend\n'
            extend = True
            new = False
            break
        else:
            print('Inavlid response.\nPlease try again')
    else:
            print('The given response is not a digit.\nPlease try again')

#A function to ask for file name that contains history.
def ask_file(ask_str):
    while True:
        try:
            fname = input(ask_str)
            f = open(fname, 'r', encoding='utf-8')
            print('File succesfully opened!')
            break
        except:
            print('The given file name is invalid.')
            initial_index = input('Do you want to try again? (Y/N)\n')
            if initial_index.lower == 'n':
                sys.exit('Thank you for using this program')
    return js.load(f)
    
f = ask_file(ask_str)

#A loop to check the video till where previous history was stored
if extend:

    cur.execute('SELECT * FROM VIDEO ORDER BY date desc, time desc LIMIT 1')
    first = cur.fetchone() #First entry of previous history

    if first:
        first_time = first[3]
        first_date = first[4]

        for last_index in range(len(f)): #A loop to match the first entry of previous history with our new history.
            video = f[last_index]
            if data(video, 'time', 'time') == first_time and data(video,'time','date') == first_date:
                print("The previous history's first entry was:\n", first)
                while True:
                    response = input('Do you want me to extend new history till the previous history?(Y/N)\n')
                    if response.lower() == 'y':
                        break
                    elif response.lower() == 'n':
                        last_index = len(f)
                        break
                    else:
                        print('Invalid response')
                break
            else:
                last_index+=1
    else: #This would be a new history and user has by mistake selected extend option.
        last_index= len(f)
else:
    last_index=len(f)

if new:
    #If program is run in pieces to mine video category (this feature is available only if a new history is stored), it will resume from last chunk mined.

    #Fetch the last row stored
    cur.execute('SELECT * FROM video ORDER BY date DESC,time DESC')
    rows = cur.fetchall()

    if rows:  #If a row was stored.
        last = rows[-1]
    else:
        last = None
else:
    last = None

if last:

    last_time = last[3]
    last_date = last[4]

    for initial_index in range(len(f)):
        video = f[initial_index]

        if data(video, 'time', 'time') == last_time and data(video,'time','date') == last_date: #If an entry in new history matches with lastest entry stored.
            print('The last entry was:\n', last)

            #A loop to ask user if he/she wants to organise from where she left.
            while True:
                response = input('Do you want me to organise history from where you left?(Y/N)\n')
                if response.lower() == 'y':
                    break
                elif response.lower() == 'n':
                    initial_index=-1
                    cur.execute('TRUNCATE TABLE video')
                    break
                else:
                    print('Invalid response')

            break

        else:
            initial_index+=1

else:
    initial_index=-1


#Loop through each video from history and store its data.
print('Starting to organise your history!')

def organise_video(video):  # function to loop through each video and parse date, time, title and channel of the video.
    time_data= data(video,'time','time')
    date= data(video,'time','date')
    title= data(video,'title','title')

    if 'subtitles' in video: #If no subtitles then it would be advertisement.
        channel= data(video['subtitles'][0],'name','channel')
    else:
        return None

    if 'titleUrl' in video:
        category = ext(video['titleUrl'],'category')
    else:
        category = None

    if category:
        category = category.replace('\\u0026','&')
    else: #This means either title url is not found or category was not extracted due to any reasons from ext function.
        return None
    
    return (title,channel,category,time_data,date)


# Use a threadpool to increase the speed of extracting category of video from web.

x=0
for index in range(initial_index+1,last_index,150): #Organise a chunk of 150 videos at a time.

    organised_video_chunk = []

    if not x: # loop is ran for the first time, so a threadpool should be created.
        pool = ThreadPool(10)

    if index+150<=last_index: # if there are less than 150 videos to organise.
        video_chunk = f[index:index+150]
    else:
        video_chunk = f[index:last_index]

    r = pool.map_async(organise_video,video_chunk) # run the threadpool.
    r.wait()

    organised_video_chunk = r.get()
    organised_video_chunk = [video for video in organised_video_chunk if video!= None] # removing empty elements from organised videos.

    sql_query = ('INSERT INTO video(title,channel,category,time,date) VALUES (%s,%s,%s,%s,%s)')
    cur.executemany(sql_query,organised_video_chunk)
    db.commit()

    cur.execute('SELECT COUNT(*) FROM video')
    total_rows = cur.fetchone()[0]

    print('Successfully uploaded',total_rows,"videos' history to database")
    
    x+=1
    if x%10 == 0: #Sleep for 2 sec after every 10 iterations to prevent overloading and crashing.
        time.sleep(2)

pool.close()

cur.execute('SELECT COUNT(*) FROM video')
total_rows = cur.fetchone()[0]
print('Successfully stored all the',total_rows,"videos' history.")

cur.close()
db.close()
