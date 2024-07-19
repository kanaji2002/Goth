from title_get import extract_title
import datetime


url_list = []
time_list = []
title_list = {} #辞書型の入れ子（さらに辞書型）
for i in range(3):
    url = input("URLを入力してください: ")
    
    title = extract_title(url)
    time=datetime.datetime.now()

    person=f"person_{i}"
    title_list[person] = {"Title" : title , "time" :time}

for person, data in title_list.items():
    print(f"{person}: {data['Title']}, {data['time']}")

# print(f"タイトル: {title_list}")



