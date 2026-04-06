from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import subprocess
import config
import os
"""
https://5278.cc/forum.php?mod=viewthread&tid=1680898&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline%26typeid%3D1109
"""
class GetData:


    def __init__(self,url):

        self.url = url
        self.soup = None
        self.url_list =[]
        self.title =None

        #run
        self._run()
        self._download()
    def _run(self):
        self._get_m3u8()

    def _get_m3u8(self):


        def _get_title(page_content):
            '''抓標題，注意context'''
            content = page_content
            soup = BeautifulSoup(content,'html.parser')

            title = soup.find('title').text.strip()
            self.title = title.split('-')[0].strip()  #正則匹配與去除多餘
            print(self.title)

        def handle_request(request):
                if '.m3u8?' in request.url:
                    m3u8_url = request.url
                    self.url_list.append(m3u8_url)
                    print(self.url_list)

        with sync_playwright() as p:

            browser =  p.chromium.launch(headless=True) # False 開啟chrome 視窗;True 關閉chrome視窗
            context =  browser.new_context()
            page = context.new_page()

            page.on('request', handle_request) #先監聽request，在進入
            page.goto(self.url, wait_until='domcontentloaded', timeout=60000)
            
            print('解析內容')
            _get_title(page.content())
            page.wait_for_timeout(10000) #等待參數，可以在調適

    def _download(self):
        '''下載function'''
        #init
        url_count = len(self.url_list)

        if not self.url_list:
            print('沒找到m3u8 URL，無法下載')
            return
        if url_count == 1:
            target_url = self.url_list[0]
            output = f'{self.title}.mp4'
            subprocess.run([
            'N_m3u8DL-RE',  # 跟ffmpeg一樣直接叫名字
            target_url,
            '--save-name', self.title,
            '--save-dir',config.DOWNLOAD_FOLDER,  # 目錄參數
            '--thread-count', str(os.cpu_count()),
            '--auto-select',
            ])
        
        elif url_count > 1:

            print('目標超過一個')
            for i, m3u8 in enumerate(self.url_list, start=1):
                target_url = m3u8
                filr_name = f"{self.title}_{i}"
                subprocess.run([
                'N_m3u8DL-RE',  # 跟ffmpeg一樣直接叫名字
                target_url,
                '--save-name', filr_name[i],
                '--save-dir',config.DOWNLOAD_FOLDER,  # 目錄參數
                '--thread-count', str(os.cpu_count()),
                '--auto-select',
                ])
if __name__ == '__main__':
    url = ''
    start = GetData(url)