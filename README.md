# 5278 爬蟲工具
## Tech Stack
* - python
* - 自動化瀏覽器
* - html解析
* - N_m3u8DL-RE 下載引擎
## Feature
* - CLI操作
* - 自動命名
* - 批量下載
* - 動態架構

## Requirement
1. 打開CMD，安裝套件
```
pip install -r requirements.txt
```
2. 安裝給爬蟲套件用的 chorme 瀏覽器
```
playwright install chromium
```
## Usage



1. 點擊 main.py

2. 會在根目錄創建下載資料夾，並自動從官方抓取[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE/releases)

## Optional - Log In  功能
有些帖子要權限，所以要登入帳號。

執行 `login.py`檔案，在瀏覽器登入後

會在.session自動創建你的cookie.jsopn

在`main.py`中，就能用權限帳號進行登入了