import Levenshtein

def levenshtein_distance(str1, str2):
    return Levenshtein.distance(str1, str2)

# 使用例
# print(f"レーベンシュタイン距離：{levenshtein_distance("kittensssss", "sitting")}")  # 出力: 3


########url_list.py########
from title_get import extract_title
import datetime


#タイトルの距離を計算する関数
def title_distance():
    url_list = []
    time_list = []
    title_list = {} #辞書型の入れ子（さらに辞書型）
    for i in range(3):
        url = input("URLを入力してください: ")
        
        title = extract_title(url)
        time=datetime.datetime.now()

        person=f"person_{i}"
        title_list[person] = {"Title" : title , "time" :time}
        
        tempo='title_example'

    for person, data in title_list.items():
        print(f"{person}: {data['Title']}, {data['time']}")
        print(f"レーベンシュタイン距離：{levenshtein_distance(data['Title'], tempo)}")  # 出力: 3
        tempo=data['Title']



# title_distance()


