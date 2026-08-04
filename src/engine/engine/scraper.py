from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from src.utils.common import load_ymal
from src.utils.block import apply_extreme_filter
import src.config as config
import subprocess
import logging

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
            self.config = load_ymal(config.CONFIG_DEFAULT)
        else:
            pass

        logging.error(f'影片')
        self.fetch_web_metadate()
        self.video_title = self.fetch_Video_title()
        self.trigger_download()

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

    def trigger_download(self):

        total_files = len(self.urls_list)

        if not total_files :
            print("沒有可下載的檔案")
            return False
        else:
            print(f"總共有 {total_files} 個影片準備下載")

            if total_files == 1:
                download_url = self.urls_list[0]
                video_title = f"{self.video_title}.mp4"
                try:
                    subprocess.run([
                        config.DOWNLOADER_PATH,
                        download_url,
                        # '--no-log', #logging for debug
                        '--save-name', video_title,
                        '--save-dir',config.DOWNLOAD_FOLDER,
                        '--thread-count', str(self.config["downloader_setting"]["thread_count"]),
                        self.config["downloader_setting"]["download_mode"],
                        '--download-retry-count',str(self.config["downloader_setting"]["retry-count"]),
                    ])
                except subprocess.CalledProcessError as e:
                    print(f"影片{self.video_title}下載失敗，錯誤原因:{e}")
                    logging.error(f'影片{self.video_title}下載失敗，錯誤原因:{e}')
                except Exception as e:
                    print(f"影片{self.video_title}下載失敗，預期外錯誤")
                
            elif total_files > 1:






if __name__ == "__main__":

    scarper = Scraper()
    scarper.url = input("輸入網址:google.com.tw")
    scarper.run()