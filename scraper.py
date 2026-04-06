from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import subprocess
import config
import os
import utils.block_ads
class GetData:


    def __init__(self,url):
        #屬性
        self.url = url
        self.soup = None
        self.url_list =[]
        self.title =None
        self.wating_secound = 10*1000
        #m3u8 參數
        self.m3u8_thread_count = 8
        
        #run
        self._run()
        self._download()
    def _run(self):
        self._get_m3u8()

    def _get_m3u8(self):


        def _get_title(page_content):
            '''抓標題'''
            content = page_content
            soup = BeautifulSoup(content,'html.parser')

            title = soup.find('title').text.strip()
            self.title = title.split('-')[0].strip()  #正則匹配與去除多餘
            print(self.title)

        def _handle_request(request):
                if '.m3u8?' in request.url:
                    m3u8_url = request.url
                    self.url_list.append(m3u8_url)

        def _ensure_login(browser):

            if os.path.exists(config.COOKIE_FILE):
                print('[。]登入狀態')
                return browser.new_context(storage_state=config.COOKIE_FILE)
            else:
                print('[。]未入狀態')
                return browser.new_context()
            
        with sync_playwright() as p:

            browser =  p.chromium.launch( headless=True) # False 開啟chrome 視窗;True 關閉chrome視窗

            context = _ensure_login(browser)
            page = context.new_page()

            page.on('request', _handle_request) #先監聽request，在進入

            interceptor = utils.block_ads.BlockAds() # 過濾器
            page.route("**/*", interceptor.apply_extreme_filter)

            page.goto(self.url, wait_until='domcontentloaded', timeout=60000)
            
            print(f'等待解析時間 {self.wating_secound/1000 } 秒')
            page.wait_for_timeout(self.wating_secound ) #抓不到調這裡
            _get_title(page.content())


    def _download(self):
        '''下載function'''
        #init
        url_count = len(self.url_list)

        if not self.url_list:
            print('[!]沒找到m3u8 URL')
            return
        if url_count == 1:
            target_url = self.url_list[0]
            output = f'{self.title}.mp4'
            subprocess.run([
            config.DOWNLOADER_PATH,  # 跟ffmpeg一樣直接叫名字
            target_url,
            # '--no-log', #關閉log
            '--save-name', self.title,
            '--save-dir',config.DOWNLOAD_FOLDER,  # 目錄參數
            '--thread-count', str(self.m3u8_thread_count),
            '--auto-select',
            '--download-retry-count',str(10), # 異常後重試次數
            ])
        
        elif url_count > 1:


            print(f'[!]批量模式:下載數量 {len(self.url_list)} 個影片')
            for i, m3u8 in enumerate(self.url_list, start=1):
                target_url = m3u8
                file_name = f"{self.title}_{i}"
                subprocess.run([
                config.DOWNLOADER_PATH,  # 跟ffmpeg一樣直接叫名字
                target_url,
                # '--no-log', #關閉log
                '--save-name', file_name,
                '--save-dir',config.DOWNLOAD_FOLDER,  # 目錄參數
                '--thread-count', str(self.m3u8_thread_count),
                '--auto-select',
                '--download-retry-count',str(10), # 異常後重試次數
                ])
if __name__ == '__main__':
    url = ''
    start = GetData(url)