from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from src.utils.common import load_ymal

from src.config import CONFIG_DEFAULT
from src.utils.block import apply_extreme_filter
class Scraper:


    def __init__(self):
        self.url = None
        self.urls_list =[]
        self.video_title =None
        self.config = None
        self.page = None
        self.page_content = None

    def _handle_request(self, request):
        '''Filter and add to the list; only URLs matching m3u8 and xhr styles will be added.'''
        if "m3u8" in request.url:
            if request.resource_type == 'xhr':
                m3u8_url = request.url
                self.urls_list.append(m3u8_url)
    
    def run(self):
        # 讀取 config
        if self.config is None:
            self.config = load_ymal(CONFIG_DEFAULT)
        else:
            pass

        self.fetch_web_metadate()
        self.video_title = self.fetch_Video_title()
        print(self.urls_list)


    def fetch_Video_title(self):
        soup = BeautifulSoup(self.page_content,'html.parser')
        title = soup.find('title').text.strip()
        title = title.split('-')[0].strip()
        return title
    
    def fetch_web_metadate(self):
        '''模擬瀏覽器行為、抓取m3u8 url'''
        #啟動 Playwright 環境
        with sync_playwright() as p:
            #啟動 chrome 瀏覽器 (headless=True 關閉瀏覽器; headless=False 開啟瀏覽器)
            browser =  p.chromium.launch( headless=False)
            # 打開新頁
            self.page = browser.new_page()
            # on 方法監聽 請求 事件時觸發過濾與捕捉
            self.page.on('request', self._handle_request) 
            self.page.route("**/*", apply_extreme_filter)


            self.page.goto(self.url, wait_until='domcontentloaded', timeout=60000)
            self.page_content = self.page.content()
            self.page.wait_for_timeout(self.config['chrome']['wait_for_timeout'])


    # def _ensure_login(browser):

    #     if os.path.exists(config.COOKIE_FILE):
    #         print('[。]登入狀態')
    #         return browser.new_context(storage_state=config.COOKIE_FILE)
    #     else:
    #         print('[。]未入狀態')
    #         return browser.new_context()


    def extract_media_metadata(page_content):

        #啟動 Playwright 環境
        with sync_playwright() as p:
            #啟動 chrome 瀏覽器 (headless=True 關閉瀏覽器; headless=False 開啟瀏覽器)
            browser =  p.chromium.launch( headless=False)


if __name__ == "__main__":

    scarper = Scraper()
    scarper.url = input("輸入網址:google.com.tw")
    scarper.run()