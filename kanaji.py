import os
import sys
import re
import asyncio
import aiohttp
import threading
import xml.etree.ElementTree as ET
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtWebEngineCore import QWebEngineProfile
import yt_dlp

#類似度
from difflib import SequenceMatcher



class AdblockX:
    def __init__(self, page, adBlocker):
        self.page = page
        self.block_lists = []
        self.tracker_lists = []
        self.adBlocker = adBlocker
        self.session = aiohttp.ClientSession()

    async def fetch_lists(self, url):
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch lists: {response.status}")
                return (await response.text()).split('\n')
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    async def update_lists(self):
        block_lists, tracker_lists = await asyncio.gather(
            self.fetch_lists("https://easylist.to/easylist/easylist.txt"),
            self.fetch_lists("https://easylist.to/easylist/easyprivacy.txt")
        )
        if block_lists and block_lists != self.block_lists:
            self.block_lists = block_lists
            await self.blockAds()
        if tracker_lists and tracker_lists != self.tracker_lists:
            self.tracker_lists = tracker_lists
            await self.blockTrackers()

    async def blockAds(self):
        await self.adBlocker.setUrlFilterRules(self.block_lists)

    async def blockTrackers(self):
        await self.adBlocker.setUrlFilterRules(self.tracker_lists)

    async def main(self):
        await self.update_lists()

    async def updateBlockedContent(self, event):
        await self.update_lists()
        
        

        


class MainWindow(QMainWindow):
    # tab_id_title_list = []
    # tab_id_title_list.append({'id': 0, 'title': 'Home'})
    
    tab_id_title_list=[
        {'id': 0, 'title': 'Home'}
    ]

    
    
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.vertical_bar = QToolBar("Vertical Bar")
        self.vertical_bar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.vertical_bar)
        self.tabs = QTabWidget(self)##元々はselfなかった
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)

        self.setup_shortcuts()
        

        
    

           # ボタンを作成してタブバーの右上に配置
        self.add_tab_button = QPushButton("newタブ")
        self.add_tab_button.clicked.connect(self.add_new_tab())
        self.add_tab_button.setStyleSheet("background-color: white; color: black;")

        
        
        self.tabs.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)
        


        
      
        self.add_tab_button.setStyleSheet("background-color: gray; color: white;")
        self.add_tab_button.clicked.connect(self.add_new_tab)

        
        self.tabs.tabCloseRequested.connect(self.close_tab)

        
        
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        print(self.status)
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        self.load_shortcuts()
        back_btn = QAction("<", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
        next_btn = QAction(">", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
        reload_btn = QAction("○", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        self.toolbar = QToolBar("Actions")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.star_button = QAction("☆", self)
        self.star_button.setStatusTip("Add shortcut to vertical bar")
        self.star_button.triggered.connect(self.add_shortcut)
        self.toolbar.addAction(self.star_button)

        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_downloadRequested)
        stop_btn = QAction("X", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        # self.add_new_tab(QUrl('https://kanaji2002.github.io/Goth-toppage/top_page.html'), 'Homepage')
        self.vertical_bar = QToolBar("Vertical Bar")
        self.vertical_bar.setOrientation(Qt.Orientation.Vertical)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.vertical_bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        self.setWindowTitle("")
        self.setStyleSheet("background-color: gray; color: white;")  # 背景色を黒に変更
        self.tabs.setStyleSheet("QTabBar::tab { color: white; }")
        # self.delete_tab_index_list=[]
        
        # self.show()
        


    
    def close_tab(self, i):
        
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

        # else :
        #     # self.tabs.removeTab(i)
        #     print("not pushed left")
        
        print ("-------close_tab end--------")
        print(f"Current tab list: {self.tab_id_title_list}")

    def setup_shortcuts(self):
        # Ctrl+W で現在のタブを閉じる
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)

        # Ctrl+Space で現在のタブを閉じる
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+Space"), self)
        close_tab_shortcut.activated.connect(self.close_related_tab)

        # Ctrl+T で新しいタブを開く
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)

        # Ctrl+Q でアプリケーションを終了する
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

        # Alt+LeftArrow で前のタブに移動する
        prev_tab_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Left), self)
        prev_tab_shortcut.activated.connect(self.prev_tab)

        # Alt+RightArrow で次のタブに移動する
        next_tab_shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Right), self)
        next_tab_shortcut.activated.connect(self.next_tab)

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)

    def close_two_tab(self):
        # a=self.tabs.count()
        # print(a)
        # print(f'現在のリストは{self.tab_id_title_list}')
        
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            self.tabs.removeTab(current_index)
            self.tabs.removeTab(current_index)
            
            
    def close_related_tab(self):
        print(f'!!!!!!現在格納されているリスト！！{self.tab_id_title_list}')
        current_index = self.tabs.currentIndex()
        
        delete_tab_index_list = []
        
        if current_index != -1 and self.tabs.count() > 1:
            print(f'現在のタブは{current_index}')   
            # print(f'現在のタブの数は{self.tabs.count()}')
        
            
            # tem=self.tab_id_title_list[current_index]['title']
            # print(f'現在のタブのtitleは{tem}')
            

            for i in range(len(self.tab_id_title_list)):
                s = SequenceMatcher(None, self.tab_id_title_list[current_index]['title'], self.tab_id_title_list[i]['title'])
                # if s.ratio() > 0 and i!=current_index:
                #     print('類似度：{0}%，{1}.tabのIDは，{2}です．'.format(round(s.ratio()*100,1), self.tab_id_title_list[i]['title'],i))
                #     delete_tab_index_list.append(i)
                
                # current_tabも削除対象に含めル．つまり，類似度は　100%でOK
                print('tabのID{0}の類似度：{1}%.タイトルは，{2}です．'.format(i,round(s.ratio()*100,1), self.tab_id_title_list[i]['title']))
                if s.ratio() > 0.8 :
                    delete_tab_index_list.append(i)
                print(f'削除対象のタブは，{delete_tab_index_list}')

                
                # 関連するタブのindexをリストに追加していき，最後に，まとめて削除
            for delete_tab_index in reversed(delete_tab_index_list):
                
                if self.tabs.count() > 1:
                    print(f'{delete_tab_index}番目のタブを削除します.タイトルは，{self.tab_id_title_list[delete_tab_index]["title"]}です．')
                    # ここでのi
                    # print(delete_tab_index_list.index(delete_tab_index))
                    # self.tab_id_title_list.remove(self.tab_id_title_list[delete_tab_index_list.index(delete_tab_index)])
                    del self.tab_id_title_list[delete_tab_index]
                    self.tabs.removeTab(delete_tab_index)
                    delete_tab_index_list.remove(delete_tab_index)
            tempo_list=[]
            for index, value in enumerate(self.tab_id_title_list):
                updated_list={'id': index, 'title': value['title']}
                tempo_list.append(updated_list)
                
            self.tab_id_title_list=tempo_list
            print(f'更新後のリストは{self.tab_id_title_list}')
                
                


        print ("-------close_related_tab end--------")
        print(f"Current tab list: {self.tab_id_title_list}")
        
                
                
         
    

    # def add_new_tab(self):
    #     self.addTab(f"New Tab {self.tabs.count() + 1}", f"This is new tab {self.tabs.count() + 1}")




    def prev_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index > 0:
            self.tabs.setCurrentIndex(current_index - 1)

    def next_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index < self.tabs.count() - 1:
            self.tabs.setCurrentIndex(current_index + 1)




      

    def add_new_tab(self, qurl=None, label="ブランク"):
        
        qurl = QUrl('https://kanaji2002.github.io/Goth-toppage/top_page.html')            
        browser = QWebEngineView()
        print(qurl)
        browser.setUrl(qurl)
        
        i = self.tabs.addTab(browser, label)
        print(f'{i}番目のタブを開いたよ')
        self.tabs.setCurrentIndex(i)
        new_title = browser.page().title()
        if new_title == '':
            new_title = 'Document'
            
            
            
        # タイトルとIDのリストを更新
        found = False
        
        
        for tab_info in self.tab_id_title_list:
            
            
            if tab_info['id'] == i:
                tab_info['title'] = new_title
                found = True
                break
        
        if not found:
            # 空いているIDを探す
            available_id = None
            for idx in range(self.tabs.count()):
                if not any(tab_info['id'] == idx for tab_info in self.tab_id_title_list):
                    available_id = idx
                    break
            
            if available_id is not None:
                self.tab_id_title_list.insert(available_id, {'id': available_id, 'title': new_title})
            else:
                self.tab_id_title_list.append({'id': i, 'title': new_title})

        print(f"New tab opened: ID={i}, Title={new_title}")
        
        # タイトル変更時に on_title_changed を呼び出す
        browser.titleChanged.connect(lambda new_title, i=i: self.on_title_changed(new_title, i))
        
        # タブのIDとタイトルをリストに追加
        
        
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        
        browser.loadFinished.connect(lambda _, i=i, : self.tabs.setTabText(i, browser.page().title()[:7] if len(browser.page().title()) > 7 else browser.page().title().ljust(7)))
        browser.iconChanged.connect(lambda _, i=i, browser=browser: self.tabs.setTabIcon(i, browser.icon()))
        
        
        print ("-------add_new_tab end--------")
        print(f"Current tab list: {self.tab_id_title_list}")
        
    def on_title_changed(self, new_title, i):
        # タイトルが変更されたらリストを更新
        for tab_info in self.tab_id_title_list:
            if tab_info['id'] == i:
                tab_info['title'] = new_title
                break

        # self.tab_id_title_list.append({i: new_title})
        #print(f"Tab updated: ID={i}, Title={new_title}")
        print(f"Current tab list: {self.tab_id_title_list}")
               
    
    

        
#そのタブのアイコンを押したら，dialogが出てきて（出てこなくてもいい），関連するタブを削除する

    #my test code
    def tab_id_print(self,i):
        return 
        print(f'now open tab is {i}')
  
    # タブを開く度に，リストに，辞書型で，タブのidとそのタブのタイトルを保存しておく関数
    # def tab_id_save(self, i,browser, tab_id_list):
    #         # Add the tab ID and title to the tab_id_list
    #     tab_id = self.tabs.indexOf(browser)
    #     tab_title = browser.page().title()
    #     tab_id_list.append({tab_id: tab_title})

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())




    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        # title = browser.page().title()
        title=self.tabs.currentWidget().page().title()
        formatted_title = title[:7] if len(title) > 7 else title.ljust(7)
        print(formatted_title)
        self.setWindowTitle("%s Goth" % formatted_title)
        
        
        self.tabs.setTabText(self.tabs.currentIndex(), formatted_title)
        if title is not None:
            print(title)
        else:
            print("Noneだよ")
        

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://kanaji2002.github.io/Goth-toppage/top_page.html"))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if "google.com/search?q=" in url:
            self.tabs.currentWidget().setUrl(QUrl(url))
        else:
            google_search_url = "https://www.google.com/search?q=" + url
            self.tabs.currentWidget().setUrl(QUrl(google_search_url))

    def update_urlbar(self, q, browser=None):
        # 現在開いているタブのみみ受け付ける．
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 使わない
    def extract_video_id(self, youtube_url):
        video_id_pattern = re.compile(r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&?/\s]+)')
        match = video_id_pattern.search(youtube_url)
        if match:
            return match.group(1)
        return None

    # 使わない
    def play_youtube_video(self):
        youtube_url = self.youtube_id_bar.text()
        video_id = self.extract_video_id(youtube_url)
        if video_id:
            embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"
            self.add_new_tab(QUrl(embed_url), 'YouTube Video')
        else:
            pass

    # 使わない
    def on_downloadRequested(self, download):
        home_dir = os.path.expanduser("~")
        download_dir = os.path.join(home_dir, "Downloads")
        download_filename = download.suggestedFileName()
        QWebEngineProfile.defaultProfile().setDownloadDirectory(download_dir)
        download.setDownloadFileName(download_filename)
        download.accept()
        self.show_download_progress(download)

    # 使わない
    def show_download_progress(self, download):
        progress_bar = QProgressBar(self.status)
        self.status.addPermanentWidget(progress_bar)
        download.downloadProgress.connect(lambda bytesReceived, bytesTotal, progress_bar=progress_bar: progress_bar.setValue(int((bytesReceived / bytesTotal) * 100) if bytesTotal > 0 else 0))
        download.finished.connect(lambda progress_bar=progress_bar: progress_bar.deleteLater())
   #使わない
    def update_progress_bar(self, progress_bar, bytesReceived, bytesTotal):
        if bytesTotal > 0:
            progress = (bytesReceived / bytesTotal) * 100
            progress_bar.setValue(int(progress))
   #使わない

    def remove_progress_bar(self, progress_bar):
        self.status.removeWidget(progress_bar)
        progress_bar.deleteLater()

    def download_youtube_video(self):
        youtube_url = self.youtube_download_bar.text()
        video_id = self.extract_video_id(youtube_url)
        if video_id:
            threading.Thread(target=self.download_video, args=(video_id,)).start()
        else:
            pass

    def download_video(self, video_id):
        ydl_opts = {'format': 'mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'http://www.youtube.com/watch?v={video_id}'])

    def add_shortcut(self):
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            url = current_tab.page().url().toString()
            title = current_tab.page().title()
            shortcut_button = QAction("", self)
            shortcut_button.setText(current_tab.page().title())
            shortcut_button.setToolTip(url)
            shortcut_button.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl(url)))
            self.vertical_bar.addAction(shortcut_button)
            self.tabs.currentWidget().setUrl(QUrl(url))
            self.save_shortcut_to_xml(title, url)

    def save_shortcut_to_xml(self, title, url):
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        for shortcut in root.findall('shortcut'):
            if shortcut.find('url').text == url:
                print("Bookmark already exists.")
                return
        shortcut = ET.SubElement(root, 'shortcut')
        ET.SubElement(shortcut, 'title').text = title
        ET.SubElement(shortcut, 'url').text = url
        tree.write('shortcuts.xml')

    def load_shortcuts(self):
        if not os.path.exists('shortcuts.xml'):
            return
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        added_urls = set()
        for shortcut in root.findall('shortcut'):
            title = shortcut.find('title').text
            url = shortcut.find('url').text
            if url not in added_urls:
                self.add_website_shortcut(url, title)
                added_urls.add(url)

    def add_website_shortcut(self, url, name):
        name = name[:23] + '...' if len(name) > 23 else name
        shortcut_button = QAction(name, self)
        shortcut_button.url = url
        view = QWebEngineView()
        view.load(QUrl(url))
        view.iconChanged.connect(lambda icon, button=shortcut_button: button.setIcon(icon))
        shortcut_button.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl(url)))
        self.vertical_bar.addAction(shortcut_button)
        self.save_shortcut_to_xml(name, url)

    def create_database(self):
        if not os.path.exists('shortcuts.xml'):
            root = ET.Element("shortcuts")
            tree = ET.ElementTree(root)
            tree.write('shortcuts.xml')

class BookmarkAction(QAction):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.url = ""
#aaa
    def showContextMenu(self, point):
        contextMenu = QMenu(self.parent())
        deleteAction = QAction("削除", self)
        deleteAction.triggered.connect(self.deleteBookmark)
        contextMenu.addAction(deleteAction)
        contextMenu.exec_(self.mapToGlobal(point))

    def deleteBookmark(self):
        tree = ET.parse('shortcuts.xml')
        root = tree.getroot()
        for shortcut in root.findall('shortcut'):
            if shortcut.find('url').text == self.url:
                root.remove(shortcut)
                tree.write('shortcuts.xml')
                break
        self.parent().removeAction(self)

app = QApplication(sys.argv)
app.setApplicationName("Goth")
window = MainWindow()
window.create_database()
window.show()
app.exec()