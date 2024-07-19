import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_title(url):
    try:
        # URLのスキームがない場合、'http://'を追加
        if not urlparse(url).scheme:
            url = 'http://' + url

        # URLにリクエストを送信
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # エラーがあれば例外を発生させる

        # HTMLをパース
        soup = BeautifulSoup(response.text, 'html.parser')

        # titleタグからタイトルを抽出
        title = soup.title.string if soup.title else None

        # タイトルがない場合、h1タグを探す
        if not title:
            h1 = soup.find('h1')
            title = h1.string if h1 else "タイトルが見つかりません"

        return title.strip()

    except requests.RequestException as e:
        return f"エラー: {str(e)}"
    except Exception as e:
        return f"予期せぬエラー: {str(e)}"

# # 使用例
# url = input("URLを入力してください: ")
# title = extract_title(url)
# print(f"タイトル: {title}")