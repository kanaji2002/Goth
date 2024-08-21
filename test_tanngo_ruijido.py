from difflib import SequenceMatcher
import itertools

lst = {
    0: "ほうれんそうとえのきの和え物",
    1: "ほうれんそうとエリンギのごま和え",
    2: "ほうれんそうの明太子和え",
    3: "ほうれんそうのたらこ和え",
    4: "ほうれんそうとにんじんのごま和え",
    5: "ほうれんそうのおかか和え",
    6: "ほうれんそうのごま和え",
    7: "ほうれんそうのソテー",
    8: "ほうれんそうのソテー温泉たまごのせ",
}

a=[]


# s = SequenceMatcher(None,lst[0],a[0])
# print(s.ratio())
t=3

# list(fruits_dict.keys())[1]
for i in range(len(lst)):
    s = SequenceMatcher(None, list(lst.values())[t], list(lst.values())[i])
    if s.ratio() > 0.7 and i!=t:
        print('類似度：{0}%，{1}ss{2}'.format(round(s.ratio()*100,1), lst[i],3))