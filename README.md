# downloader-forum-5278

自動化爬取指定影片論壇頁面中的 m3u8 串流網址，並呼叫 [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE) 下載成 mp4。

![CLI demo](./assets/demo-cli.png)

## Tech Stack

| 項目 | 說明 |
|---|---|
| Python | 3.x |
| Playwright | 無頭瀏覽器，攔截 XHR 請求抓取 m3u8 |
| BeautifulSoup4 | 解析頁面 HTML，取得影片標題 |
| N_m3u8DL-RE | 外部下載引擎，首次執行自動下載到 `bin/` |
| PyYAML | 讀取 `config/*.yaml` 設定 |

## 專案結構

```
main.py                    # 進入點，登入判斷 + 主迴圈
src/
  config.py                 # 路徑常數 (下載資料夾、cookie、bin 位置)
  engine/
    scraper.py               # 核心：開瀏覽器 → 監聽 request → 過濾 m3u8 → 丟給 N_m3u8DL-RE
    auth_check.py             # 手動登入流程，將 storage_state 存成 .sessions/auth.json
  utils/
    block.py                  # Playwright route()，依 resource_type / 廣告網域擋掉不必要請求
    deps.py                    # 檢查/自動下載 N_m3u8DL-RE.exe
    common.py                  # yaml 讀取
    logger.py                  # logging 設定 (console + log/log.log)
config/
  config_default.yaml         # chrome 參數、封鎖清單、下載參數、目標網址
  config_dev.yaml              # N_m3u8DL-RE 下載連結等開發用設定
```

## 運作流程

1. `main.py` 啟動時檢查 `bin/N_m3u8DL-RE.exe` 是否存在，不存在則依 `config_dev.yaml` 的連結下載。
2. 檢查 `.sessions/auth.json` 是否存在；不存在則詢問是否登入 → 開啟瀏覽器讓使用者手動登入 → 儲存 `storage_state`。
3. 使用者輸入貼文網址後，`Scraper` 用該 cookie 開一個 context 造訪頁面：
   - 透過 `page.on('request', ...)` 監聽所有請求，篩出 `resource_type == 'xhr'` 且網址含 `m3u8` 的項目。
   - 同時用 `page.route()` 擋掉 image / font / media / stylesheet 與已知廣告網域，加速載入。
4. 解析 `<title>` 取得影片標題，逐一把抓到的 m3u8 網址丟給 `N_m3u8DL-RE` 下載到 `Downloads/`。

## Requirement

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python main.py
```

- 第一次執行會問是否需要登入狀態（Enter 預設為 y）。
- 依提示貼上論壇貼文網址即可開始抓取與下載，輸入 `q` 離開。
- 登入狀態存在 `.sessions/auth.json`，之後不會再重複詢問，除非該檔案被刪除。

## 設定檔說明 (`config/config_default.yaml`)

| 欄位 | 說明 |
|---|---|
| `chrome.wait_for_timeout` | 頁面載入等待上限 (ms) |
| `chrome.chrome_show` | 是否顯示瀏覽器視窗，除錯用 |
| `block_setting.blocked_types` | 要攔截的資源類型 |
| `block_setting.ad_domains` | 要攔截的廣告網域關鍵字 |
| `downloader_setting.thread_count` | N_m3u8DL-RE 下載執行緒數 |
| `downloader_setting.download_mode` | 傳給 N_m3u8DL-RE 的模式參數，預設 `--auto-select` |
| `downloader_setting.retry-count` | 下載失敗重試次數 |
| `url.5278_site` | 登入流程要開啟的網址 |

## 已知限制 / TODO

- 目前只認 `resource_type == 'xhr'` 的 m3u8 請求，若站方改用其他載入方式（例如直接嵌在 HTML 或走 fetch 以外的資源類型）需要更新 `_handle_request`。
- 下載引擎路徑寫死為 `.exe`，僅支援 Windows；若要跨平台需依 OS 判斷抓對應的 N_m3u8DL-RE 執行檔。
- 目前為單線程逐一下載多支影片（迴圈呼叫 subprocess），沒有平行化。
- 無自動重試整體流程的機制，request 監聽抓不到 m3u8 時只會記 log 並跳過。

## Changelog

- 2026.6.6　因應網站反爬升級，調整 監聽策略。
- 2026.8.5　專案架構重構：明確分層化；行為參數抽離至 config.yaml，路徑常數集中於 config.py 管理。
